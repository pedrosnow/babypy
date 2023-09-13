from app import app, task_manager, checkedFoldarData as folder_data
from app.model.registro import Registro
import os
import subprocess
import json
import time
import requests
from threading import Thread

# Defina a função que executará o código em um loop infinito com intervalo de 5 minutos
def execute_code():
    
    instance_modelRegistro = Registro()
    instance_modelRegistro.setCaminho(task_manager)

    while True:
    
        for row in instance_modelRegistro.selectTeste():
             
            chave = row['chave']

            input_file = os.path.join(folder_data, f"{chave}.mkv")
            output_file = os.path.join(folder_data, f"{chave}.mp4")

            if os.path.isfile(input_file):
                input_file_size = os.path.getsize(input_file)
                if input_file_size == 0:
                    os.remove(input_file)

                    erro = "Erro: o arquivo de entrada está vazio."
                    instance_modelRegistro.updateErro(chave, erro)

                command = ["ffmpeg", "-i", input_file, output_file]
                try:
                    subprocess.run(command, check=True)
                    if os.path.exists(output_file):
                        if os.path.exists(input_file):
                            os.remove(input_file)
                        
                            url = "http://172.16.2.2:3000/getvideo/babe/stream"

                            payload = json.dumps({
                                "chave": chave
                            })
                            headers = {
                                'Content-Type': 'application/json'
                            }

                            response = requests.request("POST", url, headers=headers, data=payload)

                            if response.text == "sucesso":

                                instance_modelRegistro.update(chave)
                                
                                video_path = f'{folder_data}\\{chave}.mp4'

                                if os.path.exists(video_path):
                                    os.remove(video_path)                          
                    else:

                        erro = "Erro: o arquivo de saída não foi criado."
                        instance_modelRegistro.updateErro(chave, erro)
                    
                except subprocess.CalledProcessError as e:

                    erro = "Erro durante a conversão:" + e
                    instance_modelRegistro.updateErro(chave, erro)
                    
            else:

                erro = "Erro: o arquivo de entrada não foi encontrado."
                instance_modelRegistro.updateErro(chave, erro)
            
                print("Erro: o arquivo de entrada não foi encontrado.")
            
                
        # Aguarde 5 minutos antes de executar novamente
        time.sleep(180)

# Rota para iniciar o loop em segundo plano quando o servidor estiver online
@app.route('/start_loop')
def start_loop():
    # Crie uma thread para executar a função em segundo plano
    loop_thread = Thread(target=execute_code)
    loop_thread.daemon = True  # Isso permite que a thread seja interrompida quando o programa principal terminar
    loop_thread.start()
    
    return "Loop iniciado em segundo plano."


if __name__ == '__main__':
    app.run()
    