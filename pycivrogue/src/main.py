import pygame
import sys

WINDOW_SIZE = (800,800)

pygame.init()
window_surface = pygame.display.set_mode(WINDOW_SIZE)

update_time_delay = 0
draw_time_delay = 0

is_game_over = False

clock = pygame.time.Clock()

while True:
    dt = clock.tick()

    events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        events.append(event)

    window_surface.fill((0, 0, 0,))
    pygame.display.flip()