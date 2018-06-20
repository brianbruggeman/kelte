import munch
import pytest


@pytest.mark.parametrize('data', [
    {  # Check the simple case
        'entity': {
            'name': 'player',
            },
        'component': {
            'name': 'health',
            'data': 100
            },
        'component_update': {
            'name': 'mana',
            'data': 10,
            }
    },
    ])
def test_ecs_component_Component(data):
    from kelte.ecs import Component, Entity

    data = munch.munchify(data)

    e = Entity(name=data.entity.name)
    c = Component(e, name=data.component.name, data=data.component.data)
    assert hasattr(e, data.component.name)
    assert getattr(e, data.component.name) == data.component.data

    assert getattr(e, data.component.name).__get__(None, None) == c
    assert getattr(e, data.component.name).__get__(c, c) == c.data

    assert getattr(e, data.component.name).__set__(c, 1) == c
    with pytest.raises(AttributeError):
        assert getattr(e, data.component.name).__set__(None, None) == c

    c.name = data.component_update.name
    c.data = data.component_update.data

    assert getattr(e, data.component_update.name) == data.component_update.data
