import pygame

def anpassung_der_ebenen(kopf_x, kopf_y, basisposition, abstand_ebene, layer_width, layer_height, invert_x=False, invert_y=False):
    # Get screen dimensions
    info = pygame.display.Info()
    width, height = info.current_w, info.current_h
    
    mittelpunkt_x, mittelpunkt_y = width // 2, height // 2

    verschiebung_x = (mittelpunkt_x - kopf_x) * (abstand_ebene / 300.0)
    verschiebung_y = (mittelpunkt_y - kopf_y) * (abstand_ebene / 300.0)

    if invert_y:
        verschiebung_y = -verschiebung_y

    neue_position_x = basisposition[0] + verschiebung_x
    neue_position_y = basisposition[1] + verschiebung_y

    neue_position_x = max(min(neue_position_x, 0), width - layer_width)
    neue_position_y = max(min(neue_position_y, 0), height - layer_height)

    return neue_position_x, neue_position_y