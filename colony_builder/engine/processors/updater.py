import sys

import pygame

from colony_builder.engine.mesper import Processor


class Updater(Processor):

    def process(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
