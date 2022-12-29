from colony_builder.settlers.components.hauler import Hauler


class TestHauler:

    def test_constructor(self):
        hauler = Hauler(5)
        assert hauler.path_ent == 5
