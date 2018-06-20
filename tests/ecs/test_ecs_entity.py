import munch
import pytest


@pytest.mark.parametrize('data', [
    {  # Check for defaults
        'components': {},
        'name': None,
    },
    {  # Check for a single component
        'components': [{
            'name': 'health',
            'data': 100,
            }],
        'name': 'player',
    },
    {  # Check for multiple component
        'components': [{
                'name': 'health',
                'data': 100,
            }, {
                'name': 'mana',
                'data': 100,
            }],
        'name': 'elf',
    },
    ])
def test_ecs_entity_Entity(data):
    from kelte.ecs.entity import Entity

    data = munch.Munch(data)

    e = Entity(name=data.name)
    assert e.name == data.name

    components = {}
    for component in data.components:
        component = munch.Munch(component)
        added_component = e.add_component(component.name, component.data)
        assert added_component.name == component.name
        assert added_component.data == component.data
        # Test if entity's attribute is setup (e.g. entity.health == 1)
        assert getattr(e, added_component.name) == component.data
        components[added_component.name] = added_component

    for component_name, component in components.items():
        e.remove_component(component_name)

    with pytest.raises(AttributeError):
        print(e.not_present)
