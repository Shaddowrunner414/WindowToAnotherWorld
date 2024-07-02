# does everything needed to have the images as layers available, just separated into this file for easier access
from utils import load_and_scale
from asset_manager import *
from main import x_center, y_center, window, x_face_neu, y_face_neu, curtains_visible, width
from layer_adjustment import anpassung_der_ebenen


def prepare_layers(self):
    # Load images
    layer1 = load_and_scale(image_layer1, scale_factor=scale_layer1)
    layer2 = load_and_scale(image_layer2, scale_factor=scale_layer2)
    layer3 = load_and_scale(image_layer3, scale_factor=scale_layer3)
    layer4 = load_and_scale(image_layer4, scale_factor=scale_layer4)
    layer0_frame = load_and_scale("AIWindow.png")
    layer0_leftCurtain = load_and_scale("leftExtendedCurtainAWithImpressum.png")
    layer0_rightCurtain = load_and_scale("rightExtendedCurtainA.png")

    # Initial positions (centered)
    x_layer1, y_layer1 = x_center - layer1.get_width() // 2, y_center - layer1.get_height() // 2
    x_layer2, y_layer2 = x_center - layer2.get_width() // 2, y_center - layer2.get_height() // 2
    x_layer3, y_layer3 = x_center - layer3.get_width() // 2, y_center - layer3.get_height() // 2
    x_layer4, y_layer4 = x_center - layer4.get_width() // 2, y_center - layer4.get_height() // 2


def move_and_draw_layers():
    x_layer1, y_layer1 = anpassung_der_ebenen(x_face_neu, y_face_neu, (x_center - layer1.get_width() // 2, y_center - layer1.get_height() // 2), speed_layer1, layer1.get_width(), layer1.get_height(), invert_x=True, invert_y=True)
    x_layer2, y_layer2 = anpassung_der_ebenen(x_face_neu, y_face_neu, (x_center - layer2.get_width() // 2, y_center - layer2.get_height() // 2), speed_layer2, layer2.get_width(), layer2.get_height(), invert_x=True, invert_y=True)
    x_layer3, y_layer3 = anpassung_der_ebenen(x_face_neu, y_face_neu, (x_center - layer3.get_width() // 2, y_center - layer3.get_height() // 2), speed_layer3, layer3.get_width(), layer3.get_height(), invert_x=True, invert_y=True)
    x_layer4, y_layer4 = anpassung_der_ebenen(x_face_neu, y_face_neu, (x_center - layer4.get_width() // 2, y_center - layer4.get_height() // 2), speed_layer4, layer4.get_width(), layer4.get_height(), invert_x=True, invert_y=True)

    window.fill(BLACK)
    window.blit(layer1, (x_layer1, y_layer1))
    window.blit(layer2, (x_layer2, y_layer2)) 
    window.blit(layer3, (x_layer3, y_layer3))
    window.blit(layer4, (x_layer4, y_layer4))
    window.blit(layer0_frame, (0, 0))



def curtain_drawer():
    if curtains_visible:
        window.blit(layer0_leftCurtain, (0, 0))
        window.blit(layer0_rightCurtain, (width - layer0_rightCurtain.get_width(), 0))