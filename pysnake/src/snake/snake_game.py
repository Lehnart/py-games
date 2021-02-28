import time
import json
from configparser import ConfigParser

import pygame

from snake.controller.controller import Controller

from snake.graphics.window import Window
from snake.ia.ia_builder import IABuilder
from snake.logic.board import Board
from snake.logic.rules import Rules
from snake.tools.timer import Timer


class SnakeGame:

    def __init__(self, n_games=1):

        config = ConfigParser()
        config.read("configuration.ini")
        self.config = config

        self.window = Window(config)

        update_period_ms = int(config["LOGIC"]["update_period_ms"])
        self.update_timer = Timer(update_period_ms, self.update, ( ))

        for _ in range(n_games):
            self.t_start = time.time()
            self.is_game_over = False
            self.board = Board(config)
            self.rules = Rules(self.board, self, config)
            self.controllers = [Controller(self, snake) for snake in self.rules.snakes]
            self.ias = [IABuilder.from_name(config["LOGIC"]["ia"], self, controller) for controller in self.controllers]
            self._loop()
            try:
                self.update_timer.timer.join()
            except:
                pass

    def game_over(self):
        self.is_game_over = True
        self._write_result_file()

    def is_over(self):
        return self.is_game_over

    def update(self):

        if self.is_over():
            return

        self.rules.update()

        self.window.draw(self.board)

        for ia in self.ias:
            if ia is not None:
                ia.next_move()

    def get_controllers(self):
        return self.controllers

    def get_board(self):
        return self.board

    def _loop(self):

        while not self.is_over():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    exit()

    def _write_result_file(self):
        result_dict = {}

        t_end = time.time()
        result_dict["t_end"] = t_end
        result_dict["t_start"] = self.t_start
        result_dict["move_count"] = self.rules.move_per_snake[0]
        result_dict["apple_eat_count"] = self.rules.apple_eat_per_snake[0]

        result_dict["config"] = {}
        for key in self.config["LOGIC"]:
            result_dict["config"][key] = self.config["LOGIC"][key]

        with open('results/result_' + str(t_end) + '.txt', 'w') as file:
            file.write(json.dumps(result_dict))
