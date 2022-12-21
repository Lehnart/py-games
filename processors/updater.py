import sys

import pygame

from mesper import Processor


class Updater(Processor):

    def __init__(self):
        pass

    def process(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
