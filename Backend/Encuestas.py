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
            
            header ="Tu opinión es muy importante para nosotros"
            cuerpo ="""Hola,

Gracias por confiar en nuestros servicios. Para nosotros es fundamental mejorar cada día y tu opinión nos ayuda a hacerlo.

Te invitamos a responder una breve encuesta que no te tomará más de 2 minutos:

https://n9.cl/5as0hi.

Agradecemos mucho tu tiempo y tus comentarios.

Saludos cordiales,
Tu equipo de atención"""


            em = EmailMessage()
            em["From"] = email_MFY
            em["To"] = self.email_para
            em["Subject"] = header
            em.set_content(cuerpo)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com",465,context = context) as smtp:
                smtp.login(email_MFY,password)
                smtp.sendmail(email_MFY,self.email_para,em.as_string())
                
                
                
                
                
                