import os

from wecom import WeDrive


class TestWeDrive:
    """
    WeCom应用
    """

    def setup_class(self):
        self.wecom = WeDrive(corp_id=os.environ['CORP_ID'],
                             wedrive_secret=os.environ['WEDRIVE_SECRET'],
                             user_id=os.environ['USER_ID'],
                             space_id=os.environ['SPACE_ID'])

    def test_get_file_list(self):
        response = self.wecom.get_file_list()
        assert response['errcode'] == 0
        assert response['errmsg'] == 'ok'
        print(response)

    def test_download_file(self):
        response = self.wecom.get_file_list()
        file_info = response['file_list']['item'][0]
        downloaded_file = self.wecom.download(file_info=file_info, download_dir_path='./')
        print(downloaded_file)

    def test_upload_file(self):
        test_upload_file = os.path.join(os.path.dirname(__file__), '测试文件.xlsx')
        response = self.wecom.upload(test_upload_file)
        print(response)
