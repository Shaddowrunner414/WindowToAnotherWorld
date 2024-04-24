import pygame
import sys
import os
import numpy as np

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Pygame initialisieren
pygame.init()

# Fenstergröße festlegen
fenster_groesse = (1000, 800)
fenster = pygame.display.set_mode(fenster_groesse)

# Farben definieren
schwarz = (0, 0, 0)

# Bilder laden
hintergrund = pygame.image.load("Background.png").convert()
vordergrund = pygame.image.load("Foreground.png").convert_alpha()
zwischenebene = pygame.image.load("MiddleLayer.png").convert_alpha()  # Die dritte Ebene

# Anfangspositionen
x_hintergrund, y_hintergrund = 0, 0
x_vordergrund, y_vordergrund = 50, 100
x_zwischenebene, y_zwischenebene = 50, 100  # Startposition der Zwischenebene

# Monitorabstand zum Betrachter in Pixeln (angenommen)
monitor_distance = 300.0

# Ausgangs-Kopfposition
kopf_x = 500
kopf_y = 400

def anpassung_der_ebenen(kopf_x, kopf_y, basisposition, abstand_ebene):
    mittelpunkt_x, mittelpunkt_y = fenster_groesse[0] // 2, fenster_groesse[1] // 2
    verschiebung_x = (kopf_x - mittelpunkt_x) * (abstand_ebene / monitor_distance)
    verschiebung_y = (kopf_y - mittelpunkt_y) * (abstand_ebene / monitor_distance)
    neue_position_x = basisposition[0] + verschiebung_x
    neue_position_y = basisposition[1] + verschiebung_y
    return neue_position_x, neue_position_y

# Spiel-Schleife
running = True
while running:
    # Ereignisse prüfen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Tastendrücke erkennen und Kopfpositionen aktualisieren
    gedrueckte_tasten = pygame.key.get_pressed()
    if gedrueckte_tasten[pygame.K_UP]:
        kopf_y -= 10
    if gedrueckte_tasten[pygame.K_DOWN]:
       kopf_y += 10
    if gedrueckte_tasten[pygame.K_LEFT]:
        kopf_x -= 10
    if gedrueckte_tasten[pygame.K_RIGHT]:
        kopf_x += 10

    # Neue Position der Ebenen berechnen
    x_zwischenebene, y_zwischenebene = anpassung_der_ebenen(kopf_x, kopf_y, (50, 100), 150)
    x_vordergrund, y_vordergrund = anpassung_der_ebenen(kopf_x, kopf_y, (50, 100), 100)
    x_hintergrund, y_hintergrund = anpassung_der_ebenen(kopf_x, kopf_y, (50, 100), 300)
    
    # Hintergrund, Zwischenebene und Vordergrund zeichnen
    fenster.fill(schwarz)
    fenster.blit(hintergrund, (x_hintergrund, y_hintergrund))
    fenster.blit(zwischenebene, (x_zwischenebene, y_zwischenebene))
    fenster.blit(vordergrund, (x_vordergrund, y_vordergrund))
    
    # Fenster aktualisieren
    pygame.display.flip()

    # FPS begrenzen
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
