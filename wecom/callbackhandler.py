import urllib.parse
from hashlib import sha1


def url_decode(args):
    return {key: urllib.parse.unquote(value) for key, value in args.items()}


def validate_sig(args, token):
    msg_signature = args['msg_signature']
    timestamp = args['timestamp']
    nonce = args['nonce']
    echostr = args['echostr']
    sort_array = sorted([token, timestamp, nonce, echostr])
    sort_str = ''.join(sort_array)
    dev_msg_signature = sha1(sort_str.encode()).hexdigest()
    return dev_msg_signature == msg_signature
