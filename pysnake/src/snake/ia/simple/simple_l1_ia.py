from snake.ia.simple.simple_ia import SimpleIA


class SimpleL1IA(SimpleIA):

    def distance_to_apple(self, block_positions, apple_position):
        apple_x, apple_y = apple_position
        return [abs(r[0] - apple_x) + abs(r[1] - apple_y) for r in block_positions]
