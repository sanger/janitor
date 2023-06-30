from typing import Any, Dict

LOGGING: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "style": "{",
            "format": "{asctime:<15} {name:<45}:{lineno:<3} {levelname:<7} {message}",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "janitor": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "apscheduler": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
