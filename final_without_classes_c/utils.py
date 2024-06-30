import pygame
import os
import ctypes
from asset_manager import width, height


# Load an image file and convert it to a Pygame surface with alpha channel support.
def load(image_name):

    # Get the absolute path of the directory containing this script
    script_dir = os.path.dirname(__file__)

    # Construct the full path to the image file
    image_path = os.path.join(script_dir, image_name)

    # Load the image and convert it to a surface with per-pixel alpha
    # This allows for transparency in PNG images
    image = pygame.image.load(image_path).convert_alpha()

    return image


# Load an image, scale it based on the screen size and a given scale factor.
def load_and_scale(image_name, scale_factor=1.0):

    # Load the original image
    image = load(image_name)
    image_width = image.get_width()
    image_height = image.get_height()
    
    # Store the original scale factor for possible later use
    additional_scale_factor = scale_factor 

    # Calculate scaling factors based on screen dimensions
    # This ensures the image fits the screen height or width
    scale_factor_portrait = height / image_height 
    scale_factor_landsacpe = width / image_width


    # Scale the image based on its orientation (landscape or portrait)
    # and apply the additional scale factor
    if image_width > image_height:
        # For landscape images, scale based on width
        scaled_image = pygame.transform.scale(image, (
            int(image.get_width() * scale_factor_landsacpe * additional_scale_factor), 
            int(image.get_height() * scale_factor_landsacpe * additional_scale_factor)
        ))
    else:
        # For portrait images, scale based on height
        scaled_image = pygame.transform.scale(image, (
            int(image.get_width() * scale_factor_portrait * additional_scale_factor), 
            int(image.get_height() * scale_factor_portrait * additional_scale_factor)
        ))


    # Get the dimensions of the scaled image for debugging
    image_width2 = scaled_image.get_width()
    image_height2 = scaled_image.get_height()
    
    # Print debugging information
    print(f"{'W>H' if image_width > image_height else 'W<H'}, "
          f"{scale_factor_portrait if image_width <= image_height else scale_factor_landsacpe}, "
          f"{image_width}, {image_width2}, {width}, "
          f"{image_height}, {image_height2}, {height}, {image_name}")
    return scaled_image



# Attempt to get the system DPI scaling on Windows
def get_system_scaling():
    
    try:
        # Load the user32 DLL, which contains Windows API functions
        user32 = ctypes.windll.user32

        # Get the system DPI
        # This function returns the DPI for the system, which is used for scaling
        h_scale = user32.GetDpiForSystem()
        v_scale = user32.GetDpiForSystem()

        return h_scale, v_scale
    except Exception as e:
        # If any error occurs (e.g., not on Windows), print the error and return None values
        print("Error getting system scaling:", str(e))
        return None, None