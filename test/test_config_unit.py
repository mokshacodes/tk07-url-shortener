"""Unit tests for application configuration."""

from config import Config, config_factory


def test_config_factory_returns_default_config() -> None:
    """Ensures the config factory returns the default application config."""
    # Act
    config = config_factory()

    # Assert
    assert config == Config()
    assert config.links_path == "data/links.json"
