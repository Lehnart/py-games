import pygame
from pygame.constants import KEYDOWN

from tetris.tools.direction import Direction
from tetris.tools.rotation import Rotation


class Controller:
    PROCESSED_KEYS = [pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT]

    def __init__(self, tetris):
        self.tetris = tetris
        self._loop()

    def _loop(self):
        while not self.tetris.is_over():
            [self._process_event(event) for event in pygame.event.get()]

    def _process_event(self, event):

        # quit event
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # key pressed event
        if event.type == KEYDOWN and event.key in Controller.PROCESSED_KEYS:
            if event.key == pygame.K_DOWN:
                self.tetris.move(Direction.DOWN)

            elif event.key == pygame.K_RIGHT:
                self.tetris.move(Direction.RIGHT)

            elif event.key == pygame.K_LEFT:
                self.tetris.move(Direction.LEFT)

            elif event.key == pygame.K_UP:
                self.tetris.rotate(Rotation.CLOCKWISE)
