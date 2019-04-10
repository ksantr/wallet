import hashlib
import hmac


class Signature:
    @classmethod
    def sign_message(cls, message, key):
        return hmac.new(
                key=key.encode(), msg=message.encode(),
                digestmod=hashlib.sha256).hexdigest()

    @classmethod
    def gen_signature(cls, method, url, data, key):
        raw_signature = '{method}&{url}&{data}'.format(
                        method=method.upper(), url=url, data=data or '')
        return cls.sign_message(raw_signature, key)
