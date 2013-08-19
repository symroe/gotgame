from .common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Marco Fucci', 'marcofucci@gmail.com'),
    ('Sym Roe', 'sym.roe@talusdesign.co.uk')
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gotgame',
        'USER': 'gotgameuser',
        'PASSWORD': get_env_value('POSTGRES_PASSWORD'),
        'HOST': '',
        'PORT': '',
    }
}

HOST_NAME = "http://integration.gotgameapp.com"

# LOGGING

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    }
}
