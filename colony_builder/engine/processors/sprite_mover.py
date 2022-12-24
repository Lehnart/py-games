from colony_builder.engine.components.sprite import Sprite
from colony_builder.engine.events.move_sprite import MoveSprite
from colony_builder.engine.mesper import Processor


class SpriteMover(Processor):

    def process(self):
        move_sprite_events = self.world.receive(MoveSprite)

        for move_sprite_event in move_sprite_events:
            sprite_component = self.world.component_for_entity(move_sprite_event.ent, Sprite)
            sprite_component.move(*move_sprite_event.movement)
