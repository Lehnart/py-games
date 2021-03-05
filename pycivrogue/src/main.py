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
        self.prod_count = 0

    def draw(self, surf: pygame.Surface):
        sprite = GNOME_SPRITE
        rect = sprite.get_rect()
        rect.x = self.position.x * BLOCK_SIZE[0]
        rect.y = self.position.y * BLOCK_SIZE[1]
        surf.blit(CHEST_SPRITE, rect)


class Goal(Enum):
    FOOD = 0,
    PROD = 1


class Gnome:
    MAX_VIEW_DISTANCE = 50
    UPDATE_GOAL = 100

    def __init__(self, position: Point, chest: Chest):
        self.chest: Chest = chest
        self.p: Point = position
        self.food_count = 0
        self.prod_count = 0
        self.goal = random.choice(list(Goal) )
        self.update_count = 0

    def update(self, gameMap: Map):
        b = None
        if self.goal == Goal.FOOD:
            self._goal_food(gameMap)
        elif self.goal == Goal.PROD:
            self._goal_prod(gameMap)

        self.update_count += 1
        if self.update_count >= Gnome.UPDATE_GOAL:
            self.goal = random.choice(list(Goal))
            self.update_count = 0

        return b

    def _goal_food(self, gameMap):
        if self.food_count == 0:
            b = self._find_block(gameMap, BlockType.BUSH)

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
                self.chest.food_count += 1
        return b

    def _goal_prod(self, gameMap):
        if self.prod_count == 0:
            b = self._find_block(gameMap, BlockType.TREE)

            if b is None:
                return

            if b.p != self.p:
                self._move(b)
            else:
                self.prod_count += 1
                b.type = BlockType.GRASS

        else:
            b = gameMap.block(self.chest.position)
            if b.p != self.p:
                self._move(b)
            else:
                self.prod_count -= 1
                self.chest.prod_count += 1
        return b

    def _move(self, b: Block):
        dx = b.p.x - self.p.x
        dy = b.p.y - self.p.y

        if abs(dx) > abs(dy):
            self.p.x += dx // abs(dx)
        else:
            self.p.y += dy // abs(dy)

    def _find_block(self, gameMap: Map, blockType: BlockType):
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
                if b.type == blockType:
                    return b

        return None

    def draw(self, surf: pygame.Surface):
        sprite = GNOME_SPRITE
        rect = sprite.get_rect()
        rect.x = self.p.x * BLOCK_SIZE[0]
        rect.y = self.p.y * BLOCK_SIZE[1]
        surf.blit(GNOME_SPRITE, rect)


class City:

    def __init__(self, p: Point, color: pygame.Color):
        self.p: Point = p
        self.color = color
        self.food_threshold = FOOD_THRESHOLD
        self.food_count = 0
        self.regions: List[Region] = []

    def update(self, gameMap: Map):
        self.food_count = sum(r.chest.food_count for r in self.regions)
        if self.food_threshold <= self.food_count:
            for r in self.regions:
                r.chest.food_count = 0
            self.food_threshold *= FOOD_MULTIPLICATOR
            self.add_gnome()

        for region in self.regions:
            for gnome in region.gnomes:
                gnome.update  (gameMap)

    def draw(self, surf: pygame.Surface):
        for region in self.regions:
            region.chest.draw(surf)

            for gnome in region.gnomes:
                gnome.draw(surf)

    def add_gnome(self):
        random.choice(self.regions).add_gnome()

    def add_region(self, region):
        region.set_owner(self)
        self.regions.append(region)


class Region:
    SIZE = 20

    def __init__(self, p: Point):
        self.p: Point = p
        self.owner = None
        self.chest = Chest(Point(self.p.x + Region.SIZE // 2, self.p.y + Region.SIZE // 2))
        self.gnomes: List[Gnome] = []
        self.color = pygame.Color(0, 0, 0)

    def draw(self, surf: pygame.Surface):
        rect = pygame.Rect(
            self.p.x * BLOCK_SIZE[0],
            self.p.y * BLOCK_SIZE[1],
            Region.SIZE * BLOCK_SIZE[0],
            Region.SIZE * BLOCK_SIZE[1]
        )
        pygame.draw.rect(surf, self.color, rect, 1)

    def add_gnome(self):
        p = Point(self.p.x + Region.SIZE // 2, self.p.y + Region.SIZE // 2)
        g = Gnome(p, self.chest)
        self.gnomes.append(g)

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

    def draw(self, surf: pygame.Surface):
        for x in range(len(self.region_grid)):
            for y in range(len(self.region_grid[x])):
                self.region_grid[x][y].draw(surf)

    def get(self, x: int, y: int):
        return self.region_grid[x][y]

    def set_owner(self, x: int, y: int, owner: City):
        self.region_grid[x][y].set_owner(owner)


pygame.init()
window_surface = pygame.display.set_mode(WINDOW_SIZE)

update_time_delay = 0
draw_time_delay = 0

is_game_over = False

gameMap = Map()
city = City(Point(49, 49), pygame.Color(0, 0, 255))
regions = Regions()
city.add_region(regions.get(2, 2))
city.add_region(regions.get(1, 2))
city.add_region(regions.get(2, 1))
city.add_region(regions.get(3, 2))
city.add_region(regions.get(2, 3))
city.add_gnome()

clock = pygame.time.Clock()
while True:
    dt = clock.tick()

    events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                city.update(gameMap)
        events.append(event)

    window_surface.fill((0, 0, 0,))
    gameMap.draw(window_surface)
    regions.draw(window_surface)
    city.draw(window_surface)

    pygame.display.flip()
