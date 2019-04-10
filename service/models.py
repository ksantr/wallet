import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class SQLAlchemy:
    def __init__(self, app=None, config=None):
        self.config = config
        if app is not None:
            self.init_app(app, config)

    def init_app(self, app, config=None):
        """This is used to initialize logger with your app object"""
        if not (config is None or isinstance(config, dict)):
            raise ValueError("`config` must be an instance of dict or None")
        base_config = app.config.copy()
        if self.config:
            base_config.update(self.config)
        if config:
            base_config.update(config)
        config = base_config
        Session = self.init_db(config['SQLALCHEMY_DATABASE_URI'])
        app.db_session = Session()

    def init_db(self, uri):
        engine = create_engine(uri, pool_recycle=3600)
        Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        return Session


sql_session = SQLAlchemy()


class Wallets(Base):
    __tablename__ = 'wallets'
    __table_args__ = {'useexisting': True}

    id = Column(Integer, primary_key=True)
    balance = Column(Float(2))
    api_key = Column(String(255))
    secret_key = Column(String(255))
    limit = Column(Float(2))


class Transactions(Base):
    __tablename__ = 'transactions'
    __table_args__ = {'useexisting': True}

    id = Column(Integer, primary_key=True)
    sender = Column(Integer, ForeignKey('wallets.id'))
    recipient = Column(Integer, ForeignKey('wallets.id'))
    amount = Column(Float(2))
    date = Column(DateTime, default=datetime.datetime.utcnow)
