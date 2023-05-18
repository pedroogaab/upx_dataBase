import requests


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass





link = "https://firestore.googleapis.com/v1/projects/smart-pill-void/databases/(default)/documents/User/"
response = requests.get(link)

data = response.json()


# smtp_server = 'smtp.gmail.com'
# smtp_port = 587
# username = input("E-mail: ")
# password = getpass.getpass("Password: ", stream=None)




for i in data["documents"]:
    name = str(i["name"]).split('/')[-1]
    print(i)

    medicamentos = requests.get(link + str(name) + "/Medicamentos/")
    medicamentos_data = medicamentos.json()
    for k in medicamentos_data:
        
        data = medicamentos_data[k]
        
        logs = data[0]["fields"]["Enable"]["booleanValue"]
        
        last_pill = data[0]
        last_pill = last_pill["fields"]["log"]["mapValue"]["fields"]
        

        if logs == True:
            print("verdadeiro", logs)
            
            
        else: ...
            # # Criar uma mensagem de e-mail
            # msg = MIMEMultipart()
            # msg['From'] = username
            # msg['To'] = 'destinatario@example.com'
            # msg['Subject'] = 'Assunto do e-mail'
