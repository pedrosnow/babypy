from flask import jsonify, send_file, request
from app import app, checkedFoldarData as folder_data, task_manager
from app.model.dispositivo import Dispositivo
from app.model.conexao import Conexao
from app.model.ffmpef import Ffmpeg as FfmpegModel
from app.model.registro import Registro
from app.file import File
from app.ffmpeg import Ffmpeg
import requests
import subprocess
import re
import random
import string
import json
import os
import datetime



@app.route('/processo/verificar',  methods=['POST'])
def verificarProcesso():

    instance_model = Registro()
    instance_model.setCaminho(task_manager)

    return jsonify(instance_model.select())

@app.route('/')
def index():
   
    return 'Página inicial'

@app.route('/record_and_stream', methods=['POST'])
def stream():
    
    instance_dispositivo = Dispositivo()
    instance_dispositivo.setCaminho(task_manager)
    configuracao = instance_dispositivo.select()

    instance_conexao = Conexao()
    instance_conexao.setCaminho(task_manager)
    configuracaoConexao = instance_conexao.select()

    data = request.json

    device_video = configuracao[0]['video']
    device_audio = configuracao[1]['audio']  # Nome do dispositivo de áudio
    output_file = f'{folder_data}\\{data["chave"]}.mkv'  # Nome do arquivo de saída
    rtmp_url = f'{configuracaoConexao[0]["rmtp"]}/live/{data["chave"]}'  # URL RTMP

    pacienteid = data['pacienteid']
    chave = data["chave"]
    file = f'{data["chave"]}.mp4'
    enviado = 0
    date = datetime.datetime.now()

    instance_ffmpeg = Ffmpeg()
    instance_ffmpeg.setdevicevideo(device_video)
    instance_ffmpeg.setdeviceaudio(device_audio)
    instance_ffmpeg.setoutputfile(output_file)
    instance_ffmpeg.setrtmpurl(rtmp_url)
    instance_ffmpeg.setChave(data["chave"])

    instance_model = Registro()
    instance_model.setCaminho(task_manager)
    instance_model.insert(pacienteid,chave,file,enviado,date)
    responseStart = instance_ffmpeg.start()

    if responseStart == "Erro ao iniciar a live":
        if os.path.exists(output_file):
            os.remove(output_file)
        
        erro = "Erro: Erro ao iniciar a live"
        instance_modelRegistro = Registro()
        instance_modelRegistro.setCaminho(task_manager)
        instance_modelRegistro.updateErro(chave, erro)

    return jsonify(responseStart)

@app.route('/stream/encerrar', methods=['POST'])
def streamEncerrar():

    data = request.json
    
    process_name = 'ffmpeg.exe'
    instance_ffmpeg = Ffmpeg()
    instance_ffmpeg.setprocessname(process_name)
    instance_ffmpeg.setChave(data['chave'])

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

                if not instance_modelDispositivo.checked(nameDispositivo):

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


@app.route('/gerarchave', methods=['POST'])
def gerarchave():

    tamanho = 9
    sequencia_aleatoria = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(tamanho))

    return jsonify(sequencia_aleatoria)

@app.route('/sendmensagem', methods=['POST'])
def sendmensagem():

    instance_conexao = Conexao()
    instance_conexao.setCaminho(task_manager)
    serverBebe = instance_conexao.select()
  
    
    url = f"{serverBebe[0]['home']}/sendMensage"
    data = request.json

    payload = json.dumps({
        "celular": data['celular'],
        "pacienteid": data['pacienteid'],
        "chave": data['chave']
    })
    
    headers = {
        'authorization': serverBebe[0]['token'],
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
    return jsonify(folder_data)

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


@app.route('/gravando', methods=['POST'])
def gravando():

    data = request.json

    instance_dispositivo = Dispositivo()
    instance_dispositivo.setCaminho(task_manager)
    configuracao = instance_dispositivo.select()

    device_video = configuracao[0]['video']
    device_audio = configuracao[1]['audio']  # Nome do dispositivo de áudio
    output_file = f'{folder_data}\\{data["chave"]}.mkv'  # Nome do arquivo de saída

    pacienteid = data['pacienteid']
    chave = data["chave"]
    file = f'{data["chave"]}.mp4'
    enviado = 0
    date = datetime.datetime.now()

    instance_ffmpeg = Ffmpeg()
    instance_ffmpeg.setdevicevideo(device_video)
    instance_ffmpeg.setdeviceaudio(device_audio)
    instance_ffmpeg.setoutputfile(output_file)

    instance_model = Registro()
    instance_model.setCaminho(task_manager)
    instance_model.insert(pacienteid,chave,file,enviado,date)

    responseStart =instance_ffmpeg.gravar()

    if responseStart == "Erro ao gravar":
        if os.path.exists(output_file):
            os.remove(output_file)
        
        erro = "Erro: Erro ao gravar"
        instance_modelRegistro = Registro()
        instance_modelRegistro.setCaminho(task_manager)
        instance_modelRegistro.updateErro(chave, erro)

        return jsonify({'status': 500,'msg': "Erro ao iniciar o processo"})

    return jsonify({'status': 200,'msg': "processo encerrado"})


@app.route('/converte', methods=['POST'])
def converte():

    data = request.json

    instance_modelRegistro = Registro()
    instance_modelRegistro.setCaminho(task_manager)

    input_file = f"{folder_data}\\{data['chave']}.mkv"
    output_file = f"{folder_data}\\{data['chave']}.mp4"

    if os.path.isfile(input_file):
        input_file_size = os.path.getsize(input_file)
        if input_file_size == 0:
            os.remove(input_file)
            erro = "Erro: o arquivo de entrada está vazio."
            instance_modelRegistro.updateErro(data['chave'], erro)
            return jsonify({'status':785, 'msg': "o arquivo de entrada está vazio"})
        
        command = ["ffmpeg", "-i", input_file, output_file]
    
    try:
        subprocess.run(command, check=True)

        if os.path.exists(input_file):
             os.remove(input_file)


        uploadFile(data['chave'], data['acesso'])
        # return jsonify({'status':200, 'msg': "Conversão concluída com sucesso."})
    
    except subprocess.CalledProcessError as e:

        erro = "Erro durante a conversão:" + e
        instance_modelRegistro.updateErro(data['chave'], erro)

        return jsonify({'status':500, 'msg': "Erro durante a conversão"})
    

def uploadFile(chave, acesso):

    try:

        instance_conexao = Conexao()
        instance_conexao.setCaminho(task_manager)
        serverBebe = instance_conexao.select()

        instance_modelRegistro = Registro()
        instance_modelRegistro.setCaminho(task_manager)
    
        data = request.json

        url = f"{serverBebe[0]['home']}/getvideo/babe/stream"

        payload = json.dumps({
            "chave": chave,
            "serverStream": serverBebe[0]['stream'],
            'acesso': acesso
        })

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.text == "sucesso":
            instance_modelRegistro.update(chave)

            video_path = f'{folder_data}\\{chave}.mp4'
            nameFile = f'{chave}.mp4'

            instance_file = File()
            instance_file.insertApi(nameFile, acesso)

            if os.path.exists(video_path):
                os.remove(video_path)     

        return jsonify({"status": 200, "msg": "Sucesso", "result": response.text})
    
    except Exception as e:
        
        return jsonify({'status': 500, 'msg': "Erro", "result": e})


