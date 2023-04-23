from colony_builder.settlers.events.move_agent import MoveAgent


class TestMoveAgent:

    def test_constructor(self):
        event = MoveAgent(0, (1., 2.))
        assert event.agent_ent == 0
        assert event.destination == (1., 2.)
