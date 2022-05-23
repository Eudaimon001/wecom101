import os.path

import requests


class WecomWebhook:
    send_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send'
    upload_media_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media'

    def __init__(self, webhook_bot_key):
        self.webhook_bot_key = webhook_bot_key

    def send(self, message, msgtype='text', mentioned_list=None, mentioned_mobile_list=None):
        msg_body = {'content': message}
        if mentioned_list is not None and type(mentioned_list) is list:
            msg_body['mentioned_list'] = mentioned_list
        if mentioned_mobile_list is not None and type(mentioned_mobile_list) is list:
            msg_body['mentioned_mobile_list'] = mentioned_mobile_list
        body = {'msgtype': msgtype, msgtype: msg_body}
        response = requests.post(self.send_url, params={'key': self.webhook_bot_key}, json=body)
        return response.json()

    def upload_file(self, file_path):
        file_name = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            file_data = f.read()
        response = requests.post(self.upload_media_url,
                                 params={'key': self.webhook_bot_key, 'type': 'file'},
                                 files={'file': (file_name, file_data)},
                                 headers={"Content-Type": "multipart/form-data"})
        """
{
   "errcode": 0,
   "errmsg": "ok",
   "type": "file",
   "media_id": "1G6nrLmr5EC3MMb_-zK1dDdzmd0p7cNliYu9V5w7o8K0",
   "created_at": "1380000000"
}
        """
        file_upload_res = response.json()
        response = requests.post(self.send_url, params={'key': self.webhook_bot_key},
                                 json={
                                     "msgtype": "file",
                                     "file": {
                                         "media_id": file_upload_res['media_id']
                                     }
                                 })
        return response.json()
