import pygame


def draw_center_line():
    surface = pygame.Surface((5, 840))
    h_segment = 10
    pos_y0 = 0
    while pos_y0 + h_segment < 840:
        pygame.draw.rect(surface, (255, 255, 255), (0, pos_y0, 5, h_segment))
        pos_y0 += 2 * h_segment
    return surface


WINDOW_SIZE = (800, 840)

FPS = 60

GAME_LIMITS = (0, 800, 0, 840)

PADDLE_SPEED = 500

PADDLE_LEFT_RECT = (5, 400, 20, 80)
PADDLE_LEFT_INPUT = (pygame.K_z, pygame.K_s)

PADDLE_RIGHT_RECT = (775, 400, 20, 80)
PADDLE_RIGHT_INPUT = (pygame.K_UP, pygame.K_DOWN)

CENTER_LINE_SPRITE = draw_center_line()

BALL_RECT = (380, 420, 10, 10)
BALL_SPEED = (-400, 400)
