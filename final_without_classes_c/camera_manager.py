import cv2
import numpy as np
import pyrealsense2 as rs
from asset_manager import *

class CameraManager:
    def __init__(self, device_id=0):
        self.device_id = device_id
        self.use_realsense = True
        self.pipeline = None
        self.cap = None
        self.camera_detected = False

        try:
            # Attempt to initialize RealSense camera
            self.pipeline = rs.pipeline()
            config = rs.config()

            context = rs.context()
            device_list = context.query_devices()

            realsense_devices = {device.get_info(rs.camera_info.name): device.get_info(rs.camera_info.serial_number) for device in device_list}

            if realsense_devices:
                device_serial = next(iter(realsense_devices.values()))
                config.enable_device(device_serial)
                config.enable_stream(rs.stream.depth)
                config.enable_stream(rs.stream.color)
                self.pipeline.start(config)
                print("Using RealSense camera")
                self.camera_detected = True
            else:
                raise Exception("No RealSense devices found")

        except Exception as e:
            print(f"Failed to initialize RealSense camera: {e}")
            print("Falling back to normal webcam")
            self.use_realsense = False

            try:
                self.cap = cv2.VideoCapture(self.device_id)
                if not self.cap.isOpened():
                    raise Exception("Failed to open webcam")
                print("Successfully initialized webcam")
                self.camera_detected = True
            except Exception as e:
                print(f"Failed to initialize webcam: {e}")
                self.camera_detected = False


    def start(self):
        """
        Start the camera stream

        For RealSense cameras, the stream is already started in __init__
        For normal webcams, this method ensures the video capture is opend

        This Method should be idempotent
        """
        if not self.camera_detected:
            return False
        if not self.use_realsense:
            if not self.cap.isOpened():
                return self.cap.open(self.device_id)
        return True


    # stop the camera stream and release the allocated resources for both camera-options
    def stop(self):
    
        if self.use_realsense:
            if self.pipeline:
                # stop the RealSense pipeline
                self.pipeline.stop()
        else:
            if self.cap and self.cap.isOpened():
                # Release the OpenCV VideoCapture object, thereby stopping the stream
                self.cap.release()

    def get_frame(self):
        """
        Capture and return a frame from the camera
        This function is called in other files and acts as a facade
        The appropriate methode gets called depending if a RealSense camera or 
        a normal webcam is being used
        """

        if self.use_realsense:
            return self._get_realsense_frame()
        else:
            return self._get_webcam_frame()


    def _get_realsense_frame(self):
        """
        Capture and process a frame from the RealSense camera.
        
        This method ...
        1. Captures a set of depth and color frames
        2. Aligns the depth frame to the color frame
        3. Converts the frames to numpy arrays
        4. Performs background removal based on depth information
        """

        # wait for a coherent pair of frames: depth and color
        frames = self.pipeline.wait_for_frames()

        # Allign the depth frame to color frame
        aligned_frames = rs.align(rs.stream.color).process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        # Convert both images to numpy arrays
        # The resulting arrays are 2D for the dpeth_image and 3D for the color_image
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Convert the color image from BGR to RGB
        # OpenCV uses BGR by default, but we want RGB for consistency
        color_image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

        # Get depth scale for converting depth values to meters
        depth_scale = self.pipeline.get_active_profile().get_device().first_depth_sensor().get_depth_scale()

        # Convert the background removal threshold from meters to device units
        threshold = background_removal_threshold / depth_scale

        # Create a foreground mask based on the depth threshold
        # Pixel with depth values within the threshold are considered foreground (255)
        # Other pixels are considered background (0)
        foreground_mask = np.where((depth_image > 0) & (depth_image < threshold), 255, 0).astype(np.uint8)

        # Apply the mask to the color image to extract the foreground
        # This keeps only the parts of the image where the mask is 255 (foreground)
        foreground_image = cv2.bitwise_and(color_image_rgb, color_image_rgb, mask=foreground_mask)

        return color_image_rgb, foreground_image


    def _get_webcam_frame(self):
        """
        Capture and process a frame from the normal webcam.
        This method captures a color frame from the webcam and converts it to RGB.
        Since there is no depth information available, it does not remove any background.
        Insead, it creates a dummy foreground image that's identical to the color image for consistency and correct return values 
        """

        # Capture a frame from the webcam
        ret, frame = self.cap.read()

        # Check if the frame capture was successful
        if not ret:
            return None, None

        # Convert the captured frame from BGR to RGB
        color_image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
        # Create the dummy duplicate by copying the original image
        foreground_image = color_image_rgb    
   
        return color_image_rgb, foreground_image