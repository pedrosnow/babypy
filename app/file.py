from app import task_manager
import requests
import json
from app.model.conexao import Conexao

class File():
    
    def insertApi(self, fileName, acesso):

        instance_conexao = Conexao()
        instance_conexao.setCaminho(task_manager)
        serverBebe = instance_conexao.select()

        url = f"{serverBebe[0]['home']}/insert/file"

        payload = json.dumps({
            "acesso": str(acesso),
            "file": str(fileName)
        })
        headers = {
            'authorization': serverBebe[0]['token'],
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

