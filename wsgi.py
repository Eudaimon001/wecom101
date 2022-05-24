import logging
import os

from flask import Flask, request

from wecom import url_decode, WeComMsgCrypt

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(filename)s:%(funcName)s %(levelname)-7s %(message)s")

app = Flask("WeComServer")


@app.route("/")
def index():
    return "<p>Hello, World!</p>"


@app.route("/api", methods=["GET"])
def api():
    args = request.args.to_dict()
    args = url_decode(args)
    msg_crypt = WeComMsgCrypt(
        sToken=os.environ['CALLBACK_TOKEN'],
        sEncodingAESKey=os.environ['CALLBACK_ENCODING_AES_KEY'],
        sReceiveId=os.environ['CORP_ID']
    )
    ret, result = msg_crypt.VerifyURL(sMsgSignature=args['msg_signature'], sTimeStamp=args['timestamp'],
                                      sNonce=args['nonce'], sEchoStr=args['echostr'])
    status_code = 200 if ret == 0 else 400
    return result, status_code


if __name__ == "__main__":
    ####################
    # FOR DEVELOPMENT
    ####################
    # app.run(host='127.0.0.1', debug=True)
    app.run(host='0.0.0.0', port=80, debug=True)
