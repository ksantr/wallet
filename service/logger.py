import logging
import logging.config


class Logger:
    def __init__(self, app=None, config=None):
        self.config = config
        if app is not None:
            self.init_app(app, config)

    def init_app(self, app, config=None):
        """This is used to initialize logger with your app object"""
        if not (config is None or isinstance(config, dict)):
            raise ValueError("`config` must be an instance of dict or None")
        base_config = app.config['LOGGING'].copy()
        if self.config:
            base_config['LOGGING'].update(self.config)
        if config:
            base_config['LOGGING'].update(config)
        config = base_config

        self.setup_logger(config)

    def setup_logger(self, config):
        logging.config.dictConfig(config)


logger = Logger()
