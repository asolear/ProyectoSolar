import streamlit as st

# modules
import imaplib
import email
import pandas as pd
import json
import subprocess
import time
from app_modelo import *
from app_utils import *


if 1 == 1:  # con privateemail
    smtp_server = "smtp.privateemail.com"

    port = 465  # For SSL
    # port = 587  # For starttls
    sender_email = "admin@asolear.es"
    password = "cscnrfff"


def ss_web2ss():
    if 1 == 1:

        ss.ii.proyecto['loc']["direccion"] = ss.ii.formulario_web_hogar["Value"]["direccion"]
        ss.ii.proyecto['loc']["lat"] = ss.ii.formulario_web_hogar["Value"]["lat"]
        ss.ii.proyecto['loc']["lon"] = ss.ii.formulario_web_hogar["Value"]["lon"]
        # ss.ii.inclinacion=ss.ii.formulario_web_hogar['Value']['inclinacion']
        # ss.ii.orientacion=ss.ii.formulario_web_hogar['Value']['orientacion']
        # ss.ii.sombra_hora_desde=ss.ii.formulario_web_hogar['Value']['sombra_hora_desde']
        # ss.ii.sombra_hora_hasta=ss.ii.formulario_web_hogar['Value']['sombra_hora_hasta']
        # ss.ii.sombras_mes=ss.ii.formulario_web_hogar['Value']['sombras_mes']
        # ss.ii.kWcontratad=ss.ii.formulario_web_hogar['Value']['kWcontratad']
        ss.ii.proyecto['general']["kWh"] = ss.ii.formulario_web_hogar["Value"]["kWh"]
        # ss.ii.CUPS=ss.ii.formulario_web_hogar['Value']['CUPS']
        # ss.ii.sector=ss.ii.formulario_web_hogar['Value']['sector']
        # ss.ii.proyecto['destinatario']['nombre']=ss.ii.formulario_web_hogar['Value']['destinatario_nombre']
        # ss.ii.proyecto['destinatario']['telefono']=ss.ii.formulario_web_hogar['Value']['destinatario_telefono']
        ss.ii.proyecto['destinatario']["email"] = ss.ii.formulario_web_hogar["Value"]["email"]
        # try:
        #     ss.ii.vehiculo=ss.ii.formulario_web_hogar['Value']['vehiculo']
        # except:
        #     None
        # try:
        #     ss.ii.aire=ss.ii.formulario_web_hogar['Value']['aire']
        # except:
        #     None
        # try:
        #     ss.ii.calor=ss.ii.formulario_web_hogar['Value']['calor']
        # except:
        #     None


def correo2envia_report():
    import email, smtplib, ssl
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    ss = st.session_state
    # if st.button('envia_correo'):
    if 1 == 1:
        if 1 == 1:  # con privateemail
            smtp_server = "smtp.privateemail.com"
            port = 587  # For starttls
            sender_email = "admin@asolear.es"
            password = "cscnrfff"
        print("!!!!!!!!!!!!!!!!! correo2envia_report")

        receiver_email = ss.ii.proyecto['destinatario']["email"]
        # st.write(receiver_email)
        email_destinatario = ss.ii.proyecto['destinatario']["email"]

        text = """ddd   """

        html = f"""\
        <html>
        <body>
            <p>Buenas, Se adjunta propuesta para AUTOCONSUMO. Gracias por elegirnos,<br>
            <br>
            <a href="https://asolear.es/">Asolear. Autoconsumo</a> 
            Contactenos o llame al 600 366 211 para cualquier duda.
            </p>
        </body>
        </html>
        """

        df = pd.read_json(
            json.dumps(ss.ii.formulario_web_hogar, indent=2), orient="records"
        )
        # st.dataframe(df)
        # html = df.to_html()
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        subject = "ASOLEAR.Autoconsumo (Propuesta)"

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        st.write(email_destinatario)
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Cc"] = sender_email  # Recommended for mass emails

        # Add body to email
        message.attach(part1)
        message.attach(part2)

        filename = "pdf/r01_portada_indice.pdf"  # In same directory as script

        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)


