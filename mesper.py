import datetime
import time as _time
from functools import lru_cache as _lru_cache
from typing import Iterable as _Iterable, Tuple, Iterable
from typing import Tuple as _Tuple
from typing import Type, List, Optional


class MessageQueue:

    def __init__(self):
        self._queue = {}

    def add(self, key: Type, message: object):
        if key not in self._queue:
            self._queue[key] = []
        self._queue[key].append([message, 0])

    def tick(self, n_processors):
        for key in self._queue.keys():
            for message in self._queue[key]:
                message[1] += 1

        for key in self._queue.keys():
            self._queue[key] = [msg for msg in self._queue[key] if msg[1] < n_processors]

    def get(self, key: Type) -> List[object]:
        if key not in self._queue:
            return []
        return [msg[0] for msg in self._queue[key]]


class Event:
    def __init__(self):
        pass

    def key(self) -> Type:
        return self.__class__


class Component:
    pass


class Processor:
    priority = 0
    world: 'World' = None

    def process(self, *args, **kwargs):
        raise NotImplementedError


class World:

    def __init__(self, timed=False):
        self._processors = []
        self._next_entity_id = 0
        self._components = {}
        self._entities = {}
        self._dead_entities = set()
        self._message_queue = MessageQueue()

        self._last_process_datetime = datetime.datetime.now()
        self.process_dt = 0

        if timed:
            self.process_times = {}
            self._process = self._timed_process

    def publish(self, event: Event):
        self._message_queue.add(event.key(), event)

    def receive(self, event_class) -> List:
        return self._message_queue.get(event_class)

    def clear_cache(self) -> None:
        self.get_component.cache_clear()
        self.get_components.cache_clear()

    def clear_database(self) -> None:
        self._next_entity_id = 0
        self._dead_entities.clear()
        self._components.clear()
        self._entities.clear()
        self.clear_cache()

    def add_processor(self, processor_instance: Processor, priority=0) -> None:
        assert issubclass(processor_instance.__class__, Processor)
        processor_instance.priority = priority
        processor_instance.world = self
        self._processors.append(processor_instance)
        self._processors.sort(key=lambda proc: proc.priority, reverse=True)

    def remove_processor(self, processor_type: Type[Processor]) -> None:
        for processor in self._processors:
            if type(processor) == processor_type:
                processor.world = None
                self._processors.remove(processor)

    def get_processor(self, processor_type: Type[Processor]) -> Optional[Processor]:
        for processor in self._processors:
            if type(processor) == processor_type:
                return processor
        else:
            return None

    def create_entity(self, *components: Component) -> int:
        self._next_entity_id += 1

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

        if component_type not in self._components:
            self._components[component_type] = set()

        self._components[component_type].add(entity)

        if entity not in self._entities:
            self._entities[entity] = {}

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

    def _get_components(self, *component_types: Type[Component]) -> _Iterable[_Tuple[int, List[Component]]]:
        entity_db = self._entities
        comp_db = self._components

        try:
            for entity in set.intersection(*[comp_db[ct] for ct in component_types]):
                yield entity, [entity_db[entity][ct] for ct in component_types]
        except KeyError:
            pass

    @_lru_cache()
    def get_component(self, component_type: Type[Component]) -> List[Tuple[int, Component]]:
        return [query for query in self._get_component(component_type)]

    @_lru_cache()
    def get_components(self, *component_types: Type[Component]) -> List[Tuple[int, List[Component]]]:
        return [query for query in self._get_components(*component_types)]

    def try_component(self, entity: int, component_type: Type[Component]) -> Optional[Component]:
        if component_type in self._entities[entity]:
            return self._entities[entity][component_type]
        else:
            return None

    def try_components(self, entity: int, *component_types: Type[Component]) -> Optional[List[List[Component]]]:
        if all(comp_type in self._entities[entity] for comp_type in component_types):
            return [self._entities[entity][comp_type] for comp_type in component_types]
        else:
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

    def _process(self, *args, **kwargs):

        self.process_dt = (datetime.datetime.now() - self._last_process_datetime).total_seconds()
        self._last_process_datetime = datetime.datetime.now()

        for processor in self._processors:
            self._message_queue.tick(len(self._processors))
            processor.process(*args, **kwargs)

    def _timed_process(self, *args, **kwargs):
        for processor in self._processors:
            start_time = _time.process_time()
            processor.process(*args, **kwargs)
            process_time = int(round((_time.process_time() - start_time) * 1000, 2))
            self.process_times[processor.__class__.__name__] = process_time

    def process(self, *args, **kwargs):
        self._clear_dead_entities()
        self._process(*args, **kwargs)
