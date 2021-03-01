import random
import sys
from enum import Enum
from typing import List

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

FOOD_THRESHOLD = 1
FOOD_MULTIPLICATOR = 1.1


class Point:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


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
        self.p: Point = p
        self.type: BlockType = type

    def draw(self, surf: pygame.Surface):
        sprite = BLOCK_TYPE_SPRITES[self.type]
        rect = sprite.get_rect()
        rect.x = self.p.x * BLOCK_SIZE[0]
        rect.y = self.p.y * BLOCK_SIZE[1]
        surf.blit(sprite, rect)

    def rect(self):
        bsize = BLOCK_SIZE[0]
        return pygame.Rect(self.p.x * bsize, self.p.y * bsize, bsize, bsize)


class Map:

    def __init__(self):
        self.grid = [[Block(Point(x, y), random.choice([t for t in BlockType])) for y in range(MAP_SIZE[1])] for x in
                     range(MAP_SIZE[0])]

    def draw(self, surf: pygame.Surface):
        for line in self.grid:
            for b in line:
                b.draw(surf)

    def block(self, pos: Point):
        return self.grid[pos.x][pos.y]


class Chest:

    def __init__(self, position: Point):
        self.position = position
        self.food_count = 0

    def draw(self, surf: pygame.Surface):
        sprite = GNOME_SPRITE
        rect = sprite.get_rect()
        rect.x = self.position.x * BLOCK_SIZE[0]
        rect.y = self.position.y * BLOCK_SIZE[1]
        surf.blit(CHEST_SPRITE, rect)


class Gnome:
    MAX_VIEW_DISTANCE = 50

    def __init__(self, position: Point, chest: Chest):
        self.chest: Chest = chest
        self.p: Point = position
        self.food_count = 0

    def update(self, gameMap: Map, gnomes: List):
        b = None
        if self.food_count == 0:
            b = self._find_bush(gameMap)

            if b is None:
                return

            if b.p != self.p:
                self._move(b)
            else:
                self.food_count += 1
                b.type = BlockType.GRASS

        else:
            b = gameMap.block(self.chest.position)
            if b.p != self.p:
                self._move(b)
            else:
                self.food_count -= 1
                chest.food_count += 1

        return b

    def _move(self, b: Block):
        dx = b.p.x - self.p.x
        dy = b.p.y - self.p.y

        if abs(dx) > abs(dy):
            self.p.x += dx // abs(dx)
        else:
            self.p.y += dy // abs(dy)

    def _find_bush(self, gameMap: Map):
        for d in range(0, Gnome.MAX_VIEW_DISTANCE + 1):
            x0 = self.p.x
            y0 = self.p.y

            points = []
            for dx in range(-d, d + 1):
                dy = d - (abs(dx))
                points.append((x0 + dx, y0 + dy))
                if dy != 0: points.append((x0 + dx, y0 - dy))

            random.shuffle(points)
            for p in points:
                x, y = p
                b = gameMap.grid[x][y]
                if b.type == BlockType.BUSH:
                    return b

        return None

    def draw(self, surf: pygame.Surface):
        sprite = GNOME_SPRITE
        rect = sprite.get_rect()
        rect.x = self.p.x * BLOCK_SIZE[0]
        rect.y = self.p.y * BLOCK_SIZE[1]
        surf.blit(GNOME_SPRITE, rect)


class Civilization:

    def __init__(self, chest: Chest):
        self.chest: Chest = chest
        self.food_threshold = FOOD_THRESHOLD

    def update(self):
        print(self.chest.food_count)
        if self.food_threshold <= self.chest.food_count:
            self.chest.food_count -= self.food_threshold
            self.food_threshold *= FOOD_MULTIPLICATOR

            return Gnome(Point(self.chest.position.x, self.chest.position.y), self.chest)


class City:

    def __init__(self, p: Point, civ: Civilization, color: pygame.Color):
        self.p: Point = p
        self.civ = civ
        self.color = color


class Region:
    SIZE = 20

    def __init__(self, p: Point):
        self.p: Point = p
        self.owner = None
        self.color = pygame.Color(0, 0, 0)

    def draw(self, surf: pygame.Surface):
        rect = pygame.Rect(
            self.p.x * BLOCK_SIZE[0],
            self.p.y * BLOCK_SIZE[1],
            Region.SIZE * BLOCK_SIZE[0],
            Region.SIZE * BLOCK_SIZE[1]
        )
        pygame.draw.rect(surf, self.color, rect, 1)

    def set_owner(self, city: City):
        self.owner = city
        self.color = city.color

class Regions:
    def __init__(self):
        self.region_grid = []
        for x in range(MAP_SIZE[0] // Region.SIZE):
            self.region_grid.append([])
            for y in range(MAP_SIZE[1] // Region.SIZE):
                self.region_grid[-1].append(Region(Point(x * Region.SIZE, y * Region.SIZE)))

    def draw(self, surf:pygame.Surface):
        for x in range(len(self.region_grid)):
            for y in range(len(self.region_grid[x])):
                self.region_grid[x][y].draw(surf)

    def set_owner(self, x:int, y:int, owner:City):
        self.region_grid[x][y].set_owner(owner)


pygame.init()
window_surface = pygame.display.set_mode(WINDOW_SIZE)

update_time_delay = 0
draw_time_delay = 0

is_game_over = False

gameMap = Map()
chest = Chest(Point(MAP_SIZE[0] // 2 + 1, MAP_SIZE[1] // 2))
civ = Civilization(chest)
city = City(Point(49, 49), civ, pygame.Color(0, 0, 255))
regions = Regions()
regions.set_owner(2,2,city)
regions.set_owner(1,2,city)
regions.set_owner(2,1,city)
regions.set_owner(3,2,city)
regions.set_owner(2,3,city)

gameMap.block(chest.position).type = BlockType.GRASS
gnomes = [Gnome(Point(MAP_SIZE[0] // 2, MAP_SIZE[1] // 2), chest)]

clock = pygame.time.Clock()
while True:
    dt = clock.tick()

    events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                [gnome.update(gameMap, gnomes) for gnome in gnomes]
                g = civ.update()
                if g is not None:
                    gnomes.append(g)
        events.append(event)

    window_surface.fill((0, 0, 0,))
    gameMap.draw(window_surface)
    regions.draw(window_surface)

    chest.draw(window_surface)
    [gnome.draw(window_surface) for gnome in gnomes]

    pygame.display.flip()
