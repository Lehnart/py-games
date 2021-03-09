import pygame

from underhell.src.block import BLOCK_SIZE

HERO_SPRITE = pygame.transform.scale2x(pygame.image.load("res/hero.bmp"))


class Hero:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surf: pygame.Surface):
        rect = HERO_SPRITE.get_rect()
        rect.x = self.x * BLOCK_SIZE
        rect.y = self.y * BLOCK_SIZE
        surf.blit(HERO_SPRITE, rect)
