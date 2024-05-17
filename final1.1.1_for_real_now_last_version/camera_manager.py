import pyrealsense2 as rs
import numpy as np
import cv2
from asset_manager import AssetManager

class CameraManager:
    def __init__(self, device_id):
        self.device_id = device_id
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        # List all available RealSense devices
        context = rs.context()
        device_list = context.query_devices()
        realsense_devices = {device.get_info(rs.camera_info.name): device.get_info(rs.camera_info.serial_number) for device in device_list}

        # Configure and start the RealSense camera
        if device_id in realsense_devices:
            self.config.enable_device(realsense_devices[device_id])  # Use the serial number
        self.config.enable_stream(rs.stream.depth)
        self.config.enable_stream(rs.stream.color)

    def start(self):
        self.pipeline.start(self.config)

    def stop(self):
        self.pipeline.stop()    

    def get_frame(self):
        # Wait for a coherent set of frames: a color frame and a depth frame
        frames = self.pipeline.wait_for_frames()
        aligned_frames = rs.align(rs.stream.color).process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        # Convert images to NumPy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Convert the BGR image to an RGB image
        color_image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

        # Generate a simple foreground mask by ignoring all depth values that are above a threshold
        depth_scale = self.pipeline.get_active_profile().get_device().first_depth_sensor().get_depth_scale()
        threshold = AssetManager.background_removal_threshold / depth_scale
        foreground_mask = np.where((depth_image > 0) & (depth_image < threshold), 255, 0).astype(np.uint8)

        # Apply the mask to the color image to extract the foreground
        foreground_image = cv2.bitwise_and(color_image_rgb, color_image_rgb, mask=foreground_mask)

        # Combine the original image and the image with the background removed side by side
        #combined_image = np.hstack((color_image_rgb, foreground_image))
        # not used anymore, the streams are now returned separately
    
        return color_image_rgb, foreground_image