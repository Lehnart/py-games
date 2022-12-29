import os

import pygame.image

import colony_builder
from colony_builder.engine.components.sprite import Sprite

WINDOW_SIZE = (640, 480)

SPRITE_SIZE = 16

GROUND_LAYER = 0
ROAD_LAYER = 1
BUILDING_LAYER = 2
AGENT_LAYER = 3

res_path = os.path.dirname(colony_builder.settlers.__file__) + "/res"
GRASS_SURFACE = pygame.image.load(res_path + "/grass.png")
CASTLE_SURFACE = pygame.image.load(res_path + "/castle.png")
FLAG_SURFACE = pygame.image.load(res_path + "/flag.png")
ROAD_SURFACE = pygame.image.load(res_path + "/road.png")
HUMAN_SURFACE = pygame.image.load(res_path + "/human.png")

GROUND_ENTITIES = [
    Sprite(GRASS_SURFACE, (x, y), GROUND_LAYER)
    for y in range(0, WINDOW_SIZE[1], SPRITE_SIZE)
    for x in range(0, WINDOW_SIZE[0], SPRITE_SIZE)
]
CASTLE_ENTITY = Sprite(CASTLE_SURFACE, (640 // 16 * 8, 480 // 16 * 8), BUILDING_LAYER)