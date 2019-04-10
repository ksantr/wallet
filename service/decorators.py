from functools import wraps

from flask import abort, request
from sqlalchemy.orm.exc import NoResultFound

from models import SQLAlchemy, Wallets
from signature import Signature
from config import Config


def validate_signature(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        # Set sql session
        sql = SQLAlchemy()
        session = sql.init_db(Config.SQLALCHEMY_DATABASE_URI)()

        data = request.get_json()

        api_key = data.get('api_key')
        if not api_key:
            abort(400, 'Api-key error')

        try:
            wallet = session.query(Wallets).filter_by(api_key=api_key).one()
        except NoResultFound:
            abort(400, 'Wallet not found')

        signature = Signature.gen_signature(
                            method=request.method,
                            url=request.url,
                            data=request.data.decode(),
                            key=wallet.secret_key)

        if signature != request.headers.get('Signature'):
            abort(400, 'Signature error')
        return func(*args, **kwargs)
    return func_wrapper


def validate_json(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        try:
            data = request.get_json()
        except Exception:
            abort(400, 'JSON validation error')
        if not data:
            abort(400, 'JSON validation error')
        return func(*args, **kwargs)
    return func_wrapper
