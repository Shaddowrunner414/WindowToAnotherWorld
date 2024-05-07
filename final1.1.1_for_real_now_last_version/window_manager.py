import cv2

class WindowManager:
    def __init__(self, window_name):
        self.window_name = window_name

    def show_frame(self, frame, coords=None):
        if coords:
            x, y = coords
            cv2.drawMarker(frame, (x, y), color=(0, 255, 0), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)
        cv2.imshow(self.window_name, frame)

    def close_window(self):
        cv2.destroyWindow(self.window_name)