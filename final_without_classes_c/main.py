import pygame
import sys
import os
import cv2
import mediapipe as mp
import numpy as np
import ctypes
from camera_manager import CameraManager
from face_detector import FaceCenterDetector
from utils import load_and_scale, get_system_scaling
from layer_adjustment import anpassung_der_ebenen
from asset_manager import *

# Initialize Pygame to be able to use it at all
pygame.init()

# Initialize CameraManager (calling the init())
# This will attempt to use a RealSense camera first, then fall back to a normal webcam if necessary
camera = CameraManager()
camera.start()

# Get system scaling factors for both horizontal and vertical directions
horizontal_scale, vertical_scale = get_system_scaling()

# Debug output of the scaling from the step before
if horizontal_scale is not None and vertical_scale is not None:
    print("Horizontal system scaling:", horizontal_scale)
    print("Vertical system scaling:", vertical_scale)

# Print screen dimensions for debugging
print("Screen resolution width: ", width, "Screen resolution height: ",  height)

# Define a pygame window and starting point
window = pygame.display.set_mode((width, height), pygame.SCALED)
x_center, y_center = width // 2, height // 2

# Load images
layer1 = load_and_scale(image_layer1, scale_factor=scale_layer1)
layer2 = load_and_scale(image_layer2, scale_factor=scale_layer2)
layer3 = load_and_scale(image_layer3, scale_factor=scale_layer3)
layer4 = load_and_scale(image_layer4, scale_factor=scale_layer4)
layer0_frame = load_and_scale(image_layer0_frame, scale_layer0)
layer0_leftCurtain = load_and_scale(image_layer0_left_curtain, scale_layer0)
layer0_rightCurtain = load_and_scale(image_layer0_right_curtain, scale_layer0)

# Initial positions (centered)
x_layer1, y_layer1 = x_center - layer1.get_width() // 2, y_center - layer1.get_height() // 2
x_layer2, y_layer2 = x_center - layer2.get_width() // 2, y_center - layer2.get_height() // 2
x_layer3, y_layer3 = x_center - layer3.get_width() // 2, y_center - layer3.get_height() // 2
x_layer4, y_layer4 = x_center - layer4.get_width() // 2, y_center - layer4.get_height() // 2

# Last known position 
lastknown_x, lastknown_y = x_center, y_center

# Initiate the current face position outside the loop to prevent the layers from snapping back to center
# and avoid crashing the app when no faces are detected at startup
x_face_now, y_face_now = x_center, y_center

# Initialize game loop variables
running = True
face_detector = FaceCenterDetector()
curtains_visible = True


# Game loop
with mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
    while running:

        # Get a new frame from the camera
        color_image_rgb, foreground_image = camera.get_frame()
        if color_image_rgb is None or foreground_image is None:
            continue
        image = foreground_image

        # Handle Pygame events including 'q' for closing the application
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

        # Process the gathered frame for face detection
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)
        
        # Try to detect a face and retrieve the the coordinates of the center of the face
        face_center = face_detector.get_face_center(image)
        if face_center is not None:
            x_face_now, y_face_now = face_center 
            # multiply the detected face position (between 0 and 1) with the screen resolution to scale the movement better to the whole screen
            x_face_now = x_face_now * width
            y_face_now = y_face_now * height

            # Update last known position
            lastknown_x, lastknown_y = x_face_now, y_face_now
        elif lastknown_x is not None and lastknown_y is not None:
            # Use last known position if face is lost
            x_face_now, y_face_now = lastknown_x, lastknown_y
        else:
            # If no face has been detected yet, use screen center
            x_face_now, y_face_now = x_center, y_center
        
        # Smooth the face movement
        x_face_neu = ((x_face_now*3 + lastknown_x * 9) / 10)
        y_face_neu = ((y_face_now*3 + lastknown_y * 9) / 10)
        print(x_face_neu, y_face_neu)

        # Process the frame to detect if a face is present detected at all to control the curtains
        face_detector.process_frame(image)
        curtains_visible = not face_detector.face_detected

        # Adjust the layer positions based on the face position
        x_layer1, y_layer1 = anpassung_der_ebenen(x_face_neu, y_face_neu, (x_center - layer1.get_width() // 2, y_center - layer1.get_height() // 2), speed_layer1, layer1.get_width(), layer1.get_height())
        x_layer2, y_layer2 = anpassung_der_ebenen(x_face_neu, y_face_neu, (x_center - layer2.get_width() // 2, y_center - layer2.get_height() // 2), speed_layer2, layer2.get_width(), layer2.get_height())
        x_layer3, y_layer3 = anpassung_der_ebenen(x_face_neu, y_face_neu, (x_center - layer3.get_width() // 2, y_center - layer3.get_height() // 2), speed_layer3, layer3.get_width(), layer3.get_height())
        x_layer4, y_layer4 = anpassung_der_ebenen(x_face_neu, y_face_neu, (x_center - layer4.get_width() // 2, y_center - layer4.get_height() // 2), speed_layer4, layer4.get_width(), layer4.get_height())

        # Create a black background
        window.fill(BLACK)

        # Draw the layers
        window.blit(layer1, (x_layer1, y_layer1))
        window.blit(layer2, (x_layer2, y_layer2)) 
        window.blit(layer3, (x_layer3, y_layer3))
        window.blit(layer4, (x_layer4, y_layer4))
        window.blit(layer0_frame, (0, 0))

        # Draw a small cross at the face coordinates if activated in asset manager
        if draw_face_position_crosshair == True:
            cross_color = (255, 0, 0)  # Red color
            cross_size = 10  # Size of the cross
            pygame.draw.line(window, cross_color, (x_face_neu - cross_size, y_face_neu), (x_face_neu + cross_size, y_face_neu), 2)
            pygame.draw.line(window, cross_color, (x_face_neu, y_face_neu - cross_size), (x_face_neu, y_face_neu + cross_size), 2)

        # Draw the curtains if they should be visible
        if curtains_visible:
            window.blit(layer0_leftCurtain, (0, 0))
            window.blit(layer0_rightCurtain, (width - layer0_rightCurtain.get_width(), 0))

        # Update the display
        pygame.display.flip()



# Clean up resources
camera.stop()
face_detector.close()
pygame.quit()
sys.exit()