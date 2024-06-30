import pygame

# Image Variables
image_layer0_frame = "AIWindow.png"
image_layer0_left_curtain = "leftExtendedCurtainAWithImpressum.png"
image_layer0_right_curtain = "rightExtendedCurtainA.png"
image_layer1 = "CitySky.png"
image_layer2 = "CityBackground.png"
image_layer3 = "CityMidground.png"
image_layer4 = "CityForeground.png"

# Individual Layer Speed Variables (Geschwindigkeitsfactor: größere Zahl -> schneller)
speed_layer1 = 340
speed_layer2 = 260
speed_layer3 = 180
speed_layer4 = 100

# Genral Speed Modifier
# Increase this value for less sensitive movement, decrease for more sensitive
general_speed_modifier = 400

# Scale Variables (Zoomfactor: größere Zahl -> mehr ran gezoomt)
scale_layer0 = 1
scale_layer1 = 1
scale_layer2 = 1.45
scale_layer3 = 1.3
scale_layer4 = 1.1

# Monitor distance to viewer in pixels
monitor_distance = 300.0

# Colors
BLACK = (0, 0, 0)

# Other constants
FACE_DETECTION_THRESHOLD = 2  # seconds
QUADRANT_DURATION_THRESHOLD = 4  # seconds
CROSS_SIZE = 10
CROSS_COLOR = (255, 0, 0)  # Red color

# Camera settings
CAMERA_DEVICE_ID = 0

# Window settings
WINDOW_TITLE = "Parallax Window"

# When using the Realsense Camera, everything that's farther away from the camera then this variable (in meters) get's cut away
background_removal_threshold = 1.0

# Get screen dimensions
pygame.init()
info = pygame.display.Info()
width, height = info.current_w, info.current_h
pygame.quit()