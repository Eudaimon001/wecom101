import logging
import os

from flask import Flask, request

from wecom.aes import AES256CTR
from wecom import validate_sig, url_decode

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(filename)s:%(funcName)s %(levelname)-7s %(message)s")

app = Flask("WeComServer")


@app.route("/")
def index():
    return "<p>Hello, World!</p>"


@app.route("/api", methods=["GET"])
def api():
    args = request.args.to_dict()
    args = url_decode(args)
    if validate_sig(args, os.environ['CALLBACK_TOKEN']):
        aes_key = os.environ['CALLBACK_ENCODING_AES_KEY'] + "="
        aes_msg = args['echostr']
        rand_msg = AES256CTR(aes_key).decrypt(aes_msg)
    else:
        pass


if __name__ == "__main__":
    ####################
    # FOR DEVELOPMENT
    ####################
    # app.run(host='127.0.0.1', debug=True)
    app.run(host='0.0.0.0', port=80, debug=True)
