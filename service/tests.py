from flask_testing import TestCase

from app import create_app
from models import Transactions, Wallets


class TestViews(TestCase):
    def create_app(self):
        app = create_app('config.Config')
        return app

    def test_get_balance(self):
        pass

    def test_get_history(self):
        pass

    def test_limit_exceed(self):
        pass

    def test_balance_exceed(self):
        pass

    def test_send_money(self):
        pass

    def test_good_api_key(self):
        pass

    def test_wrong_api_key(self):
        pass
