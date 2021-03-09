import pygame

from underhell.src.block import BLOCK_SIZE

GORLAB_SPRITE = pygame.transform.scale2x(pygame.image.load("res/gorlab.bmp"))

class Gorlab:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_dead = False

    def draw(self, surf: pygame.Surface):
        rect = GORLAB_SPRITE.get_rect()
        rect.x = self.x * BLOCK_SIZE
        rect.y = self.y * BLOCK_SIZE
        surf.blit(GORLAB_SPRITE, rect)