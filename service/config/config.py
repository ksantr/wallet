
class Config:
    API_BASE_URL = '/api/v1'
    BASE_APP_URL = 'http://wallet'

    DEBUG = True

    DATABASE_URI = '{engine}://{user}:{password}@{host}:{port}/{name}'
    DATABASE = {
                'engine': 'postgresql',
                'name': 'wallet',
                'user': 'wallet',
                'password': 'wallet12345',
                'host': 'localhost',
                'port': '5432'}

    SQLALCHEMY_DATABASE_URI = DATABASE_URI.format(**DATABASE)

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'base': {
                'format': '%(asctime)s; %(process)d; %(thread)d; %(levelname)s; %(name)s; %(message)s)'
            }
        },

        'handlers': {
            'file_handler': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'base',
                'filename': 'logs/debug.log',
                'encoding': 'utf8',
                'maxBytes': 100000,
                'backupCount': 1
            },
            'console_handler': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'base'
            }
        },

        'loggers': {
            '': {
                'level': 'DEBUG',
                'handlers': ['file_handler', 'console_handler']
            }
        }
    }
