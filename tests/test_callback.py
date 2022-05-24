import os

from wecom.aes import AES256CTR
from wecom.callbackhandler import validate_sig, url_decode

args = {
    'msg_signature': 'fe4f1ba8ee03fb6f35440ca8ac53991d5077c3f4',
    'timestamp': '1653368662',
    'nonce': '1653375606',
    'echostr': 'QPGk8AKt9eCWd4PRHLGUV67VD31WV9JD3mD1WFJepKUisi3Cos3+U8ZkR2e9YKueW4xNrQdNGIw+5NitdnhdhQ%3D%3D'
}
args = url_decode(args)


def test_validate_sig():
    assert validate_sig(args, os.environ['CALLBACK_TOKEN'])


def test_aes():
    aes_key = os.environ['CALLBACK_ENCODING_AES_KEY'] + "="
    aes_msg = args['echostr']
    rand_msg = AES256CTR(aes_key).decrypt(aes_msg)
    print(rand_msg)
