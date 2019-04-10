from flask import Flask, jsonify

from logger import logger
from models import sql_session
from response import JsonResponse
from views import BalanceApiView, WalletHistoryApiView, SendMoneyApiView


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.response_class = JsonResponse

    logger.init_app(app)
    sql_session.init_app(app)

    balance_view = BalanceApiView.as_view('balance_view', app)
    app.add_url_rule('{}/balance'.format(app.config['API_BASE_URL']),
            view_func=balance_view, methods=['POST'])

    history_view = WalletHistoryApiView.as_view('history_view', app)
    app.add_url_rule('{}/history'.format(app.config['API_BASE_URL']),
            view_func=history_view, methods=['POST'])

    send_money_view = SendMoneyApiView.as_view('send_money_view', app)
    app.add_url_rule('{}/send'.format(app.config['API_BASE_URL']),
            view_func=send_money_view, methods=['POST'])
    return app


app = create_app('config.config.Config')


@app.errorhandler(400)
def custom400(error):
    response = jsonify({'message': error.description})
    response.status_code = 400
    return response


if __name__ == '__main__':
    app.run()
