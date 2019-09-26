import smtplib
from email.mime.text import MIMEText
from email.header import Header
from scau_crawler import Crawler
from config import config


class Mail:
    smtpObj = None
    message = None
    worker = None

    def __init__(self):
        if self.worker is None:
            self.worker = Crawler(config['login_account'], config['login_password'])
        if self.smtpObj is None:
            self.smtpObj = smtplib.SMTP_SSL(config['mail_host'], 465)
        if self.message is None:
            self.worker()
            self.message = MIMEText(str(self.worker), 'plain', 'utf-8')
            self.message['From'] = Header("Lily", 'utf-8')
            self.message['To'] = Header("Test User", 'utf-8')
            self.message['Subject'] = Header('明日课程', 'utf-8')

    def send(self, receiver=config['receive_mail']):
        try:
            self.smtpObj.ehlo()
            self.smtpObj.login(config['mail_account'], config['mail_password'])
            self.smtpObj.sendmail(config['mail_account'], receiver, self.message.as_string())
            print('邮件发送成功')
            return True
        except smtplib.SMTPException as why:
            print(f'邮件发送失败, {why}')
            return False
