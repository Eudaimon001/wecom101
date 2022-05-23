import os

from wecom import WecomAgent


class TestWecomAgent:
    """
    WeCom应用
    """

    def setup_class(self):
        self.wecom = WecomAgent(corp_id=os.environ['CORP_ID'],
                                agent_secret=os.environ['AGENT_SECRET'],
                                agent_id=os.environ['AGENT_ID'])

    def test_send_text(self):
        response = self.wecom.send('Hello world!', os.environ['USER_ID'])
        assert response['errcode'] == 0
        assert response['errmsg'] == 'ok'
