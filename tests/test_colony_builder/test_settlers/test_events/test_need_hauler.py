from colony_builder.settlers.events.need_hauler import NeedHauler


class TestNeedHauler:

    def test_constructor(self):
        event = NeedHauler(0)
        assert event.path_ent == 0