def correo2ss_web():
    #  funciona utilizando la directiva de FORMSUBMIT para qeu envie el correo como tabla
    import streamlit as st
    import imaplib
    import email
    import pandas as pd
    import time

    #
    ss = st.session_state

    imap_server = "imap.privateemail.com"
    sender_email = "admin@asolear.es"
    password = "cscnrfff"
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(sender_email, password)
    mail.select("INBOX")
    _, selected_mails = mail.search(None, '(FROM "submissions@formsubmit.co")')
    print(
        "Total Messages from submissions@formsubmit.co:", len(selected_mails[0].split())
    )
    # st.stop()
    for num in selected_mails[0].split():
        _, data = mail.fetch(num, "(RFC822)")
        _, bytes_data = data[0]
        # convert the byte data to message
        email_message = email.message_from_bytes(bytes_data)
        # access data
        # st.write("Subject: ",email_message["subject"])
        for part in email_message.walk():
            if (
                part.get_content_type() == "text/plain"
                or part.get_content_type() == "text/html"
            ):
                message = part.get_payload(decode=True)
                # st.write("Message: \n", message.decode())
                break
        # es una tabla que se puede leer con beutifulsoup y tambien con pandas
        dfs = pd.read_html(message.decode())
        df = dfs[0].copy()
        df = df.set_index("Name")
        #
        result = df.to_json(orient="columns")
        ss.ii.formulario_web_hogar = json.loads(df.to_json(orient="columns"))
        # st.write("\n===========================================")
        st.download_button(
            "Descargar_escenario ?",
            json.dumps(vars(ss.ii)),
            file_name=ss.ii.proyecto['loc']['referencia_catastral'] + ".json",
        )
        # st.write("\n===========================================")
        # st.dataframe(df)

        # para cada nuevo correo
        ss_web2ss()
        correo2envia_report()
        # despues de enviar el informe lo copia en ofertado y lo borra
        # correo_inbox2ofertado()
        mail.copy(num, "ofertado")
        time.sleep(1)
        mail.store(num, "+FLAGS", "\\Deleted")
        mail.expunge()


def email_attachs():
    # Import modules
    import smtplib, ssl

    ## email.mime subclasses
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    ### Add new subclass for adding attachments
    ##############################################################
    from email.mime.application import MIMEApplication

    ##############################################################
    ## The pandas library is only for generating the current date, which is not necessary for sending emails
    import pandas as pd

    # Define the HTML document
    html = """
        <html>
            <body>
                <h1>Daily S&P 500 prices report</h1>
                <p>Hello, welcome to your report!</p>
            </body>
        </html>
        """

    # Define a function to attach files as MIMEApplication to the email
    ##############################################################
    def attach_file_to_email(email_message, filename):
        # Open the attachment file for reading in binary mode, and make it a MIMEApplication class
        with open(filename, "rb") as f:
            file_attachment = MIMEApplication(f.read())
        # Add header/name to the attachments
        file_attachment.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        # Attach the file to the message
        email_message.attach(file_attachment)

    ##############################################################

    # Set up the email addresses and password. Please replace below with your email address and password
    email_from = "admin@asolear.es"
    password = "cscnrfff"
    email_to = "kgnete@gmail.com"

    # Generate today's date to be included in the email Subject
    date_str = pd.Timestamp.today().strftime("%Y-%m-%d")

    # Create a MIMEMultipart class, and set up the From, To, Subject fields
    email_message = MIMEMultipart()
    email_message["From"] = email_from
    email_message["To"] = email_to
    email_message["Subject"] = f"Report email - {date_str}"

    # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
    email_message.attach(MIMEText(html, "html"))

    # Attach more (documents)
    filename = "pdf/r01_portada_indice.pdf"
    ##############################################################
    attach_file_to_email(email_message, "pdf/r01_portada_indice.pdf")
    attach_file_to_email(email_message, "pdf/_plantilla_flow.pdf")
    attach_file_to_email(email_message, "pdf/Anexo_IB_DATOS_TECNICOS_Y_ECONOMICOS.pdf")
    ##############################################################
    # Convert it as a string
    email_string = email_message.as_string()

    # Connect to the Gmail SMTP server and Send Email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("imap.privateemail.com", 465, context=context) as server:
        server.login(email_from, password)
        server.sendmail(email_from, email_to, email_string)


def app():
    with st.expander("RESPUESTA AUTOMATICA", expanded=True):
        st.write(
            "automatico!!!! Si esa corriendo './tt.py' que mira el inbox periodicamente entonces  \
            cuando hay correo modifica la fecha escirta 'aaa.py' importado en stremlit.run para dispararlo"
        )
        correo2ss_web()

    with st.expander("RESPUESTA MANUAL", expanded=True):

        with st.form("my_form"):
            st.write("Enviar documentacion")
            receiver_email = st.text_input("Movie title", "")

            # Every form must have a submit button.
            submitted = st.form_submit_button("Enviar")
            if submitted:
                ss.ii.proyecto['destinatario']["email"] = receiver_email
                correo2envia_report()
                # send_mail(send_from, send_to, subject, text, files=None, server="smtp.privateemail.com")

        if st.button("TEST!!! kgnete@gmail.com "):
            ss.ii.proyecto['destinatario']["email"] = "kgnete@gmail.com"
            correo2envia_report()
        if st.button("TEST (varios ficheros)!!! kgnete@gmail.com "):
            ss.ii.proyecto['destinatario']["email"] = "kgnete@gmail.com"
            email_attachs()

    crea_pdf(os.path.dirname(__file__)+'/'+os.path.splitext(os.path.basename(__file__))[0]+'.pdf')