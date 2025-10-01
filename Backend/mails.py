import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib
from Backend.Clientes import ConexionClientes





class Encuestas: 
    def __init__(self,email_MFY = "montallantasfy@gmail.com", id_cliente = None):
        self.email_para = ConexionClientes.buscar_correo_usuario(id_cliente)

    def enviar_correo(email_para):
            load_dotenv()
            email_MFY = "montallantasfy@gmail.com"
            password = os.getenv("PASSWORD")
            email_para = ""
            
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