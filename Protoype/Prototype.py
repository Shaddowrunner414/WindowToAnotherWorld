import pygame
import sys

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
x_vordergrund, y_vordergrund = 50, 100
x_zwischenebene, y_zwischenebene = 50, 100  # Startposition der Zwischenebene

# Bewegungsgeschwindigkeiten
geschwindigkeit_vordergrund = 5
geschwindigkeit_zwischenebene = geschwindigkeit_vordergrund / 2  # Halbe Geschwindigkeit

# Spiel-Schleife
running = True
while running:
    # Ereignisse prüfen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Tastendrücke erkennen und Positionen aktualisieren
    gedrueckte_tasten = pygame.key.get_pressed()
    if gedrueckte_tasten[pygame.K_UP]:
        y_vordergrund -= geschwindigkeit_vordergrund
        y_zwischenebene -= geschwindigkeit_zwischenebene
    if gedrueckte_tasten[pygame.K_DOWN]:
        y_vordergrund += geschwindigkeit_vordergrund
        y_zwischenebene += geschwindigkeit_zwischenebene
    if gedrueckte_tasten[pygame.K_LEFT]:
        x_vordergrund -= geschwindigkeit_vordergrund
        x_zwischenebene -= geschwindigkeit_zwischenebene
    if gedrueckte_tasten[pygame.K_RIGHT]:
        x_vordergrund += geschwindigkeit_vordergrund
        x_zwischenebene += geschwindigkeit_zwischenebene
    
    # Hintergrund, Zwischenebene und Vordergrund zeichnen
    fenster.fill(schwarz)
    fenster.blit(hintergrund, (0, 0))
    fenster.blit(zwischenebene, (x_zwischenebene, y_zwischenebene))
    fenster.blit(vordergrund, (x_vordergrund, y_vordergrund))
    
    # Fenster aktualisieren
    pygame.display.flip()

    # FPS begrenzen
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
