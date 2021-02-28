import random
import sys
from enum import Enum

import pygame

WINDOW_SIZE = (800, 800)
MAP_SIZE = (100, 100)
BLOCK_SIZE = (8, 8)

SPRITE_PATH = "res/"
BUSH_SPRITE = pygame.image.load(SPRITE_PATH + "bush.bmp")
ROCK_SPRITE = pygame.image.load(SPRITE_PATH + "rock.bmp")
TREE_SPRITE = pygame.image.load(SPRITE_PATH + "tree.bmp")
GRASS_SPRITE = pygame.image.load(SPRITE_PATH + "grass.bmp")
GNOME_SPRITE = pygame.image.load(SPRITE_PATH + "gnome.bmp")
CHEST_SPRITE = pygame.image.load(SPRITE_PATH + "chest.bmp")

class Point:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class BlockType(Enum):
    GRASS = 1,
    TREE = 2,
    ROCK = 3,
    BUSH = 4


BLOCK_TYPE_SPRITES = {
    BlockType.GRASS: GRASS_SPRITE,
    BlockType.TREE: TREE_SPRITE,
    BlockType.ROCK: ROCK_SPRITE,
    BlockType.BUSH: BUSH_SPRITE
}


class Block:

    def __init__(self, p: Point, type: BlockType):
        self.p = p
        self.type = type

    def draw(self, surf: pygame.Surface):
        sprite = BLOCK_TYPE_SPRITES[self.type]
        rect = sprite.get_rect()
        rect.x = self.p.x * BLOCK_SIZE[0]
        rect.y = self.p.y * BLOCK_SIZE[1]
        surf.blit(sprite, rect)


class Map:

    def __init__(self):
        self.grid = [[Block(Point(x, y), random.choice([t for t in BlockType])) for y in range(MAP_SIZE[1])] for x in
                     range(MAP_SIZE[0])]

    def draw(self, surf: pygame.Surface):
        for line in self.grid:
            for b in line:
                b.draw(surf)

class Chest:

    def __init__(self, position: Point):
        self.position = position

    def draw(self, surf: pygame.Surface):
        sprite = GNOME_SPRITE
        rect = sprite.get_rect()
        rect.x = self.position.x * BLOCK_SIZE[0]
        rect.y = self.position.y * BLOCK_SIZE[1]
        surf.blit(CHEST_SPRITE, rect)

class Gnome:

    def __init__(self, position: Point):
        self.position = position

    def draw(self, surf: pygame.Surface):
        sprite = GNOME_SPRITE
        rect = sprite.get_rect()
        rect.x = self.position.x * BLOCK_SIZE[0]
        rect.y = self.position.y * BLOCK_SIZE[1]
        surf.blit(GNOME_SPRITE, rect)

pygame.init()
window_surface = pygame.display.set_mode(WINDOW_SIZE)

update_time_delay = 0
draw_time_delay = 0

is_game_over = False

gameMap = Map()
gnome = Gnome(Point(MAP_SIZE[0]//2, MAP_SIZE[1]//2))
chest = Chest(Point(MAP_SIZE[0]//2+1, MAP_SIZE[1]//2))

clock = pygame.time.Clock()
while True:
    dt = clock.tick()

    events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        events.append(event)

    window_surface.fill((0, 0, 0,))
    gameMap.draw(window_surface)
    gnome.draw(window_surface)
    chest.draw(window_surface)
    pygame.display.flip()
