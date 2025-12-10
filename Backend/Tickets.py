import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib
import mysql.connector
from BD.conexion import conectar


class Tickets:

    def __init__(self, cuerpo, header, estado="Pendiente"):
        self.cuerpo = cuerpo
        self.header = header
        self.estado = estado


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

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465,
            context=context
        ) as smtp:
            smtp.login(email_MFY,password)
            smtp.sendmail(
                email_MFY,
                email_para,
                em.as_string()
            )


    # ✅ Guarda ticket en MySQL
    def guardar_ticket(self):

        con = conectar()
        cursor = con.cursor()

        sql = """
            INSERT INTO tickets (problema, descripcion, estado)
            VALUES (%s,%s,%s)
        """

        cursor.execute(sql,(
            self.header,
            self.cuerpo,
            self.estado
        ))

        con.commit()
        cursor.close()
        con.close()


    # ✅ Obtener todos los tickets
    @staticmethod
    def obtener_tickets():

        con = conectar()
        cursor = con.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM tickets
            ORDER BY fecha DESC
        """)

        tickets = cursor.fetchall()

        cursor.close()
        con.close()

        return tickets


    # ✅ Cambiar estado
    @staticmethod
    def cambiar_estado(id_ticket):

        con = conectar()
        cursor = con.cursor()

        cursor.execute("""
            UPDATE tickets
            SET estado='Atendida'
            WHERE id_ticket=%s
        """,(id_ticket,))

        con.commit()
        cursor.close()
        con.close()
