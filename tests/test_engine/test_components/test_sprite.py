import pygame

from colony_builder.engine.components.sprite import Sprite


class TestSprite:

    def test_constructor(self):
        pygame.init()
        surf = pygame.Surface((10, 10))
        sprite = Sprite(surf, (5, 5), 9)
        assert surf == sprite.surface
        assert (5, 5) == sprite.top_left_position
        assert 9 == sprite.layer

    def test_move(self):
        pygame.init()
        surf = pygame.Surface((10, 10))
        sprite = Sprite(surf, (5, 5), 9)
        sprite.move(-4, 12)
        assert sprite.top_left_position == (1, 17)
