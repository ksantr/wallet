class Config:
    API_BASE_URL = '/sanctions/api/v1'
    DEBUG = True
    LOG_REQUESTS = True

    CACHE_TYPE = 'memcached'
    CACHE_DEFAULT_TIMEOUT = 60

    DATABASE_URI = '{engine}://{user}:{password}@{host}:{port}/{name}'
    DATABASE = {
                'engine': 'postgresql',
                'name': 'sanctions',
                'user': 'anton',
                'password': '12345',
                'host': '127.0.0.1',
                'port': '5432'}

    SQLALCHEMY_DATABASE_URI = DATABASE_URI.format(**DATABASE)

    SOURCE_URLS = {'eu': 'Europa', 'tr': 'Treasury', 'un': 'UnitedNations', 'rf': 'RosFinMonitoring'}

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
                'filename': 'logs/sanctions_api.log',
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


class ProductionConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    DEBUG = True
