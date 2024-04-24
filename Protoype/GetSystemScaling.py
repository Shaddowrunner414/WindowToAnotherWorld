import ctypes

#SystemSkalierung ausgeben
scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
print(scaleFactor)

#Bildschirmskalierung von pygame ausgeben(Standartmäßig 96 dpi)
def get_system_scaling():
    try:
        user32 = ctypes.windll.user32
        # Horizontale Skalierungsfaktor abrufen
        h_scale = user32.GetDpiForSystem()
        # Vertikale Skalierungsfaktor abrufen
        v_scale = user32.GetDpiForSystem()
        return h_scale, v_scale
    except Exception as e:
        print("Fehler beim Abrufen der Systemskalierung:", str(e))
        return None, None

# Systemskalierung auslesen
horizontal_scale, vertical_scale = get_system_scaling()
if horizontal_scale is not None and vertical_scale is not None:
    print("Horizontale Systemskalierung:", horizontal_scale)
    print("Vertikale Systemskalierung:", vertical_scale)


layer1 = load_and_scale("background.png")
layer2 = load_and_scale("hill.png", scale_factor=1.0)
layer3 = load_and_scale("tree.png", scale_factor=1.0)
layer4 = load_and_scale("fence.png", scale_factor=1.0)

x_layer1, x_layer2, x_layer3, x_layer4 = x_starter, x_starter, x_starter, x_starter
y_layer1, y_layer2, y_layer3, y_layer4 = y_starter, y_starter, y_starter, y_starter

        x_layer2 = x_neu
        y_layer2 = y_neu
        x_layer3 = x_neu
        y_layer3 = y_neu
        x_layer4 = x_neu
        y_layer4 = y_neu


 window.fill(black)
        window.blit(layer1, (0, 0))
        window.blit(layer2, (x_layer2, y_layer2)) 
        window.blit(layer3, (x_layer3, y_layer3))
        window.blit(layer4, (x_layer4, y_layer4))
