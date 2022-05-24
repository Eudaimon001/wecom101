import urllib.parse

from .wecomwebhook import WecomWebhook
from .wecomagent import WecomAgent
from .wedrive import WeDrive
from .wecommsgcrypt import WeComMsgCrypt


def url_decode(args):
    return {key: urllib.parse.unquote(value) for key, value in args.items()}
