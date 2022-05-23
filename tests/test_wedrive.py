import os

from wecom import WeDrive


class TestWeDrive:
    """
    WeCom应用
    """

    def setup_class(self):
        self.wecom = WeDrive(corp_id=os.environ['CORP_ID'],
                             wedrive_secret=os.environ['WEDRIVE_SECRET'])

    def test_get_file_list(self):
        response = self.wecom.get_file_list(user_id=os.environ['USER_ID'], space_id=os.environ['SPACE_ID'])
        assert response['errcode'] == 0
        assert response['errmsg'] == 'ok'
        print(response)

    def test_download_file(self):
        response = self.wecom.get_file_list(user_id=os.environ['USER_ID'], space_id=os.environ['SPACE_ID'])
        file_info = response['file_list']['item'][0]
        downloaded_file = self.wecom.download(user_id=os.environ['USER_ID'], file_info=file_info,
                                              download_dir_path='./')
        print(downloaded_file)
