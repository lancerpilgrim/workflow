import os
import logging
import logging.config

from yaml import load
from yaml import Loader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = int(os.getenv('DEBUG', 0)) == 1
LOG_LEVEL = 'DEBUG' if DEBUG else 'INFO'
PLATFORM_HOST = "platform.bidongwifi.com"
CLIENT_HOST = "client.bidongwifi.com"
COOKIE_SECRET = "9e98fb0f-bb6b-4426-8067-f7476491c32b"
JWT_SECRET = "fe780900-1203-451e-b700-2c77edd8747f"


def get_conf_path():
    if not DEBUG:
        return '/etc/bidong.yaml'

    conf = os.getenv('CONF_PATH', '/etc/bidong.yaml')
    if conf:
        return conf

    conf = os.path.join(BASE_DIR, 'conf/etc/bidong.yaml')
    return conf


def read_yaml():
    path = get_conf_path()

    with open(path, 'rb') as f:
        stream = f.read()
    return load(stream, Loader=Loader)


globals().update(read_yaml())

conf = {
    'version': 1,
    'formatters': {
        'basic': {
            'format': '%(asctime)s %(name)s %(levelname)s#: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': LOG_LEVEL,
            'formatter': 'basic',
        },
        'rotate_platform': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': LOG_LEVEL,
            'formatter': 'basic',
            'when': 'D',
            'interval': 1,
            'filename': os.path.join(globals().get('rotate_log_dir'),
                                     'platform.log')
        },
        'rotate_project': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': LOG_LEVEL,
            'formatter': 'basic',
            'when': 'D',
            'interval': 1,
            'filename': os.path.join(globals().get('rotate_log_dir'),
                                     'project.log')
        }
    },
    'loggers': {
        '': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'propagate': 0
        },
        'service': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'propagate': 0
        },
        'storage': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'propagate': 0
        },
        'project': {
            'level': LOG_LEVEL,
            'handlers': ['console', 'rotate_project'],
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'propagate': 0
        },
        'platform': {
            'level': LOG_LEVEL,
            'handlers': ['console', 'rotate_platform'],
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'propagate': 0
        }
    },
}

logging.config.dictConfig(conf)
default_logger = logging.getLogger()

version = "v1.0"
