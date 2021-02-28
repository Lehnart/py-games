from enum import Enum


class BlockType(Enum):
    WALL = 1
    APPLE = 2
    SNAKE = 3
    SNAKE_HEAD = 4

class Block:
    """ A block with a type"""
    
    def __init__(self, p_type):
        self.type = p_type

    def get_type(self):
        return self.type
