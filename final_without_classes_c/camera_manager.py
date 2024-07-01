import cv2
import numpy as np
import pyrealsense2 as rs
from asset_manager import *


class CameraManager:
    
    # Initialize the CameraManager
    # Try to use a RealSense Camera. Use a normal webcam if that fails
    def __init__(self, device_id=0):
        self.device_id = device_id
        self.use_realsense = True
        self.pipeline = None
        self.cap = None

        try:
            # Attempt to initialize RealSense camera
            self.pipeline = rs.pipeline()
            config = rs.config()

            # Create a context object. This object owns the handles to all connected RealSense devices
            context = rs.context()

            # Get a list of all connected RealSense devices
            device_list = context.query_devices()

            # Create a dictionary of available RealSense devices
            # The keys are device names. the values are their serial numbers
            realsense_devices = {device.get_info(rs.camera_info.name): device.get_info(rs.camera_info.serial_number) for device in device_list}

            if realsense_devices:
                # If RealSense devices are available, use the first one
                device_serial = next(iter(realsense_devices.values()))

                # Use the choosen device using its serial number
                config.enable_device(device_serial)

                # Enable the depth stream to capture depth information 
                config.enable_stream(rs.stream.depth)

                #Enable the color stream to capture RGB information
                config.enable_stream(rs.stream.color)

                # Start the RealSense pipeline with the configured settings
                self.pipeline.start(config)
                print("Using RealSense camera")
            else:
                # If no RealSense devices are found, raise an exception
                raise Exception("No RealSense devices found")

        except Exception as e:
            # If RealSense initialisation fails, fall back to a normal webcam
            print(f"Failed to initialize RealSense camera: {e}")
            print("Falling back to normal webcam")
            self.use_realsense = False

            # Initialize OpenCV's VideCapture for the specified device
            self.cap = cv2.VideoCapture(self.device_id)

    def start(self):
        """
        Start the camera stream

        For RealSense cameras, the stream is already started in __init__
        For normal webcams, this method ensures the video capture is opend

        This Method should be idempotent
        """

        if not self.use_realsense and not self.cap.isOpened():
            # If it's not already open, open the video capture for normal webcams
            self.cap.open(self.device_id)


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


"""
ab hier nur noch alte überreste, die wahrscheinlich gelöscht werden können
"""

# class CameraManager:
#     def __init__(self, device_id=0):
#         self.device_id = device_id
#         self.cap = cv2.VideoCapture(self.device_id)

#     def start(self):
#         if not self.cap.isOpened():
#             self.cap.open(self.device_id)

#     def stop(self):
#         if self.cap.isOpened():
#             self.cap.release()

#     def get_frame(self):
#         ret, frame = self.cap.read()
#         if not ret:
#             return None, None

#         color_image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         foreground_mask = np.ones((frame.shape[0], frame.shape[1]), dtype=np.uint8) * 255
#         foreground_image = cv2.bitwise_and(color_image_rgb, color_image_rgb, mask=foreground_mask)

#         return color_image_rgb, foreground_image
    

# class CameraManager:
#     def __init__(self, device_id):
#         self.device_id = device_id
#         self.pipeline = rs.pipeline()
#         self.config = rs.config()

#         # List all available RealSense devices
#         context = rs.context()
#         device_list = context.query_devices()
#         realsense_devices = {device.get_info(rs.camera_info.name): device.get_info(rs.camera_info.serial_number) for device in device_list}

#         # Configure and start the RealSense camera
#         if device_id in realsense_devices.values():
#             self.config.enable_device(device_id)  # Use the serial number directly
#         self.config.enable_stream(rs.stream.depth)
#         self.config.enable_stream(rs.stream.color)

#     def start(self):
#         self.pipeline.start(self.config)

#     def stop(self):
#         self.pipeline.stop()    

#     def get_frame(self):
#         # Wait for a coherent set of frames: a color frame and a depth frame
#         frames = self.pipeline.wait_for_frames()
#         aligned_frames = rs.align(rs.stream.color).process(frames)
#         depth_frame = aligned_frames.get_depth_frame()
#         color_frame = aligned_frames.get_color_frame()

#         # Convert images to NumPy arrays
#         depth_image = np.asanyarray(depth_frame.get_data())
#         color_image = np.asanyarray(color_frame.get_data())

#         # Convert the BGR image to an RGB image
#         color_image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

#         # Generate a simple foreground mask by ignoring all depth values that are above a threshold
#         depth_scale = self.pipeline.get_active_profile().get_device().first_depth_sensor().get_depth_scale()
#         #threshold = AssetManager.background_removal_threshold / depth_scale
#         threshold = background_removal_threshold / depth_scale
#         foreground_mask = np.where((depth_image > 0) & (depth_image < threshold), 255, 0).astype(np.uint8)

#         # Apply the mask to the color image to extract the foreground
#         foreground_image = cv2.bitwise_and(color_image_rgb, color_image_rgb, mask=foreground_mask)

#         return color_image_rgb, foreground_image
