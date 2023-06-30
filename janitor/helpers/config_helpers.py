import os
from importlib import import_module
from types import ModuleType


def get_config(settings_module: str = "") -> ModuleType:
    """
    Load configs from janitor/config folder using environment variable.

    Arguments:
        settings_module (str): the settings module to load

    Returns:
        [ModuleType]: config module, available to use via `config.<param>`
    """
    if not settings_module:
        settings_module = os.environ["SETTINGS_MODULE"]

    config = import_module(settings_module)
    return config
