import base64
import os
import shutil

import redis
import requests


class WeDrive:
    def __init__(self, corp_id, wedrive_secret, user_id, space_id):
        self.corp_id = corp_id
        self.wedrive_secret = wedrive_secret
        self.access_token = self.get_access_token()
        self.user_id = user_id
        self.space_id = space_id

    def get_access_token(self):
        r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
        access_token = r.get('weipan_token')

        if access_token is None or len(access_token) == 0:
            get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken"
            response = requests.get(get_token_url,
                                    params={'corpid': self.corp_id, 'corpsecret': self.wedrive_secret}).json()
            access_token = response['access_token']
            expires_in = int(response['expires_in'])
            r.set('token', access_token, expires_in)

        return access_token

    def get_file_list(self, sort_type=6, start=0, limit=1000):
        response = requests.post('https://qyapi.weixin.qq.com/cgi-bin/wedrive/file_list',
                                 params={'access_token': self.access_token},
                                 json={
                                     'userid': self.user_id,
                                     'spaceid': self.space_id,
                                     'fatherid': self.space_id,
                                     'sort_type': sort_type,
                                     'start': start,
                                     'limit': limit
                                 }).json()
        return response

    def download(self, file_info, download_dir_path):
        response = requests.post('https://qyapi.weixin.qq.com/cgi-bin/wedrive/file_download',
                                 params={'access_token': self.access_token},
                                 json={
                                     'userid': self.user_id,
                                     'fileid': file_info['fileid'],
                                 }).json()
        download_url = response['download_url']
        cookie_name = response['cookie_name']
        cookie_value = response['cookie_value']
        local_file_path = os.path.join(download_dir_path, file_info['file_name'])
        with requests.get(download_url, cookies={cookie_name: cookie_value}, stream=True) as r:
            with open(local_file_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        return local_file_path

    def upload(self, upload_file_path):
        with open(upload_file_path, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data)
            response = requests.post('https://qyapi.weixin.qq.com/cgi-bin/wedrive/file_upload',
                                     params={'access_token': self.access_token},
                                     json={
                                         "userid": self.user_id,
                                         "spaceid": self.space_id,
                                         "fatherid": self.space_id,
                                         "file_name": os.path.basename(upload_file_path),
                                         "file_base64_content": encoded.decode()
                                     })
            return response
