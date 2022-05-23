import os

from wecom.wecomwebhook import WecomWebhook


class TestWecomWebhook:
    def setup_class(self):
        self.wecom = WecomWebhook(os.environ['WEBHOOK_URL'])

    def test_send_text(self):
        response = self.wecom.send('Hello everybody!')
        assert response['errcode'] == 0
        assert response['errmsg'] == 'ok'

    def test_send_mentioned_text(self):
        response = self.wecom.send('Hello, ', mentioned_list=['wuhan', '@all'])
        assert response['errcode'] == 0
        assert response['errmsg'] == 'ok'

    def test_send_mentioned_mobile_list_text(self):
        response = self.wecom.send('Hello, ', mentioned_mobile_list=[os.environ['MY_MOBILE']])
        assert response['errcode'] == 0
        assert response['errmsg'] == 'ok'

    def test_send_md(self):
        md = '您的会议室已经预定，稍后会同步到`邮箱` \n' \
             '>**事项详情** \n' \
             '>事　项：<font color="info">开会</font> \n' \
             '>组织者：@miglioguan \n' \
             '>参与者：@miglioguan、@kunliu、@jamdeezhou、@kanexiong、@kisonwang \n' \
             '> \n' \
             '>会议室：<font color="info">广州TIT 1楼 301</font> \n' \
             '>日　期：<font color="warning">2018年5月18日</font> \n' \
             '>时　间：<font color="comment">上午9:00-11:00</font> \n' \
             '> \n' \
             '>请准时参加会议。 \n' \
             '> \n' \
             '>如需修改会议信息，请点击：[修改会议信息](https://work.weixin.qq.com)'
        response = self.wecom.send(md, msgtype='markdown', mentioned_mobile_list=[os.environ['MY_MOBILE']])
        assert response['errcode'] == 0
        assert response['errmsg'] == 'ok'
