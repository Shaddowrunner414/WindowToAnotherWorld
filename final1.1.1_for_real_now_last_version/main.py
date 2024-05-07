import cv2
from camera_manager import CameraManager
from window_manager import WindowManager
from face_detector import FaceDetector
from image_mover import adjust_layers, x_starter, y_starter, new_position_x, new_position_y

def main():
    camera_manager = CameraManager("Intel RealSense D435")
    window_manager_original = WindowManager("Original")
    window_manager_foreground = WindowManager("Foreground")
    face_detector = FaceDetector()

    camera_manager.start()

    try:
        while True:
            original_frame, foreground_frame = camera_manager.get_frame()
            coords = face_detector.process_frame(foreground_frame)
            if coords:
                print(f"Face detected at {coords}")
            
            # Last known position
            lastknown_x, lastknown_y = x_starter, y_starter

            # Move layers
            #x_layer1, y_layer1 = adjust_layers(new_position_x, new_position_y, (x_starter, y_starter), 4000)
            #x_layer2, y_layer2 = adjust_layers(new_position_x, new_position_y, (x_starter, y_starter), 3000)
            #x_layer3, y_layer3 = adjust_layers(new_position_x, new_position_y, (x_starter, y_starter), 800)
            #x_layer4, y_layer4 = adjust_layers(new_position_x, new_position_y, (x_starter, y_starter), -400)

                
            window_manager_original.show_frame(original_frame)
            window_manager_foreground.show_frame(foreground_frame, coords)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        camera_manager.stop()
        window_manager_original.close_window()
        window_manager_foreground.close_window()

if __name__ == "__main__":
    main()