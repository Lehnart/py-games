import pygame

def get_sprite(pixel_x: int, pixel_y: int, width: int, height: int, color: pygame.Color) -> pygame.Surface:
    surface = SPRITE_SHEET.subsurface(pygame.Rect(pixel_x, pixel_y, width, height))
    surface: pygame.Surface = surface.convert()
    original_color = surface.map_rgb(pygame.Color(239, 239, 239))
    color = surface.map_rgb(color)
    pixel_array = pygame.PixelArray(surface)
    pixel_array.replace(original_color, color)
    surface = pixel_array.surface
    return surface

WINDOW_SIZE = (800, 840)

SPRITE_SHEET: pygame.Surface = pygame.image.load("res/sprites.bmp")

PLAYER_SURFACE = pygame.transform.scale2x(get_sprite(56, 200, 8, 8, pygame.Color(155, 71, 102)))
