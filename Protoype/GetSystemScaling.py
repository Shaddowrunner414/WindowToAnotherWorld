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
