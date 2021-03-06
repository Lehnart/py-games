import random
import sys

import pygame

from underhell.src.dungeon import Dungeon, TileType
from underhell.src.gorlab import Gorlab
from underhell.src.hero import Hero
from underhell.src.move import DOWN, RIGHT, LEFT, UP

WINDOW_SIZE = (800, 800)

pygame.init()
window_surface = pygame.display.set_mode(WINDOW_SIZE)

hero = Hero(0, 0)
gorlab = Gorlab(0, 0)
dungeon = Dungeon(100, 100)

while hero.x == gorlab.x and hero.y == gorlab.y:
    rooms = dungeon.rooms
    r = random.choice(rooms)
    hero.x, hero.y = r.rand()

    r = random.choice(rooms)
    gorlab.x, gorlab.y = r.rand()

is_game_over = False

clock = pygame.time.Clock()
while not is_game_over:
    dt = clock.tick()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                hero.move = DOWN
            if event.key == pygame.K_UP:
                hero.move = UP
            if event.key == pygame.K_LEFT:
                hero.move = LEFT
            if event.key == pygame.K_RIGHT:
                hero.move = RIGHT

    if hero.move is not None:
        x = hero.x + hero.move.dx
        y = hero.y + hero.move.dy
        if x == gorlab.x and y == gorlab.y:
            gorlab.hit_points -= 1
            hero.move = None

        elif dungeon.tiles[y][x].type == TileType.GROUND :
            hero.x = x
            hero.y = y

        hero.move = None

    if gorlab.is_dead():
        is_game_over = True

    window_surface.fill((0, 0, 0,))
    dungeon.draw(window_surface)
    hero.draw(window_surface)
    gorlab.draw(window_surface)
    pygame.display.flip()
