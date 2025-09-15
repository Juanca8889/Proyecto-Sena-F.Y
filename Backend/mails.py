import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib



load_dotenv()
email_MFY = "montallantasfy@gmail.com"
password = os.getenv("PASSWORD")
email_para = "sierra9camilo9@gmail.com"

header ="JCGS"
cuerpo ="""https://n9.cl/5as0hi"""


em = EmailMessage()
em["From"] = email_MFY
em["To"] = email_para
em["Subject"] = header
em.set_content(cuerpo)

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com",465,context = context) as smtp:
    smtp.login(email_MFY,password)
    smtp.sendmail(email_MFY,email_para,em.as_string())