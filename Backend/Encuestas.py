import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib
from Backend.Clientes import ConexionClientes



class Encuestas: 
    def __init__(self, correo):
        self.email_para = correo

    def enviar_correo(self):
            load_dotenv()
            email_MFY = "montallantasfy@gmail.com"
            password = os.getenv("PASSWORD")
            self.email_para
            
            header ="JCGS"
            cuerpo ="""Por favor te invitamos a responder una encuesta de satisfaccion,
por medio del siguiente link :https://n9.cl/5as0hi.

Gracias por tu tiempo y preferencia."""


            em = EmailMessage()
            em["From"] = email_MFY
            em["To"] = self.email_para
            em["Subject"] = header
            em.set_content(cuerpo)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com",465,context = context) as smtp:
                smtp.login(email_MFY,password)
                smtp.sendmail(email_MFY,self.email_para,em.as_string())