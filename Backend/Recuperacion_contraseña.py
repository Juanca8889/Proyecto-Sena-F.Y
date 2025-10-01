import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib
from BD.conexion import conectar

conexion = conectar()
cursor = conexion.cursor()


class recuperacion_contraseña: 
    def __init__(self, email):
        self.email_para = email


    def enviar_correo_verificacion(self):
            load_dotenv()
            email_MFY = "montallantasfy@gmail.com"
            password = os.getenv("PASSWORD")
            self.email_para
            
            header ="Correo de verificación"
            cuerpo ="""Para la recuperacion de su contraseña ingrese al siguiente enlace:
                        http://127.0.0.1:5000/recuperar_contraseña"""


            em = EmailMessage()
            em["From"] = email_MFY
            em["To"] = self.email_para
            em["Subject"] = header
            em.set_content(cuerpo)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com",465,context = context) as smtp:
                smtp.login(email_MFY,password)
                smtp.sendmail(email_MFY,self.email_para,em.as_string())
    
def actualizar_contrasena_usuario( nombre, nueva_contrasena):
    query = "UPDATE Usuario SET `clave` = UNHEX(SHA2(%s, 512)) WHERE Usuario = %s"
    values = (nueva_contrasena, nombre)
    cursor.execute(query, values)
    conexion.commit()
