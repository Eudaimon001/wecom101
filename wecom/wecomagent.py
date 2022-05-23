import redis
import requests


class WecomAgent:
    def __init__(self, corp_id, agent_secret, agent_id):
        self.corp_id = corp_id
        self.agent_secret = agent_secret
        self.agent_id = agent_id
        self.access_token = self.get_access_token()

    def get_access_token(self):
        r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
        access_token = r.get('wecom_agent_token')

        if access_token is None or len(access_token) == 0:
            get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken"
            response = requests.get(get_token_url,
                                    params={'corpid': self.corp_id, 'corpsecret': self.agent_secret}).json()
            access_token = response['access_token']
            expires_in = int(response['expires_in'])
            r.set('token', access_token, expires_in)

        return access_token

    def send(self, text, to_user):
        send_msg_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send'
        data = {
            "touser": to_user,
            "agentid": self.agent_id,
            "msgtype": "text",
            "text": {
                "content": text
            },
            "duplicate_check_interval": 600
        }
        response = requests.post(send_msg_url, params={'access_token': self.access_token}, json=data).json()
        return response
