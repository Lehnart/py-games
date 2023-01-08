import math
import time

from engine.events.set_sprite_position import SetSpritePosition
from engine.mesper import World
from colony_builder.settlers.components.agent import Agent
from colony_builder.settlers.events.move_agent import MoveAgent
from colony_builder.settlers.processors.agent_mover import AgentMover


class TestAgentMover:

    def test_time_update(self):
        world = World()
        agent_mover = AgentMover()
        world.add_processor(agent_mover)
        first_time = agent_mover.last_process_time

        time.sleep(0.1)
        world.process()
        second_time = agent_mover.last_process_time
        assert second_time >= first_time + 0.1

    def test_move_agent_at_dest(self):
        world = World()
        agent_mover = AgentMover()
        world.add_processor(agent_mover)

        agent_ent = world.create_entity(Agent((1., 5.), 2000.))
        world.publish(MoveAgent(agent_ent, (2., 10.)))
        time.sleep(0.1)
        world.process()

        agent_comp = world.component_for_entity(agent_ent, Agent)
        assert abs(agent_comp.pos[0] - 2.) < 0.00001
        assert abs(agent_comp.pos[1] - 10.) < 0.00001

        world.publish(MoveAgent(agent_ent, (2., 10.)))
        time.sleep(0.1)
        world.process()

        agent_comp = world.component_for_entity(agent_ent, Agent)
        assert abs(agent_comp.pos[0] - 2.) < 0.00001
        assert abs(agent_comp.pos[1] - 10.) < 0.00001

    def test_move_agent(self):
        world = World()
        agent_mover = AgentMover()
        world.add_processor(agent_mover)

        agent_ent = world.create_entity(Agent((5., 5.), 2.))
        world.publish(MoveAgent(agent_ent, (10., 5.)))

        time.sleep(0.1)
        world.process()

        agent_comp = world.component_for_entity(agent_ent, Agent)
        assert abs(agent_comp.pos[0] - 2.) <= 4.8
        assert abs(agent_comp.pos[1] - 5.) <= 0.00001

        agent_comp.pos = (5., 5.)
        world.publish(MoveAgent(agent_ent, (10., 10.)))
        time.sleep(0.1)
        world.process()
        assert abs(agent_comp.pos[0] - 10.) <= 5. - (0.2 / math.sqrt(2))
        assert abs(agent_comp.pos[1] - 10.) <= 5. - (0.2 / math.sqrt(2))

    def test_sprite_position_published(self):
        world = World()
        agent_mover = AgentMover()
        world.add_processor(agent_mover)

        agent_ent = world.create_entity(Agent((5., 5.), 2.))
        world.publish(MoveAgent(agent_ent, (10., 5.)))
        world.process()

        msgs = world.receive(SetSpritePosition)
        assert len(msgs) == 1

        msg = msgs[0]
        assert msg.ent == agent_ent
