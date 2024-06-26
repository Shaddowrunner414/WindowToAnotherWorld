import pygame
import os

def load(image_name):
    script_dir = os.path.dirname(__file__)
    image = pygame.image.load(os.path.join(script_dir, image_name)).convert_alpha()
    return image

def load_and_scale(image_name, scale_factor=1.0):
    print("__")
    sf = scale_factor
    image = load(image_name)
    image_width = image.get_width()
    image_height = image.get_height()
    
    # Get screen dimensions
    info = pygame.display.Info()
    width, height = info.current_w, info.current_h
    
    scale_factor = height / image_height 
    scale_factor2 = width / image_width

    if image_width > image_height:
        scaled_image = pygame.transform.scale(image, (int(image.get_width() * scale_factor2 * sf), int(image.get_height() * scale_factor2 * sf)))
    else:
        scaled_image = pygame.transform.scale(image, (int(image.get_width() * scale_factor * sf), int(image.get_height() * scale_factor * sf)))

    image_width2 = scaled_image.get_width()
    image_height2 = scaled_image.get_height()
    print(f"{'W>H' if image_width > image_height else 'W<H'}, {scale_factor if image_width <= image_height else scale_factor2}, {image_width}, {image_width2}, {width}, {image_height}, {image_height2}, {height}, {image_name}")
    print("__")
    return scaled_image