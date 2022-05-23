import requests


class WecomWebhook:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send(self, message, msgtype='text', mentioned_list=None, mentioned_mobile_list=None):
        msg_body = {'content': message}
        if mentioned_list is not None and type(mentioned_list) is list:
            msg_body['mentioned_list'] = mentioned_list
        if mentioned_mobile_list is not None and type(mentioned_mobile_list) is list:
            msg_body['mentioned_mobile_list'] = mentioned_mobile_list
        body = {'msgtype': msgtype, msgtype: msg_body}
        response = requests.post(self.webhook_url, json=body)
        return response.json()

    def upload_file(self, file_path):
        pass