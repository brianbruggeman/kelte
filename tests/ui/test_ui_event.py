import munch
import pytest


@pytest.mark.parametrize('data', [
    {
        'key': ('b', True, False, False, False, False, False),
        'expected': {
            'action': 'pressed'
            }
    }
])
def test_ui_events_UserInputEvent(data):
    import tcod as tdl
    from kelte.ui.event import KeyboardEvent

    data = munch.Munch(data)
    tdl_keys = {
        k.replace('KEY_', '').lower(): getattr(tdl, k)
        for k in dir(tdl)
        if k.startswith('KEY_')
        }
    TCODK_CHAR = 0x41  # This should mean a single character enum
    tdl_value = tdl_keys.get(data.key[0], TCODK_CHAR)
    key_args = (tdl_value, *data.key)

    # tdl.Keys are not comparable, so we fudge this by testing
    #   equality across two KeyboardEvents
    event = KeyboardEvent()
    event2 = KeyboardEvent()
    key = tdl.libtcodpy.Key(*key_args)
    key2 = tdl.libtcodpy.Key(*key_args)
    event.tdl_key = key
    event2.tdl_key = key2
    assert event == event2
