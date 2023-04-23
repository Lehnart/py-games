from colony_builder.settlers.components.agent import Agent


class TestAgent:

    def test_constructor(self):
        agent = Agent((1., 2.), (3., 4.))
        assert agent.pos == (1., 2.)
        assert agent.speed == (3., 4.)
        assert agent.job is None

    def test_move(self):
        agent = Agent((-5., 7.), (-1., 1.))
        agent.move((2., 3.))
        assert agent.pos[0] == -3.
        assert agent.pos[1] == 10.
