import cv2
import numpy as np
import pyrealsense2 as rs
from asset_manager import *


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
        if device_id in realsense_devices.values():
            self.config.enable_device(device_id)  # Use the serial number directly
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
        #threshold = AssetManager.background_removal_threshold / depth_scale
        threshold = background_removal_threshold / depth_scale
        foreground_mask = np.where((depth_image > 0) & (depth_image < threshold), 255, 0).astype(np.uint8)

        # Apply the mask to the color image to extract the foreground
        foreground_image = cv2.bitwise_and(color_image_rgb, color_image_rgb, mask=foreground_mask)

        return color_image_rgb, foreground_image
