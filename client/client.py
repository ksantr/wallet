import json
import logging
import requests

from argparse import ArgumentParser
from configparser import RawConfigParser

from signature import Signature


logging.basicConfig(format='%(asctime)-15s %(message)s',
        level=logging.DEBUG, filename='debug.log', filemode='a+')
logger = logging.getLogger(__name__)


class Wallet:
    def __init__(self):
        config = RawConfigParser()
        config.read('config.ini')
        self.api_key = config.get('main', 'api_key')
        self.secret_key = config.get('main', 'secret_key')
        self.base_url = config.get('main', 'base_url')

    def parse_cl(self):
        """CL args parser"""
        parser = ArgumentParser(description='Simple wallet')
        parser.add_argument('-b', '--balance', action="store_true",
                                help=('Get wallet balance'))
        parser.add_argument('-s', '--send', metavar='Send', type=float,
                                help='Send money')
        parser.add_argument('-r', '--recipient', metavar='Recipient', type=str,
                                help='Send money recipient')
        parser.add_argument('--history', action="store_true",
                                help='Get tranfers history')
        args = parser.parse_args()
        return args

    def main(self):
        args = self.parse_cl()
        if args.balance:
            balance = self.get_balance()
            print('Wallet balance: {}'.format(balance))
        elif args.history:
            transfers = self.get_history()
            print('Wallet transfers: {}'.format(transfers))
        elif args.send:
            if not args.recipient:
                print('Recipient wallet id is required')
                return
            result = self.send_money(args.send, args.recipient)
            print('Send request result: {}'.format(result))

    def get_balance(self):
        """Get client wallet balance"""
        url = '{}/balance'.format(self.base_url.rstrip('/ '))
        payload = {'api_key': self.api_key}

        signature = Signature.gen_signature(
                'post', url, json.dumps(payload), self.secret_key)
        headers = {'Signature': signature}

        logger.debug('Get balance request: {} {} {}'.format(
            url, payload, signature))

        try:
            res = requests.post(url, json=payload, headers=headers)
            res.raise_for_status()
        except Exception as e:
            logger.exception(e)
            return 'Get balance error'

        json_res = res.json()
        logger.debug('Get balance response: {}'.format(json_res))

        if json_res['status'] == 'success':
            return json_res['balance']
        else:
            return json_res['message']

    def send_money(self, amount, recipient):
        """Send money from wallet"""
        url = '{}/send'.format(self.base_url.rstrip('/ '))

        payload = {'api_key': self.api_key,
                   'amount': amount,
                   'recipient': recipient}

        signature = Signature.gen_signature(
                'post', url, json.dumps(payload), self.secret_key)
        headers = {'Signature': signature}

        logger.debug('Send money request: {} {} {}'.format(
            url, payload, signature))

        try:
            res = requests.post(url, json=payload, headers=headers)
            res.raise_for_status()
        except Exception as e:
            logger.exception(e)
            return 'Send money error'

        json_res = res.json()
        logger.debug('Send money response: {}'.format(json_res))

        if json_res['status'] == 'success':
            return 'Success'
        else:
            return json_res['message']

    def get_history(self):
        """Get wallet transfer history"""
        url = '{}/history'.format(self.base_url.rstrip('/ '))
        payload = {'api_key': self.api_key}

        signature = Signature.gen_signature(
                'post', url, json.dumps(payload), self.secret_key)
        headers = {'Signature': signature}

        logger.debug('History request: {} {} {}'.format(
            url, payload, signature))

        try:
            res = requests.post(url, json=payload, headers=headers)
            res.raise_for_status()
        except Exception as e:
            logger.exception(e)
            return 'Get history error'

        json_res = res.json()
        logger.debug('Get history response: {}'.format(json_res))

        if json_res['status'] == 'success':
            return json_res['history']
        else:
            return json_res['message']


if __name__ == '__main__':
    w = Wallet()
    w.main()
