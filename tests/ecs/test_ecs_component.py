import munch
import pytest


@pytest.mark.parametrize(
    "data",
    [
        {  # Check the simple case
            "entity": {"name": "user"},
            "component": {"name": "name", "data": "John"},
            "component_update": {"name": "dob", "data": 20180101},
        }
    ],
)
def test_ecs_component(data):
    from kelte.ecs import Component, Entity

    data = munch.munchify(data)

    e = Entity(name=data.entity.name)
    c = Component(data=data.component.data)
    setattr(e, data.component.name, c)
    assert getattr(e, data.component.name) == c.data
    # assert c.entity == e

    c2 = Component(data=data.component_update.data)
    setattr(e, data.component_update.name, c2)
    assert getattr(e, data.component_update.name) == c2.data
    assert c2.entity == c.entity

    assert c2.name is None
