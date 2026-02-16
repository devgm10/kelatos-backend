import os
import smtplib
from email.message import EmailMessage

def send_email(to_email: str, category: str, summary: str):

    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")

    subject_map = {
        "Ventas": "Gracias por tu interés en nuestros servicios.",
        "Soporte": "Hemos recibido tu solicitud de soporte.",
        "Información": "Infomación solicitada.",
        "Spam": "Mensaje recibido."
    }

    body_map = {
        "Ventas": "Nuestro equipo comercial te contactará pronto.",
        "Soporte": "Nuestro equipo de soporte ya está revisando tu caso.",
        "Información": "Gracias por tu interés. Te enviaremos más detalles pronto.",
        "Spam": "Hemos recibido tu mensaje."
    }

    msg = EmailMessage()
    msg["From"] = email_user
    msg["To"] = to_email
    msg["Subject"] = subject_map.get(category, "Mensaje recibido")

    msg.set_content(f"""
    Hola,
    
    Resumen de tu mensaje:
    '{summary}'

    {body_map.get(category, "")}

    Saludos,
    Equipo de Atención Kelatos.
    """)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_user, email_pass)
        smtp.send_message(msg)