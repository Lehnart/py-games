import math
import time

from colony_builder.engine.events.set_sprite_position import SetSpritePosition
from colony_builder.engine.mesper import Processor
from colony_builder.settlers.components.agent import Agent
from colony_builder.settlers.events.move_agent import MoveAgent


class AgentMover(Processor):

    def __init__(self):
        self.last_process_time = time.time()

    def process(self):
        process_time = time.time()
        delta = process_time - self.last_process_time
        self.last_process_time = process_time

        move_agent_events = self.world.receive(MoveAgent)
        for move_agent_event in move_agent_events:
            agent_comp = self.world.component_for_entity(move_agent_event.agent_ent, Agent)
            dest = move_agent_event.destination
            pos = agent_comp.pos
            dist_x, dist_y = (dest[0] - pos[0], dest[1] - pos[1])
            norm = math.sqrt((dist_x ** 2) + (dist_y ** 2))

            if norm < 0.001:
                continue

            vec_x, vec_y = dist_x / norm, dist_y / norm
            move_x, move_y = delta * agent_comp.speed[0] * vec_x, delta * agent_comp.speed[1] * vec_y

            if abs(move_x) > abs(dist_x):
                move_x = dist_x
            if abs(move_y) > abs(dist_y):
                move_y = dist_y

            agent_comp.move((move_x, move_y))
            self.world.publish(
                SetSpritePosition(
                    move_agent_event.agent_ent,
                    (int(agent_comp.pos[0] * 16), int(agent_comp.pos[1] * 16))
                )
            )
