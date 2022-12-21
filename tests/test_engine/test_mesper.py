from colony_builder.engine.mesper import MessageQueue, Event


class TestMessageQueue:
    class AnEvent(Event):
        pass

    class UnknownEvent(Event):
        pass

    def test_add(self):
        msg_queue = MessageQueue()
        msg_queue.add(TestMessageQueue.AnEvent, "Test message 1")
        msg_queue.add(TestMessageQueue.AnEvent, "Test message 2")
        assert len(msg_queue.get(TestMessageQueue.AnEvent)) == 2
        assert len(msg_queue.get(TestMessageQueue.UnknownEvent)) == 0
