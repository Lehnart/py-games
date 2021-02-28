import math

from snake.ia.simple.simple_ia import SimpleIA


class SimpleL2IA(SimpleIA):

    def distance_to_apple(self, block_positions, apple_position):
        apple_x, apple_y = apple_position
        return [math.sqrt((r[0] - apple_x) ** 2 + (r[1] - apple_y) ** 2) for r in block_positions]
