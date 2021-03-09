import pygame
import sys

WINDOW_SIZE = (800, 800)

pygame.init()
window_surface = pygame.display.set_mode(WINDOW_SIZE)

is_game_over = False

clock = pygame.time.Clock()
while True:
    dt = clock.tick()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    window_surface.fill((0, 0, 0,))
    pygame.display.flip()
