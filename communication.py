import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass


def get_email_provider(email):
    smtp = str(email.split("@")[-1])
    if smtp == "gmail.com":
        return "smtp.gmail.com"
    elif smtp in ["outlook.com", "hotmail.com"]:
        return "smtp.office365.com"
    else:
        print("Provedor de e-mail não suportado: " + smtp)
        exit()


def get_medicamentos_data(user):
    link = "https://firestore.googleapis.com/v1/projects/smart-pill-void/databases/(default)/documents/User/"
    response = requests.get(link + str(user) + "/Medicamentos/")
    return response.json()


def send_email(email_origin, password, email_destiny, subject, message):
    msg = MIMEMultipart()
    msg["From"] = email_origin
    msg["To"] = email_destiny
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_origin, password)
        server.send_message(msg)
        print("\033[1;32;40mE-mail enviado com sucesso! \033[0;0m")


email_origin = input("\nE-mail: ")
smtp_server = get_email_provider(email_origin)
smtp_port = 587
password = getpass.getpass("Password: ", stream=None)


link = "https://firestore.googleapis.com/v1/projects/smart-pill-void/databases/(default)/documents/User/"
response = requests.get(link)
data = response.json()

for i in data["documents"]:
    user = str(i["name"]).split("/")[-1]
    name = str(i["fields"]["Name"]["stringValue"])
    first_name = name.split(" ")[0]
    email_destiny = str(i["fields"]["Email"]["stringValue"])

    medicamentos_data = get_medicamentos_data(user)
    precisa_tomar = []
    if medicamentos_data:
        for med in medicamentos_data["documents"]:
            remedio = med["name"]
            name_remedio = str(remedio).split("/")[-1]

            try:
                tomou = med["fields"]["log"]["arrayValue"]["values"][0]
                tomou = tomou["mapValue"]["fields"]["tomou"]["booleanValue"]

                if tomou is False:
                    precisa_tomar.append(name_remedio)
            except:
                print(f"Erro ao acessar o remedio '{name_remedio}' do {name}")

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
