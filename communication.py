import requests


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass

from datetime import datetime
import pytz


link = "https://firestore.googleapis.com/v1/projects/smart-pill-void/databases/(default)/documents/User/"
response = requests.get(link)

data = response.json()


email_origin = input("E-mail: ")
smtp = str(email_origin.split("@")[-1])
if smtp == "gmail.com":
    smtp_server = "smtp.gmail.com"
elif smtp in ["outlook.com", "hotmail.com"]:
    smtp_server = "smtp.office365.com"
else:
    print("Provedor de e-mail não suportado: " + smtp)
    exit()


smtp_port = 587
password = getpass.getpass("Password: ", stream=None)


for i in data["documents"]:
    user = str(i["name"]).split("/")[-1]

    name = str(i["fields"]["Name"]["stringValue"])
    first_name = name.split(" ")[0]

    email_destiny = str(i["fields"]["Email"]["stringValue"])

    medicamentos = requests.get(link + str(user) + "/Medicamentos/")
    medicamentos_data = medicamentos.json()

    msg = MIMEMultipart()
    msg["From"] = email_origin
    msg["To"] = email_destiny
    msg["Subject"] = f"{first_name}, você precisa tomar seu remedio"

    for k in medicamentos_data:
        data = medicamentos_data[k]

        local = pytz.timezone("America/Sao_Paulo")

        moment = datetime.now(local)
        moment = moment.strftime("%D às %H:%M")

        remedio = str(data[0]["name"]).split("/")[-1]

        logs = data[0]["fields"]["Enable"]["booleanValue"]

        # last_pill = data[0]
        # last_pill = last_pill["fields"]["log"]["mapValue"]["fields"]

        if logs == False:
            msg.attach(
                MIMEText(f"Olá {name}, você precisa tomar o seu {remedio}", "plain")
            )
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(email_origin, password)
                server.send_message(msg)
                print("E-mail enviado com sucesso!")

        else:
            ...
