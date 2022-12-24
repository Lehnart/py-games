from typing import Dict, Callable

from colony_builder.engine.mesper import Component, World


class KeyboardInput(Component):

    def __init__(self, input_callbacks: Dict[int, Callable[[int, World], None]]):
        self.input_callbacks = input_callbacks

    def is_listening(self, key: int):
        return key in self.input_callbacks

    def call(self, key: int, ent: int, world: World):
        self.input_callbacks[key](ent, world)
