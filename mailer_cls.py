import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

class Mailer:

    _instance = None

   
    def __new__(mlr, *args, **kwargs):
        if mlr._instance is None:
            mlr._instance = super().__new__(mlr)
        return mlr._instance

    def __init__(self,smtp_server,smtp_port,sender_email,sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
    
    def send_email(self,recipient_email,mail_subject,mail_body,filePath):

       
    
        file_name = os.path.splitext(os.path.basename(filePath))[0]
        file_extension = os.path.splitext(os.path.basename(filePath))[1]

        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = recipient_email
        msg["Subject"] = mail_subject
        msg.attach(MIMEText(mail_body,'plain'))

        with open(filePath, 'rb') as attachment:
            part = MIMEApplication(attachment.read(), Name=f"{file_name}.{file_extension}")
            part['Content-Disposition'] = f'attachment; filename="{file_name}.{file_extension}"'
            msg.attach(part)
        
        # Connect to SMTPS server and send the email using SSL
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, recipient_email, msg.as_string())
        
        return 0



