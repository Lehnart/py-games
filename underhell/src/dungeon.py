import random
from enum import Enum
from random import randint

import pygame

from underhell.src import block

ROOM_SIZE_MIN = 6
ROOM_SIZE_MAX = 15
ROOM_COUNT_MIN = 4
ROOM_COUNT_MAX = 6

GROUND_SPRITE = pygame.image.load("res/ground.bmp")
WALL_SPRITE = pygame.image.load("res/wall.bmp")


class TileType(Enum):
    VOID = 0,
    GROUND = 1,
    WALL = 2


SPRITES = {TileType.VOID: None, TileType.GROUND: GROUND_SPRITE, TileType.WALL: WALL_SPRITE}


class Tile:

    def __init__(self, x: int, y: int, ttype: TileType):
        self.x = x
        self.y = y
        self.type = ttype
        self.sprite = SPRITES[ttype]

    def _rect(self):
        s = block.SIZE
        return pygame.Rect(self.x * s, self.y * s, s, s)

    def draw(self, surf: pygame.Surface):
        if self.sprite is not None:
            surf.blit(self.sprite, self._rect())


class Room:

    def __init__(self, x0: int, y0: int, w: int, h: int):
        self.x0 = x0
        self.y0 = y0
        self.w = w
        self.h = h

    def rand_x(self):
        return random.randint(self.x0 + 1, self.x0 + self.w - 2)

    def rand_y(self):
        return random.randint(self.y0 + 1, self.y0 + self.h - 2)

    def rand(self):
        return self.rand_x(), self.rand_y()


class Dungeon:

    def __init__(self, block_width: int, block_height: int):
        self.w = block_width
        self.h = block_height

        self.tiles = [[Tile(x, y, TileType.VOID) for x in range(self.w)] for y in range(self.h)]

        self.rooms = self._generate_rooms()
        self._connect_rooms(self.rooms)

    def draw(self, surf: pygame.Surface):
        for y in range(self.h):
            for x in range(self.w):
                tile = self.tiles[y][x]
                if tile.type == TileType.VOID:
                    pass
                else:
                    tile.draw(surf)

    def _generate_rooms(self):
        n_room = randint(ROOM_COUNT_MIN, ROOM_COUNT_MAX)
        return [self._generate_room() for _ in range(n_room)]

    def _generate_room(self):

        while True:

            w, h = randint(ROOM_SIZE_MIN, ROOM_SIZE_MAX), randint(ROOM_SIZE_MIN, ROOM_SIZE_MAX)
            x_max, y_max = self.w - w - 1, self.h - h - 1
            x0, y0 = randint(1, x_max), randint(1, y_max)

            is_empty = True
            for y in range(y0, y0 + h):

                if not is_empty:
                    break

                for x in range(x0, x0 + w):
                    if self.tiles[y][x].type != TileType.VOID:
                        is_empty = False
                        break

            if not is_empty:
                continue

            for x in range(x0, x0 + w):
                self.tiles[y0][x] = Tile(x, y0, TileType.WALL)
                self.tiles[y0 + h - 1][x] = Tile(x, y0 + h - 1, TileType.WALL)

            for y in range(y0, y0 + h):
                self.tiles[y][x0] = Tile(x0, y, TileType.WALL)
                self.tiles[y][x0 + w - 1] = Tile(x0 + w - 1, y, TileType.WALL)

            for x in range(x0 + 1, x0 + w - 1):
                for y in range(y0 + 1, y0 + h - 1):
                    self.tiles[y][x] = Tile(x, y, TileType.GROUND)

            return Room(x0, y0, w, h)

    def _connect_rooms(self, rooms):
        connected_rooms = []
        not_connected_rooms = list(rooms)
        while len(not_connected_rooms) != 0:
            room_index = random.randint(0, len(not_connected_rooms) - 1)
            not_connected_room = not_connected_rooms[room_index]

            if len(connected_rooms) == 0:
                connected_rooms.append(not_connected_room)
                not_connected_rooms.pop(room_index)
                continue

            connected_room = random.choice(connected_rooms)
            if self._connect_two_rooms(connected_room, not_connected_room):
                connected_rooms.append(not_connected_room)
                not_connected_rooms.pop(room_index)

    def _connect_two_rooms(self, room1: Room, room2: Room):
        x1, y1 = room1.rand()
        x2, y2 = room2.rand()
        x_min, y_min = min(x1, x2), min(y1, y2)
        x_max, y_max = max(x1, x2), max(y1, y2)

        for i in range(x_min, x_max + 1):
            self.tiles[y1][i] = Tile(i, y1, TileType.GROUND)

        for i in range(y_min, y_max + 1):
            self.tiles[i][x2] = Tile(x2, i, TileType.GROUND)

        return True
