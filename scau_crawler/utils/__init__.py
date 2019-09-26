from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from scau_crawler import Crawler
from config import config


def get_tomorrow_week_number():
    return (datetime.today().day - datetime(2019, 9, 2).day + 1) // 7 + 1


def get_tomorrow_weekday():
    return (datetime.today().weekday())

class Mail:
    smtpObj = None
    message = None
    worker = None

    def __init__(self):
        if self.worker is None:
            worker = Crawler(config['login_account'], config['login_password'])
        if self.smtpObj is None:
            self.smtpObj = smtplib.SMTP_SSL(config['mail_host'], 465)
        if self.message is None:
            message = MIMEText(str(self.worker), 'plain', 'utf-8')
            message['From'] = Header("Lily", 'utf-8')
            message['To'] = Header("", 'utf-8')
            message['Subject'] = Header('明日课程', 'utf-8')
            receiver = config['receive_mail']

    def send(self, receiver, message):
        try:
            self.smtpObj.ehlo()
            self.smtpObj.login(config['mail_account'], config['mail_password'])
            self.smtpObj.sendmail(config['mail_account'], receiver, message.as_string())
            print('邮件发送成功')
            return True
        except smtplib.SMTPException as why:
            print(f'邮件发送失败, {why}')
            return False


print(datetime.today().weekday())