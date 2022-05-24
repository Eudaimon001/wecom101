import logging
import os

from flask import Flask, request

from wecom import url_decode, WeComMsgCrypt
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(filename)s:%(funcName)s %(levelname)-7s %(message)s")

app = Flask("WeComServer")

msg_crypt = WeComMsgCrypt(
    sToken=os.environ['CALLBACK_TOKEN'],
    sEncodingAESKey=os.environ['CALLBACK_ENCODING_AES_KEY'],
    sReceiveId=os.environ['CORP_ID']
)


@app.route("/api", methods=["GET"])
def api_get():
    args = url_decode(request.args.to_dict())

    ret, result = msg_crypt.VerifyURL(sMsgSignature=args['msg_signature'], sTimeStamp=args['timestamp'],
                                      sNonce=args['nonce'], sEchoStr=args['echostr'])
    status_code = 200 if ret == 0 else 400
    return result, status_code


@app.route("/api", methods=["POST"])
def api_post():
    args = request.args.to_dict()
    content = request.get_data()
    logging.info(args, content)


if __name__ == "__main__":
    ####################
    # FOR DEVELOPMENT
    ####################
    # app.run(host='127.0.0.1', debug=True)
    app.run(host='0.0.0.0', port=80, debug=True)
