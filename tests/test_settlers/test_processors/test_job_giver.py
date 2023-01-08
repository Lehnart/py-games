from mesper.mesper import World
from colony_builder.settlers.components.agent import Agent, Job
from colony_builder.settlers.components.hauler import Hauler
from colony_builder.settlers.components.path import Path
from colony_builder.settlers.events.need_hauler import NeedHauler
from colony_builder.settlers.processors.job_giver import JobGiver
from tests.test_settlers.test_components.test_path import TestPath


class TestJobGiver:

    def test_process(self):
        world = World()

        job_giver = JobGiver()
        world.add_processor(job_giver)

        path = TestPath.create_test_path(world)
        world.publish(NeedHauler(path))
        agent = world.create_entity(Agent((0., 0.), 1.))
        agent2 = world.create_entity(Agent((0., 0.), 1.))
        agent2_comp = world.component_for_entity(agent2, Agent)
        agent2_comp.job = Job.HAULER

        world.process()
        path_comp = world.component_for_entity(path, Path)
        agent_comp = world.component_for_entity(agent, Agent)

        assert path_comp.worker_ent == agent
        assert agent_comp.job == Job.HAULER
        assert world.component_for_entity(agent, Hauler) is not None
