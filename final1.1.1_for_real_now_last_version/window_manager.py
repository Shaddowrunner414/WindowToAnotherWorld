import cv2
import pygame
import numpy as np
from asset_manager import AssetManager


class WindowManager:
    def __init__(self, window_name):
        self.window_name = window_name
        self.screen = None

    def show_frame(self, frame, coords=None):
        if not self.screen:
            self.screen = pygame.display.set_mode(AssetManager.init(self), pygame.SCALED)

        # Convert BGR (OpenCV) to RGB (pygame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Transpose the frame to fix the rotation
        frame = np.transpose(frame, (1, 0, 2))

        surface = pygame.surfarray.make_surface(frame)
        if coords:
            x, y = coords
            pygame.draw.line(surface, (0, 255, 0), (x - 10, y), (x + 10, y))
            pygame.draw.line(surface, (0, 255, 0), (x, y - 10), (x, y + 10))
        self.screen.blit(surface, (0, 0))
        pygame.display.flip()

    def close_window(self):
        pygame.quit()

    # insert auto scaling here somewhere



#class WindowManager:
#    def __init__(self, window_name):
#        self.window_name = window_name

#    def show_frame(self, frame, coords=None):
#        if coords:
#            x, y = coords
#            cv2.drawMarker(frame, (x, y), color=(0, 255, 0), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)
#        cv2.imshow(self.window_name, frame)

#    def close_window(self):
#        cv2.destroyWindow(self.window_name)