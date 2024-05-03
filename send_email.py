import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

def send (email,nombre,fecha,hora,servicio,empleado):
    
    # Create the email message
    msg = MIMEMultipart()

    #Alternative css

    css_style_alternative = """
        <style>
            /* Add your custom styles here */
            body {
                font-family: Arial, sans-serif;
                background-color: #222222;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                text-align: center;
                margin-bottom: 20px;
            }
            .header img {
                max-width: 200px;
                height: auto;
            }
            .content {
                background-color: #333333;
                padding: 30px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
            .content h1 {
                color: #ffffff;
                font-size: 24px;
                margin-bottom: 20px;
            }
            .content p {
                color: #cccccc;
                font-size: 16px;
                line-height: 1.5;
            }
            .cta-button {
                display: inline-block;
                background-color: #007bff;
                color: #ffffff;
                text-decoration: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
                margin-top: 20px;
            }
        </style>
    """

    html_mensaje= f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Barberia de barrio</title>
        <style>
            /* Add your custom styles here */
        {css_style_alternative}
        </style>
    </head>
    <body>
        <div style="background-color: #f2f2f2; padding: 20px;">
            <h1 style="text-align: center;">Barberia de barrio</h1>
            <hr>
            <p>Estimado {nombre},</p>
            <p>Esperamos que se encuentre bien. Queremos confirmar la cita que ha solicitado en nuestra peluquería. Agradecemos la confianza que ha depositado en nuestros servicios y estamos ansiosos por atenderle.

            Detalles de la cita:</p>

            <p>Fecha: {fecha}</p>
            <p>Hora: {hora}</p>
            <p>Servicio Solicitado: {servicio}</p>
            <p>Peluquero(a) Asignado(a): {empleado}</p>
            <p>Ubicación: Jiron Mariano Soto Mz N4 Lt5, Urb. Mariscal Caceres</p>
           <p> Por favor, recuerde llegar unos minutos antes de su cita para que podamos ofrecerle el mejor servicio posible. Si necesita cancelar o reprogramar la cita por alguna razón, le agradecemos que nos contacte con anticipación.

            Si tiene alguna pregunta o inquietud antes de la cita, no dude en ponerse en contacto con nosotros a través de 920187327 o barberiadebarrio@gmail.com. Estamos aquí para ayudarle.</p>

            <p> ¡Esperamos poder brindarle una experiencia excepcional en nuestra peluquería!</p>

            <p>Atentamente,</p>
            <p>El Equipo de Barberia de barrio</p>
            <p>920187327</p>
           <p> barberiadebarrio@gmail.com</p>
           <p> https://topicnurse.streamlit.app/</p>
                
            <hr>
            <p>Saludos cordiales,</p>
            <p>Barberia de barrio</p>
        </div>
    </body>
    </html>


    """

    # Attach the HTML content to the email
    msg.attach(MIMEText(html_mensaje, 'html'))

    # SMTP server configuration
    smtp_server = 'smtp.gmail.com'
    #smtp_server = "smtp-mail.outlook.com"
    smtp_port = 587

    smtp_username = st.secrets['db_credencial']['smpt_username']    #["db_credentials"]["smtp_username"]
    smtp_password = st.secrets['db_credencial']['smpt_password']    #["db_credentials"]["smtp_password"]

    # Email configuration
    sender_email = f'Barberia de Barrio'
    subject = f'Cita {nombre}'
    msg['From'] = sender_email
    msg['Subject'] = subject

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        # Send the email
        msg['To'] = email
        server.sendmail(sender_email, email, msg.as_string())            
            
        server.quit()

    except smtplib.SMTPException as e:
        st.warning("Ha habido un error con el envío de correo de confirmación de cita.")
        print("Error envío de correo: ",e)