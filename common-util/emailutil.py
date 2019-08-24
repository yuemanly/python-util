# -*- coding:utf-8 -*-
#发送email的工具类
# 参考:http://www.runoob.com/python/python-email.html


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailUtil(object):
    def __init__(self,configUtil):
        self.email_host = configUtil.getOrElse("email.host")
        self.email_port = configUtil.getOrElse("email.port")
        self.email_username = configUtil.getOrElse("email.username")
        self.email_password = configUtil.getOrElse("email.password")
        email_receivers = configUtil.getOrElse("email.receivers")
        if email_receivers is not None:
            self.email_receivers_array = configUtil.getOrElse("email.receivers").split(",")

    def send_email(self,subject,content,receivers_array=None):
        try:
            if receivers_array == None:
               receivers_array = self.email_receivers_array

            smtp_server = smtplib.SMTP_SSL(host=self.email_host,port=self.email_port)
            smtp_server.login(self.email_username,self.email_password)

            #支持附件的message类型
            main_message = MIMEMultipart()
            main_message['From'] = self.email_username
            main_message['To'] = ",".join(receivers_array)
            main_message['Subject'] = subject

            #设置邮件的内容
            text_message = MIMEText(content,'plain','utf-8')
            main_message.attach(text_message)

            main_message_str = main_message.as_string()
            smtp_server.sendmail(self.email_username,receivers_array,main_message_str)

            smtp_server.quit()
            print("发送邮件成功")
        except smtplib.SMTPException:
            print("发送邮件失败")


