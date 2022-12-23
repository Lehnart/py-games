import pytest

from colony_builder.engine.mesper import MessageQueue, Event, Processor, World, Component


class TestMessageQueue:
    class AnEvent(Event):
        pass

    class UnknownEvent(Event):
        pass

    test_message_str_1 = "Test message 1"

    def get_msg_queue(self):
        msg_queue = MessageQueue()
        msg_queue.add(TestMessageQueue.AnEvent, TestMessageQueue.test_message_str_1)
        return msg_queue

    def test_add(self):
        msg_queue = self.get_msg_queue()
        msg_queue.add(TestMessageQueue.AnEvent, "Test message 2")
        assert len(msg_queue.get(TestMessageQueue.AnEvent)) == 2
        assert len(msg_queue.get(TestMessageQueue.UnknownEvent)) == 0

    def test_get(self):
        msg_queue = self.get_msg_queue()
        assert len(msg_queue.get(TestMessageQueue.AnEvent)) == 1
        assert msg_queue.get(TestMessageQueue.AnEvent) == [TestMessageQueue.test_message_str_1]
        assert msg_queue.get(TestMessageQueue.UnknownEvent) == []

    def test_tick(self):
        msg_queue = self.get_msg_queue()
        msg_queue.tick(2)
        assert len(msg_queue.get(TestMessageQueue.AnEvent)) == 1
        assert msg_queue.get(TestMessageQueue.AnEvent) == [TestMessageQueue.test_message_str_1]
        msg_queue.tick(2)
        assert len(msg_queue.get(TestMessageQueue.AnEvent)) == 0
        assert msg_queue.get(TestMessageQueue.AnEvent) == []


class TestEvent:
    class MyEvent(Event):
        pass

    def test_event(self):
        my_event = TestEvent.MyEvent()
        assert my_event.key() == TestEvent.MyEvent


class TestProcessor:

    def test_processor(self):
        with pytest.raises(NotImplementedError):
            processor = Processor()
            processor.process()


class TestWorld:
    class MyEvent(Event):
        def __init__(self, txt: str):
            self.txt = txt

    class MyProcessor(Processor):
        def __init__(self):
            self.count = 0

        def process(self):
            self.count += 1

    class AComponent(Component):
        pass

    class AnotherComponent(Component):
        pass

    class OtherComponent(Component):
        pass

    def test_publish_and_receive(self):
        world = World()
        world.publish(TestWorld.MyEvent("toto"))
        events = world.receive(TestWorld.MyEvent)
        assert len(events) == 1
        event = events[0]
        assert event.txt == "toto"

    def test_processor_modification(self):
        world = World()
        processor = world.get_processor(TestWorld.MyProcessor)
        assert processor is None
        world.add_processor(TestWorld.MyProcessor())
        processor = world.get_processor(TestWorld.MyProcessor)
        assert isinstance(processor, TestWorld.MyProcessor)
        world.remove_processor(TestWorld.MyProcessor)
        processor = world.get_processor(TestWorld.MyProcessor)
        assert processor is None

    def test_entity_creation_and_deletion(self):
        world = World()
        assert world.entity_exists(1) is False
        entity_1 = world.create_entity()
        entity_2 = world.create_entity()
        assert world.entity_exists(entity_1) is True
        assert world.entity_exists(entity_2) is True
        world.delete_entity(entity_1)
        assert world.entity_exists(entity_1) is False
        world.delete_entity(entity_2, True)
        assert world.entity_exists(entity_2) is False

    def test_component_for_entity(self):
        world = World()
        comp1 = TestWorld.AComponent()
        comp2 = TestWorld.AnotherComponent()

        entity_1 = world.create_entity(comp1)
        comp = world.component_for_entity(entity_1, TestWorld.AComponent)
        assert comp == comp1
        comp = world.component_for_entity(entity_1, TestWorld.AnotherComponent)
        assert comp is None

        world.add_component(entity_1, comp2)
        comp = world.component_for_entity(entity_1, TestWorld.AComponent)
        assert comp == comp1
        comp = world.component_for_entity(entity_1, TestWorld.AnotherComponent)
        assert comp == comp2

        world.remove_component(entity_1, TestWorld.AComponent)
        comp = world.component_for_entity(entity_1, TestWorld.AComponent)
        assert comp is None
        comp = world.component_for_entity(entity_1, TestWorld.AnotherComponent)
        assert comp == comp2

    def test_components_for_entity(self):
        world = World()
        comp1 = TestWorld.AComponent()
        comp2 = TestWorld.AnotherComponent()

        entity_1 = world.create_entity(comp1, comp2)
        comps = world.components_for_entity(entity_1)
        assert comp1 in comps
        assert comp2 in comps

    def test_get_components(self):
        world = World()
        comp1 = TestWorld.AComponent()
        comp2 = TestWorld.AnotherComponent()

        entity_1 = world.create_entity(comp1)
        entity_2 = world.create_entity(comp2)
        entity_3 = world.create_entity(comp1, comp2)

        comp_and_ent_list = world.get_component(TestWorld.AComponent)
        assert len(comp_and_ent_list) == 2
        assert (entity_1, comp1) in comp_and_ent_list
        assert (entity_3, comp1) in comp_and_ent_list

        comp_and_ent_list = world.get_component(TestWorld.AnotherComponent)
        assert len(comp_and_ent_list) == 2
        assert (entity_2, comp2) in comp_and_ent_list
        assert (entity_3, comp2) in comp_and_ent_list

        comp_and_ent_list = world.get_component(TestWorld.OtherComponent)
        assert len(comp_and_ent_list) == 0

        comp_and_ent_list = world.get_components(TestWorld.AComponent, TestWorld.AnotherComponent)
        assert len(comp_and_ent_list) == 1
        assert (entity_3, [comp1, comp2]) in comp_and_ent_list

    def test_process(self):
        world = World()
        processor = TestWorld.MyProcessor()
        world.add_processor(processor)
        processor = world.get_processor(TestWorld.MyProcessor)
        assert isinstance(processor, TestWorld.MyProcessor)
        assert processor.count == 0

        world.process()
        processor = world.get_processor(TestWorld.MyProcessor)
        assert isinstance(processor, TestWorld.MyProcessor)
        assert processor.count == 1
