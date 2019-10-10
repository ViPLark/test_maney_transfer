import logging.config
import os

from .settings import BASE_DIR, INSTALLED_APPS

SECRET_KEY = 'REPLACE_ME'

DEBUG = True
TEMPLATE_DEBUG = True
THUMBNAIL_DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
]

ADMINS = MANAGERS = [
    ('Admin', 'REPLACE_ME_EMAIL'),
]

SERVER_EMAIL = 'REPLACE_ME_EMAIL'

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
# TODO Then run a dummy SMTP server: `python -m smtpd -n -c DebuggingServer localhost:1025`

INSTALLED_APPS += ()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'debug': {
            'format': '%(levelname)-8s [%(asctime)s] %(name)s | %(lineno)d | %(funcName)s() — %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': logging.DEBUG,
            'formatter': 'debug',
            'stream': 'ext://sys.stdout',
        },
    },
    'root': {
        'level': logging.DEBUG,
        'handlers': ['console']
    },
})
