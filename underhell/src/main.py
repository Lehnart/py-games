import pygame
import sys

from underhell.src.gorlab import Gorlab
from underhell.src.hero import Hero

WINDOW_SIZE = (800, 800)

pygame.init()
window_surface = pygame.display.set_mode(WINDOW_SIZE)

hero = Hero(1,1)
gorlab = Gorlab(20,20)

is_game_over = False

clock = pygame.time.Clock()
while True:
    dt = clock.tick()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                hero.y += 1
            if event.key == pygame.K_UP:
                hero.y -= 1
            if event.key == pygame.K_LEFT:
                hero.x -= 1
            if event.key == pygame.K_RIGHT:
                hero.x += 1

    window_surface.fill((0, 0, 0,))
    hero.draw(window_surface)
    gorlab.draw(window_surface)
    pygame.display.flip()
