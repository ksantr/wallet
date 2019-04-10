import logging

from flask import request
from flask.views import MethodView

from decorators import validate_signature, validate_json
from models import Transactions, Wallets
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)


class BaseApiView(MethodView):
    decorators = [validate_signature, validate_json]

    def __init__(self, app):
        self.db_session = app.db_session
        self.config = app.config
        super().__init__()


class SendMoneyApiView(BaseApiView):
    def post(self):
        """Send money request"""
        data = request.get_json()
        api_key = data.get('api_key')
        amount = abs(data.get('amount'))
        recipient_api_key = data.get('recipient')
        logger.debug('Send money request. '
                'sender: {}, amount: {}, recipient: {}, ip: {}'.format(
                         api_key, amount,
                         recipient_api_key, request.remote_addr))

        sender = self.db_session.query(Wallets).filter_by(
                api_key=api_key).with_for_update().one()

        if sender.balance < amount:
            logger.debug('Sender balance exceed: {} {} {}'.format(
                api_key, sender.balance, amount))
            return {'status': 'error', 'message': 'Not enough money'}, 200

        try:
            recipient = self.db_session.query(Wallets).filter_by(
                    api_key=recipient_api_key).with_for_update().one()
        except NoResultFound:
            logger.debug('Recipient not found: {}'.format(
                recipient_api_key))
            return {'status': 'error', 'message': 'Recipient Not Found'}, 200

        if recipient.limit < recipient.balance + amount:
            logger.debug('Recipient lemit exceed: {} {} {}'.format(
                recipient_api_key,
                recipient.limit,
                recipient.balance + amount))
            return {'status': 'error', 'message': 'Recipient Limit Exceed'}, 200

        sender.balance = sender.balance - amount
        recipient.balance = recipient.balance + amount

        transaction = Transactions(
                sender=sender.id,
                recipient=recipient.id,
                amount=amount)
        self.db_session.add(transaction)
        self.db_session.commit()
        logger.debug('Transaction is created: '
                     'trid={}, sender={}, recipient={}, amount={}'.format(
                         transaction.id, sender.id, recipient.id, amount))
        return {'status': 'success'}, 200


class WalletHistoryApiView(BaseApiView):
    def post(self):
        """Get wallet transactions history"""
        data = request.get_json()
        api_key = data.get('api_key')
        logger.debug('Wallet history request: {} {}'.format(
            api_key, request.remote_addr))

        try:
            wallet = self.db_session.query(Wallets).filter_by(api_key=api_key).one()
        except NoResultFound:
            logger.debug('Wallet not found: {}'.format(api_key))
            return {'status': 'error', 'message': 'Wallet Not Found'}, 200

        transactions = self.db_session.query(Transactions).filter_by(sender=wallet.id)

        out = []
        for t in transactions:
            recipient = self.db_session.query(Wallets).filter_by(id=t.recipient).one()
            out.append({'recipient': recipient.api_key,
                        'date': t.date,
                        'amount': t.amount})
        return {'status': 'success', 'history': out}, 200


class BalanceApiView(BaseApiView):
    def post(self):
        """Get wallet balance"""
        data = request.get_json()
        api_key = data.get('api_key')
        logger.debug('Wallet balance request: {} {}'.format(
            api_key, request.remote_addr))
        try:
            wallet = self.db_session.query(Wallets).filter_by(api_key=api_key).one()
        except NoResultFound:
            return {'status': 'error', 'message': 'Wallet Not Found'}, 200
        return {'status': 'success', 'balance': wallet.balance}, 200
