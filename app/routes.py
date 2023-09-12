from flask import jsonify, send_file, request
from app import app, checkedFoldarData as folder_data, task_manager
from app.model.dispositivo import Dispositivo
from app.model.conexao import Conexao
from app.model.ffmpef import Ffmpeg as FfmpegModel
from app.ffmpeg import Ffmpeg
from app.model.paciente import Paciente
import requests
import subprocess
import re
import random
import string
import json
import os


@app.route('/')
def index():
    return 'Página inicial'

@app.route('/record_and_stream', methods=['POST'])
def stream():
    
    data = request.json

    device_video = 'USB Video'
    device_audio = 'Microfone (Realtek High Definition Audio)'  # Nome do dispositivo de áudio
    output_file = f'{folder_data}\\{data["chave"]}.mkv'  # Nome do arquivo de saída
    rtmp_url = f'rtmp://172.16.2.2:1935/live/{data["chave"]}'  # URL RTMP
    
    instance_ffmpeg = Ffmpeg()
    instance_ffmpeg.setdevicevideo(device_video)
    instance_ffmpeg.setdeviceaudio(device_audio)
    instance_ffmpeg.setoutputfile(output_file)
    instance_ffmpeg.setrtmpurl(rtmp_url)

    instance_modelPaciente = Paciente()
    instance_modelPaciente.setCaminho(task_manager)
    instance_modelPaciente.insert(data['pacienteid'])

    return jsonify(instance_ffmpeg.start())


@app.route('/stream/encerrar')
def streamEncerrar():
    
    process_name = 'ffmpeg.exe'
    instance_ffmpeg = Ffmpeg()
    instance_ffmpeg.setprocessname(process_name)

    return jsonify(instance_ffmpeg.encerrar())
    

@app.route('/dispositivos', methods=['POST'])
def dispositivos():

    instance_modelDispositivo = Dispositivo()
    instance_modelDispositivo.setCaminho(task_manager)
   

    array = []
   # Comando FFmpeg para listar dispositivos
    ffmpeg_command = [
        "ffmpeg",
        "-list_devices",
        "true",
        "-f",
        "dshow",
        "-i",
        "dummy"
    ]

    # Executa o comando e captura a saída
    try:
        output = subprocess.check_output(ffmpeg_command, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e}")
        output = e.output  # Captura a saída de erro

    # Verifica se há saída
    if output:
        # Usar regex para encontrar os nomes entre as aspas duplas
        nomes_dispositivos = re.findall(r'"([^"]*)"', output)

        # Imprime os nomes dos dispositivos
        for nome in nomes_dispositivos:
            # array.append(nome)
            if nome.split('@')[0] != "":
                
                nameDispositivo = nome.split('@')[0]

                if not instance_modelDispositivo.select(nameDispositivo):

                    array.append({'name': nome.split('@')[0], 'selected': False})

                else:

                     array.append({'name': nome.split('@')[0], 'selected': 'selected'})

        # Você agora tem os nomes dos dispositivos em 'nomes_dispositivos'

    else:
        array.append(0)


    return jsonify(array)

@app.route('/download-video', methods=['POST'])
def sendVideo():

    data = request.json
    
    file = data['chave']

    video_path = f'{folder_data}\\{file}.mp4'
    return send_file(video_path, as_attachment=True)

@app.route('/converte', methods=['POST'])
def converte():

    data = request.json

    input_file = f"{folder_data}\\{data['name_file']}.mkv"
    output_file = f"{folder_data}\\{data['name_file']}.mp4"

    command = ["ffmpeg", "-i", input_file, output_file]

    try:
        subprocess.run(command, check=True)

        if os.path.exists(input_file):
            os.remove(input_file)

        print("Conversão concluída com sucesso.")
    except subprocess.CalledProcessError as e:
        print("Erro durante a conversão:", e)

    
    return 'sucesso'

@app.route('/gerarchave', methods=['POST'])
def gerarchave():

    tamanho = 9
    sequencia_aleatoria = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(tamanho))

    return jsonify(sequencia_aleatoria)

@app.route('/sendmensagem', methods=['POST'])
def sendmensagem():
    
    url = "http://localhost:3000/sendMensage"
    data = request.json

    payload = json.dumps({
        "celular": data['celular'],
        "pacienteid": data['pacienteid'],
        "chave": data['chave']
    })
    
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except requests.exceptions.ConnectionError as e:
        print(e)
        return jsonify({"erro": "Nenhuma conexão pôde ser feita porque a máquina de destino as recusou ativamente"})

    try:
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"A solicitação falhou com o código de status: {response.status_code}"})
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Ocorreu um erro de rede ao fazer a solicitação: {str(e)}"})
    except Exception as e:
         return jsonify({"error": f"Ocorreu um erro desconhecido: {str(e)}"})

@app.route('/path')
def path():
    return jsonify(data)

@app.route('/updateDispositivo', methods=['POST'])
def config(): 

    data = request.json

    dispositivo = data['dispositivo']

    instance_modelDispositivo = Dispositivo()
    instance_modelDispositivo.setCaminho(task_manager)

    if data['tipo'] == "video":
        return jsonify(instance_modelDispositivo.updateVideo(dispositivo))
    else:
        return jsonify(instance_modelDispositivo.updateAudio(dispositivo))

@app.route('/ffmpeg',  methods=['POST'])
def ffmpeg():

    instance_modelFfmpeg = FfmpegModel()
    instance_modelFfmpeg.setCaminho(task_manager)

    return jsonify(instance_modelFfmpeg.select())

@app.route('/ffmpeg/edit',  methods=['POST'])
def ffmpegEdit():

    data = request.json

    instance_modelFfmpeg = FfmpegModel()
    instance_modelFfmpeg.setCaminho(task_manager)

    if data['tipo'] == "fps":
        return jsonify(instance_modelFfmpeg.updateFps(data['valor']))
    elif data['tipo'] == "codec":
        return jsonify(instance_modelFfmpeg.updateCodec(data['valor']))
    elif data['tipo'] == "texabitsaudio":
        return jsonify(instance_modelFfmpeg.updatexabitsaudio(data['valor']))
    elif data['tipo'] == "taxmostraudio":
        return jsonify(instance_modelFfmpeg.taxmostraudio(data['valor']))
    elif data['tipo'] == "altura":
        return jsonify(instance_modelFfmpeg.resolucaoaltura(data['valor']))
    elif data['tipo'] == "largura":
        return jsonify(instance_modelFfmpeg.resolucaolargura(data['valor']))


@app.route('/conexao',  methods=['POST'])
def conexao():

    instance_modelConexao = Conexao()
    instance_modelConexao.setCaminho(task_manager)

    return jsonify(instance_modelConexao.select())


@app.route('/conexao/edit',  methods=['POST'])
def conexaoedit():

    instance_modelConexao = Conexao()
    instance_modelConexao.setCaminho(task_manager)
   
    data = request.json

    if data['tipo'] == "rmtp":
        return jsonify(instance_modelConexao.updateRmtp(data['valor']))
    else:
        return jsonify(instance_modelConexao.updateservidorPrincipal(data['valor']))


@app.route('/getNuuvem',  methods=['POST'])
def nuuvem():

    instance_modelConexao = Conexao()
    instance_modelConexao.setCaminho(task_manager)

    return jsonify(instance_modelConexao.select())


@app.route('/uploadFile',  methods=['POST'])
def uploadFile():

    data = request.json

    url = "http://172.16.2.2:3000/getvideo/babe/stream"

    payload = json.dumps({
        "chave": data['chave']
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    return 'teste'

    


    

