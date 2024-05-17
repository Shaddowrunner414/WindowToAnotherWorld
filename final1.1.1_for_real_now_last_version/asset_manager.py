import os
import pygame

class AssetManager:

    script_dir = 0
    width = 0
    height = 0
    

    #Define the initial position of the images
    x_starter = width * 0.2
    y_starter = height * 0.2
    # Last known position
    lastknown_x, lastknown_y = x_starter, y_starter
    # Monitor distance to the viewer in pixels (assumed)
    monitor_distance = 300.0
    # Maxmum Distance before the background removal starts
    background_removal_threshold = 1.5 # in meters


    def init(self):
        # Read Screen Resolution
        pygame.init()
        info = pygame.display.Info()
        width, height = info.current_w, info.current_h
        print("Bildschirmauflösung Breite: ", width, "Bildschirmauflösung Höhe: ",  height)      




        # Path of the current script
        script_dir = os.path.dirname(__file__)

        return width, height

    # Function to load the images with relative paths
    def load(image_name):
        image = pygame.image.load(os.path.join(AssetManager.script_dir, image_name)).convert_alpha()
        return image

    # Function to scale the images and adjust them to the screen resolution
    def load_and_scale(image_name, scale_factor=1.0):
        sf = scale_factor
        image = AssetManager.load(image_name)
        image_width = image.get_width()
        image_height = image.get_height()
        scale_factor = AssetManager.height / image_height 
        scale_factor2 = AssetManager.width / image_width

        # Automatic scaling
        if image_width > image_height:
            scaled_image = pygame.transform.scale(image, (image.get_width() * scale_factor2 * sf, image.get_height() * scale_factor2 * sf))
            image_width2 = scaled_image.get_width()
            image_height2 = scaled_image.get_height()
            print("W>H", scale_factor2, image_width, image_width2, AssetManager.width, image_height, image_height2, AssetManager.height, image_name)
        elif image_width <= image_height:
            scaled_image = pygame.transform.scale(image, (image.get_width() * scale_factor * sf, image.get_height() * scale_factor * sf))
            image_width2 = scaled_image.get_width()
            image_height2 = scaled_image.get_height()
            print("W<H", scale_factor, image_width, image_width2, AssetManager.width, image_height, image_height2, AssetManager.height, image_name)

        return scaled_image

    # Load images
    # Layer index counts up from the background
    #layer1 = load_and_scale("AIBackground.png")
    #layer2 = load_and_scale("AIMiddleground.png", scale_factor=1.0)
    #layer3 = load_and_scale("AIForeground.png", scale_factor=1.0)
    #layer4 = load_and_scale("AIWindow.png", scale_factor=1.0)