import os
import time

import xmltodict

from wecom import url_decode, WeComMsgCrypt

msg_crypt = WeComMsgCrypt(
    sToken=os.environ['CALLBACK_TOKEN'],
    sEncodingAESKey=os.environ['CALLBACK_ENCODING_AES_KEY'],
    sReceiveId=os.environ['CORP_ID']
)


def test_verify_url():
    args = url_decode({
        'msg_signature': 'fe4f1ba8ee03fb6f35440ca8ac53991d5077c3f4',
        'timestamp': '1653368662',
        'nonce': '1653375606',
        'echostr': 'QPGk8AKt9eCWd4PRHLGUV67VD31WV9JD3mD1WFJepKUisi3Cos3+U8ZkR2e9YKueW4xNrQdNGIw+5NitdnhdhQ%3D%3D'
    })
    ret, reply_echo_str = msg_crypt.VerifyURL(sMsgSignature=args['msg_signature'], sTimeStamp=args['timestamp'],
                                              sNonce=args['nonce'], sEchoStr=args['echostr'])
    assert ret == 0
    assert reply_echo_str == b'9126774625041940471'


def test_decrypt():
    args = {
        'msg_signature': '1a1dd500d1d5bd095684a80bc201679d866881f8',
        'timestamp': '1653388309',
        'nonce': '1653361162'
    }
    content = '<xml><ToUserName><![CDATA[wwbdd7609be778bb8d]]></ToUserName><Encrypt><![CDATA[EY8ng1U6a60W6GRYlRPD5DB0/S0u4YvvtaQYvTPXwMxnl0lXqXpNbTzhBbL7iJ6f9S9yd38gTg0e4reftYDGSFhgDquVb3yIdqYZJeY5P/WAmTWHpK055SKie35HREmyWUSSnNTqBCLe9HZWtcsTMIwXgBsxv13aNitcYKjcxIY4TzWHwFrRrByRoKCWqI8kt6qIzdF0ebGo3C2KCHph25v5bvhhmSnYravlDL/oUyDc/tmPFLGInGVqZXg+PRLKkvDNvpQTa//E1g+CanRiPlYHl+3tbC4XEaTOAWrT6L2XOfLU+8SYQ0lVEvlxGjOR6UPlfJ2/oLWaGO8gkwkR/ssBwUxuV4ptlu47wPxgXSVvnqSyHIU1BmN1wSpHONXqGnWojZQM4E4A/zO3f6AvzNKhkzcO8j8Wjsv+nAAlQjU=]]></Encrypt><AgentID><![CDATA[1000006]]></AgentID></xml>'
    ret, msg = msg_crypt.DecryptMsg(sPostData=content, sMsgSignature=args['msg_signature'],
                                    sTimeStamp=args['timestamp'], sNonce=args['nonce'])
    assert ret == 0
    assert msg == b'<xml><ToUserName><![CDATA[wwbdd7609be778bb8d]]></ToUserName><FromUserName><![CDATA[WuHan]]></FromUserName><CreateTime>1653388309</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[hi]]></Content><MsgId>7101248714887079956</MsgId><AgentID>1000006</AgentID></xml>'


def test_encrypt():
    timestamp = str(int(time.time() * 1000))
    reply = '<xml><ToUserName><![CDATA[wwbdd7609be778bb8d]]></ToUserName><FromUserName><![CDATA[WuHan]]></FromUserName><CreateTime>1653388309</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[hi]]></Content><MsgId>7101248714887079956</MsgId><AgentID>1000006</AgentID></xml>'
    ret, msg = msg_crypt.EncryptMsg(sReplyMsg=reply, sNonce=timestamp, timestamp=timestamp)
    assert ret == 0


def test_xmltodict():
    xml = '<xml><ToUserName><![CDATA[wwbdd7609be778bb8d]]></ToUserName><FromUserName><![CDATA[WuHan]]></FromUserName><CreateTime>1653388309</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[hi]]></Content><MsgId>7101248714887079956</MsgId><AgentID>1000006</AgentID></xml>'
    msg = xmltodict.parse(xml)['xml']
    print(msg)
