from asset_manager import width, height, x_starter, y_starter, monitor_distance


# Initial position of the images
x_layer1, x_layer2, x_layer3, x_layer4 = x_starter, x_starter, x_starter, x_starter
y_layer1, y_layer2, y_layer3, y_layer4 = y_starter, y_starter, y_starter, y_starter


# Function to calculate the layer position depending on the distance of the layer to the monitor
def adjust_layers(head_x, head_y, base_position, layer_distance):
    
    #Calculate the center of the screen based on the globally defined variables 'width' and 'height'.
    center_x, center_y = width // 2, height // 2

    #Calculate the shift in x-direction based on the difference between head position and screen center.
    # 'layer_distance' is the depth distance from the base position to the monitor, 'monitor_distance' is the distance of the monitor to the viewer.
    shift_x = (head_x - center_x) * (layer_distance / monitor_distance)

    #Calculate the shift in y-direction similar to x-direction.
    shift_y = (head_y - center_y) * (layer_distance / monitor_distance)

    #Calculate the new x-position by adding the shift to the base x-position.
    new_position_x = base_position[0] + shift_x

    #Calculate the new y-position by adding the shift to the base y-position.
    new_position_y = base_position[1] + shift_y

    #Return the new x and y positions.
    return new_position_x, new_position_y