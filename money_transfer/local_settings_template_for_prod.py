import os.path
import logging.config

from .settings import BASE_DIR, MIDDLEWARE

SECRET_KEY = 'REPLACE_ME'

ALLOWED_HOSTS = [
    '*',
]

DEBUG = False

SECURE_SSL_REDIRECT = True

ADMINS = MANAGERS = [
    ('Admin', 'REPLACE_ME_EMAIL'),
]

SERVER_EMAIL = 'REPLACE_ME_EMAIL'

EMAIL_HOST = 'REPLACE_ME'
EMAIL_PORT = 465
EMAIL_HOST_USER = SERVER_EMAIL
EMAIL_HOST_PASSWORD = 'REPLACE_ME'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

EMAIL_SUBJECT_PREFIX = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # TODO pip install psycopg2-binary
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    },
}

MIDDLEWARE += (
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'main.middleware.RedirectToNonWww',
)

STATIC_ROOT = os.path.join(BASE_DIR, 'deploystatic')

# python-telegram-handler
# https://github.com/sashgorokhov/python-telegram-handler
TELEGRAM_LOGGING_BOT_TOKEN = 'REPLACE_ME'
TELEGRAM_LOGGING_BOT_CHAT_ID = 'REPLACE_ME'

# Logging
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'debug': {
            'format': '%(levelname)-8s [%(asctime)s] %(name)s | %(lineno)d | %(funcName)s() — %(message)s',
            # https://docs.python.org/3/library/logging.html#logrecord-attributes
        },
        'telegram': {
            'class': 'telegram_handler.HtmlFormatter',
            'fmt': '<code>%(asctime)s</code> <b>%(levelname)s</b>\n%(processName)s|%(name)s|%(funcName)s()\n%(message)s',
            # https://core.telegram.org/bots/api#html-style
        },
    },
    'handlers': {
        'telegram': {
            'class': 'telegram_handler.TelegramHandler',
            'token': TELEGRAM_LOGGING_BOT_TOKEN,
            'chat_id': TELEGRAM_LOGGING_BOT_CHAT_ID,
            'formatter': 'telegram',
        },
        'error_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': logging.ERROR,
            'formatter': 'debug',
            'filters': ['require_debug_false'],
            'filename': os.path.join(LOG_DIR, 'errors.log'),
            'maxBytes': 10485760,
            'backupCount': 20,
            'encoding': 'utf8',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'loggers': {
        'telegram': {
            'handlers': ['telegram'],
            'level': logging.INFO,
        },
    },
    'root': {
        'level': logging.INFO,
        'handlers': ['error_file_handler', 'telegram']  # TODO pip install python-telegram-handler
    },
})
