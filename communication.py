import requests

link = "https://firestore.googleapis.com/v1/projects/smart-pill-void/databases/(default)/documents/User/"
response = requests.get(link)

data = response.json()

for i in data["documents"]:
    name = str(i["name"]).split('/')[-1]
    print(name)

    medicamentos = requests.get(link + str(name) + "/Medicamentos/")
    medicamentos_data = medicamentos.json()
    for k in medicamentos_data:
        
        data = medicamentos_data[k]
        
        logs = data[0]["fields"]["Enable"]["booleanValue"]
        
        last_pill = data[0]
        last_pill = last_pill["fields"]["log"]["mapValue"]["fields"]
        print(last_pill)

        # if logs == True:
        #     print("verdadeiro", logs)
            
        # else: print("falso", logs)