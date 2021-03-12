import pygame

from underhell.src.block import SIZE

SPRITE = pygame.transform.scale2x(pygame.image.load("res/gorlab.bmp"))

HIT_POINTS_MAX = 5

class Gorlab:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hit_points = HIT_POINTS_MAX

    def draw(self, surf: pygame.Surface):
        rect = SPRITE.get_rect()
        rect.x = self.x * SIZE
        rect.y = self.y * SIZE
        surf.blit(SPRITE, rect)

    def is_dead(self):
        return self.hit_points == 0