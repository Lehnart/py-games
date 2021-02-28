import pygame


class Controller:

    def __init__(self, snake_game, snake):
        self.rules = snake_game.rules
        self.snake = snake

    def move(self, direction):
        self.rules.move(direction, self.snake)
