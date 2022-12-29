from colony_builder.engine.mesper import Processor
from colony_builder.settlers.components.agent import Agent, Job
from colony_builder.settlers.components.hauler import Hauler
from colony_builder.settlers.components.path import Path
from colony_builder.settlers.events.need_hauler import NeedHauler


class JobGiver(Processor):

    def process(self):
        need_hauler_events = self.world.receive(NeedHauler)
        for need_hauler_event in need_hauler_events:
            agents = self.world.get_component(Agent)
            for agent_ent, agent_comp in agents:
                if agent_comp.job is not None:
                    continue
                path_ent = need_hauler_event.path_ent
                path_comp = self.world.component_for_entity(path_ent, Path)

                path_comp.assign_worker(agent_ent)
                agent_comp.assign_job(Job.HAULER)
                self.world.add_component(agent_ent, Hauler(path_ent))
                break
