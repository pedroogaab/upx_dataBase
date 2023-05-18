import requests


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass





# link = "https://firestore.googleapis.com/v1/projects/smart-pill-void/databases/(default)/documents/User/"
# response = requests.get(link)

# data = response.json()


email = input("E-mail: ")
smtp = email.split("@")[-1]
smtp_server = 'smtp.' + str(smtp)
smtp_port = 587
password = getpass.getpass("Password: ", stream=None)



msg = MIMEMultipart()
msg['From'] = email
msg['To'] = 'plechi_2016@hotmail.com'
msg['Subject'] = 'Teste'

msg.attach(MIMEText('Olá, este é um e-mail enviado pelo Python!', 'plain'))


with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(email, password)
    server.send_message(msg)
    print('E-mail enviado com sucesso!')




# for i in data["documents"]:
#     name = str(i["name"]).split('/')[-1]
#     print(i)

#     medicamentos = requests.get(link + str(name) + "/Medicamentos/")
#     medicamentos_data = medicamentos.json()
#     for k in medicamentos_data:
        
#         data = medicamentos_data[k]
        
#         logs = data[0]["fields"]["Enable"]["booleanValue"]
        
#         last_pill = data[0]
#         last_pill = last_pill["fields"]["log"]["mapValue"]["fields"]
        

#         if logs == True:
#             print("verdadeiro", logs)
            
            
#         else: ...
            # # Criar uma mensagem de e-mail