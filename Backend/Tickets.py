import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib


class Tickets:
    def __init__(self,cuerpo,header):
        self.cuerpo = cuerpo
        self.header = header


    def enviar_ticket(self):
            load_dotenv()
            email_MFY = "montallantasfy@gmail.com"
            password = os.getenv("PASSWORD")
            email_para = "sierra9camilo9@gmail.com"
            
            em = EmailMessage()
            em["From"] = email_MFY
            em["To"] = email_para
            em["Subject"] = self.header
            em.set_content(self.cuerpo)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com",465,context = context) as smtp:
                smtp.login(email_MFY,password)
                smtp.sendmail(email_MFY,email_para,em.as_string())