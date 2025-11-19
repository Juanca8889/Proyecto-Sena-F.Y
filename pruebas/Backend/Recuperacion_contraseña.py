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
            
            header ="Recuperación de contraseña"
            cuerpo ="""Hola,

Recibimos una solicitud para restablecer tu contraseña. Para continuar con el proceso, haz clic en el siguiente enlace:

http://127.0.0.1:5000/recuperar_contraseña

Si tú no solicitaste este cambio, puedes ignorar este mensaje y tu cuenta permanecerá segura.

Gracias,
Soporte Técnico
                        """


            em = EmailMessage()
            em["From"] = email_MFY
            em["To"] = self.email_para
            em["Subject"] = header
            em.set_content(cuerpo)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com",465,context = context) as smtp:
                smtp.login(email_MFY,password)
                smtp.sendmail(email_MFY,self.email_para,em.as_string())
    
def actualizar_contrasena_usuario(nombre, celular, nueva_contrasena):
    conexion = conectar()
    cursor = conexion.cursor()

    # Verificar si el usuario y celular existen
    verificar_query = "SELECT * FROM Usuario WHERE Usuario = %s AND celular = %s"
    cursor.execute(verificar_query, (nombre, celular))
    usuario = cursor.fetchone()

    if usuario:
        # Actualizar contraseña usando SHA2 (512 bits)
        update_query = "UPDATE Usuario SET clave = UNHEX(SHA2(%s, 512)) WHERE Usuario = %s AND celular = %s"
        cursor.execute(update_query, (nueva_contrasena, nombre, celular))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    else:
        cursor.close()
        conexion.close()
        return False
