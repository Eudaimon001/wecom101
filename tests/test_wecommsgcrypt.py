import os

from wecom import url_decode, WeComMsgCrypt

args = {
    'msg_signature': 'fe4f1ba8ee03fb6f35440ca8ac53991d5077c3f4',
    'timestamp': '1653368662',
    'nonce': '1653375606',
    'echostr': 'QPGk8AKt9eCWd4PRHLGUV67VD31WV9JD3mD1WFJepKUisi3Cos3+U8ZkR2e9YKueW4xNrQdNGIw+5NitdnhdhQ%3D%3D'
}
args = url_decode(args)
msg_crypt = WeComMsgCrypt(
    sToken=os.environ['CALLBACK_TOKEN'],
    sEncodingAESKey=os.environ['CALLBACK_ENCODING_AES_KEY'],
    sReceiveId=os.environ['CORP_ID']
)


def test_verify_url():
    ret, reply_echo_str = msg_crypt.VerifyURL(sMsgSignature=args['msg_signature'], sTimeStamp=args['timestamp'],
                                              sNonce=args['nonce'], sEchoStr=args['echostr'])
    assert ret == 0
