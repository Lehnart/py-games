import datetime

from functools import lru_cache
from typing import Iterable, Tuple, Type, List, Optional


class MessageQueue:
    def __init__(self):
        self._queue = {}

    def add(self, key: Type, message: object):
        if key not in self._queue:
            self._queue[key] = []
        self._queue[key].append([message, 0])

    def tick(self, max_tick):
        for key, value in self._queue.items():
            for message in value:
                message[1] += 1

        for key, value in self._queue.items():
            self._queue[key] = [msg for msg in value if msg[1] < max_tick]

    def get(self, key: Type) -> List[object]:
        if key not in self._queue:
            return []
        return [msg[0] for msg in self._queue[key]]


class Event:

    def key(self) -> Type:
        return self.__class__


class Component:
    pass


class Processor:
    priority = 0
    world: 'World' = None

    def process(self):
        raise NotImplementedError


class World:

    def __init__(self):
        self.is_running = True
        self._processors = []
        self._next_entity_id = 0
        self._components = {}
        self._entities = {}
        self._dead_entities = set()
        self._message_queue = MessageQueue()

        self._last_process_datetime = datetime.datetime.now()
        self.process_dt = 0

    def publish(self, event: Event):
        self._message_queue.add(event.key(), event)

    def receive(self, event_class) -> List:
        return self._message_queue.get(event_class)

    def clear_cache(self) -> None:
        self.get_component.cache_clear()
        self.get_components.cache_clear()

    def add_processor(self, processor_instance: Processor, priority=0) -> None:
        assert issubclass(processor_instance.__class__, Processor)
        processor_instance.priority = priority
        processor_instance.world = self
        self._processors.append(processor_instance)
        self._processors.sort(key=lambda proc: proc.priority, reverse=True)

    def remove_processor(self, processor_type: Type[Processor]) -> None:
        for processor in self._processors:
            if isinstance(processor, processor_type):
                processor.world = None
                self._processors.remove(processor)

    def get_processor(self, processor_type: Type[Processor]) -> Optional[Processor]:
        for processor in self._processors:
            if isinstance(processor, processor_type):
                return processor
        return None

    def create_entity(self, *components: Component) -> int:
        self._next_entity_id += 1

        self._entities[self._next_entity_id] = {}

        for cmp in components:
            self.add_component(self._next_entity_id, cmp)

        return self._next_entity_id

    def delete_entity(self, entity: int, immediate=False) -> None:
        if immediate:
            for component_type in self._entities[entity]:
                self._components[component_type].discard(entity)

                if not self._components[component_type]:
                    del self._components[component_type]

            del self._entities[entity]
            self.clear_cache()

        else:
            self._dead_entities.add(entity)

    def entity_exists(self, entity: int) -> bool:
        return entity in self._entities and entity not in self._dead_entities

    def component_for_entity(self, entity: int, component_type: Type[Component]) -> Component:
        return self._entities[entity][component_type]

    def components_for_entity(self, entity: int) -> Tuple[Component, ...]:
        return tuple(self._entities[entity].values())

    def has_component(self, entity: int, component_type: Type[Component]) -> bool:
        return component_type in self._entities[entity]

    def has_components(self, entity: int, *component_types: Type[Component]) -> bool:
        return all(comp_type in self._entities[entity] for comp_type in component_types)

    def add_component(self, entity: int, component_instance: Component,
                      type_alias: Optional[Type[Component]] = None) -> None:
        component_type = type_alias or type(component_instance)

        if entity not in self._entities:
            return

        if component_type not in self._components:
            self._components[component_type] = set()

        self._components[component_type].add(entity)

        self._entities[entity][component_type] = component_instance
        self.clear_cache()

    def remove_component(self, entity: int, component_type: Type[Component]) -> int:
        self._components[component_type].discard(entity)

        if not self._components[component_type]:
            del self._components[component_type]

        del self._entities[entity][component_type]

        if not self._entities[entity]:
            del self._entities[entity]

        self.clear_cache()
        return entity

    def _get_component(self, component_type: Type[Component]) -> Iterable[Tuple[int, Component]]:
        entity_db = self._entities

        for entity in self._components.get(component_type, []):
            yield entity, entity_db[entity][component_type]

    def _get_components(self, *component_types: Type[Component]) -> Iterable[Tuple[int, List[Component]]]:
        entity_db = self._entities
        comp_db = self._components

        try:
            for entity in set.intersection(*[comp_db[ct] for ct in component_types]):
                yield entity, [entity_db[entity][ct] for ct in component_types]
        except KeyError:
            pass

    @lru_cache()
    def get_component(self, component_type: Type[Component]) -> List[Tuple[int, Component]]:
        return list(query for query in self._get_component(component_type))

    @lru_cache()
    def get_components(self, *component_types: Type[Component]) -> List[Tuple[int, List[Component]]]:
        return list(query for query in self._get_components(*component_types))

    def try_component(self, entity: int, component_type: Type[Component]) -> Optional[Component]:
        if component_type in self._entities[entity]:
            return self._entities[entity][component_type]
        return None

    def try_components(self, entity: int, *component_types: Type[Component]) -> Optional[List[List[Component]]]:
        if all(comp_type in self._entities[entity] for comp_type in component_types):
            return [self._entities[entity][comp_type] for comp_type in component_types]
        return None

    def _clear_dead_entities(self):
        for entity in self._dead_entities:

            for component_type in self._entities[entity]:
                self._components[component_type].discard(entity)

                if not self._components[component_type]:
                    del self._components[component_type]

            del self._entities[entity]

        self._dead_entities.clear()
        self.clear_cache()

    def _process(self):

        self.process_dt = (datetime.datetime.now() - self._last_process_datetime).total_seconds()
        self._last_process_datetime = datetime.datetime.now()

        for processor in self._processors:
            self._message_queue.tick(len(self._processors))
            processor.process()

    def process(self):
        self._clear_dead_entities()
        self._process()

    @classmethod
    def run(cls):
        game_world = cls()
        while game_world.is_running:
            game_world.process()
