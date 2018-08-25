import pytest


@pytest.mark.parametrize(
    "data",
    [
        {},
        {"alt": True},
        {"right_alt": True},
        {"left_alt": True},
        {"shift": True},
        {"right_shift": True},
        {"left_shift": True},
        {"meta": True},
        {"left_meta": True},
        {"right_meta": True},
        {"control": True},
        {"right_control": True},
        {"left_control": True},
    ],
)
def test_keys_KeyModifiers(data):
    from kelte.engine.ui import KeyboardModifiers

    expected = {
        "left_control": False,
        "right_control": False,
        "control": False,
        "left_alt": False,
        "right_alt": False,
        "alt": False,
        "left_shift": False,
        "right_shift": False,
        "shift": False,
        "left_meta": False,
        "right_meta": False,
        "meta": False,
    }
    aggregates = ["control", "shift", "alt", "meta"]

    for key, value in data.items():
        expected[key] = value
        for aggregate in aggregates:
            if key == aggregate:
                expected[f"left_{aggregate}"] = value
                expected[f"right_{aggregate}"] = value

            elif aggregate in key:
                expected[aggregate] = True

    aggregated_data = {k: v for k, v in data.items() if k in aggregates}
    non_aggregated_data = {k: v for k, v in data.items() if k not in aggregates}
    modifier = KeyboardModifiers(**non_aggregated_data)

    # TODO: This should be a better test
    comparison_modifier = KeyboardModifiers(**non_aggregated_data)
    assert modifier == comparison_modifier

    for key, value in aggregated_data.items():
        setattr(modifier, key, value)

    for key, value in expected.items():
        assert (
            getattr(modifier, key) == value
        ), f"{key} expected to be {value} but was {getattr(modifier, key)}."
