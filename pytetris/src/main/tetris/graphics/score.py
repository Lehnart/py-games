import pygame


class Score:
    SCORE_RECT = pygame.Rect(0, 0, 300, 100)

    def __init__(self, window):
        self.window = window

    def draw(self, score):
        font = pygame.font.SysFont("comicsansms", 72)
        text = font.render(str(score), True, (255, 255, 255))
        self.window.blit(text, (0,0))
