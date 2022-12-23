from colony_builder.engine.components.window import Window


class TestMessageQueue:

    def test_constructor(self):
        window = Window((640, 480))
        surface = window.surface()
        assert surface.get_width() == 640
        assert surface.get_height() == 480
