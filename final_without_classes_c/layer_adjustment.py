from asset_manager import general_speed_modifier, width, height

# Initialze Ballon offset
ballon_speed = 0

def ballon_speed_up():
    global ballon_speed
    ballon_speed += 1
    return ballon_speed

def anpassung_der_ebenen(kopf_x, kopf_y, basisposition, abstand_ebene, layer_width, layer_height, layer_name=None):

    # Calculate the center of the screen
    mittelpunkt_x, mittelpunkt_y = width // 2, height // 2

    # Calculate the displacement from a centerd position based on the head position relative to the screen center
    verschiebung_x = (mittelpunkt_x - kopf_x) * (abstand_ebene / general_speed_modifier)
    verschiebung_y = (mittelpunkt_y - kopf_y) * (abstand_ebene / general_speed_modifier)

    # Apply the displacement to the the starting position
    neue_position_x = basisposition[0] + verschiebung_x
    neue_position_y = basisposition[1] + verschiebung_y

    # Ensure the new position doesn't move the layer off-screen
    # This clamps the values to keep the layer within the screen boundaries
    neue_position_x = max(min(neue_position_x, 0), width - layer_width)
    neue_position_y = max(min(neue_position_y, 0), height - layer_height)

    if layer_name:
        # moves the ballon
        neue_position_y -= ballon_speed

    return neue_position_x, neue_position_y