import pygame

from underhell.src import block

SPRITE = pygame.image.load("res/gorlab.bmp")
if block.SIZE == 16:
    SPRITE = pygame.transform.scale2x(SPRITE)
HIT_POINTS_MAX = 5


class Gorlab:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hit_points = HIT_POINTS_MAX

    def draw(self, surf: pygame.Surface):
        rect = SPRITE.get_rect()
        rect.x = self.x * block.SIZE
        rect.y = self.y * block.SIZE
        surf.blit(SPRITE, rect)

    def is_dead(self):
        return self.hit_points == 0
