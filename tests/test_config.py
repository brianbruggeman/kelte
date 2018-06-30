import pytest


@pytest.mark.parametrize(
    "data",
    [
        # Project settings
        "repo_path",
        "assets_path",
        # Main windows settings
        "width",
        "height",
        "title",
        "full_screen",
        "font_path",
    ],
)
def test_config_settings_attributes(data):
    from kelte.config import settings

    assert hasattr(settings, data)
