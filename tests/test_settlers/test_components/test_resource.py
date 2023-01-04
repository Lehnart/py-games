from colony_builder.settlers.components.resource import Resource, ResourceType


class TestResource:

    def test_constructor(self):
        resource = Resource(ResourceType.WOOD)
        assert resource.resource_type == ResourceType.WOOD
        assert resource.destination is None
        assert resource.next_flag is None
