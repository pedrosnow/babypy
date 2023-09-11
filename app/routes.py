from flask import jsonify, send_file, request
import requests
from app import app, checkedFoldarData as data
import subprocess
import re
import time
import random
import string
import json

@app.route('/')
def index():
    return 'Página inicial'

@app.route('/record_and_stream')
def stream():
    
    device_video = 'USB Video'
    device_audio = 'Microfone (Realtek High Definition Audio)'  # Nome do dispositivo de áudio
    output_file = 'output.mkv'  # Nome do arquivo de saída
    rtmp_url = 'rtmp://172.16.2.2:1935/live/tutorial'  # URL RTMP

    # Comando FFmpeg
    command = [
        "ffmpeg",
        "-y",
        "-loglevel",
        "debug",
        "-f",
        "dshow",
        "-i",
        f"video={device_video}:audio={device_audio}",
        "-s",
        "1280x720",
        "-r",
        "30",
        "-threads",
        "2",
        "-vcodec",
        "libx264",
        "-f",
        "flv",
        rtmp_url,  # URL RTMP
        "-c:a",
        "aac",  # Codec de áudio AAC
        "-strict",
        "2",
        "-ar",
        "44100",  # Taxa de amostragem de áudio
        "-b:a",
        "128k",  # Taxa de bits de áudio
        output_file  # Nome do arquivo de saída
    ]

    # Executar o comando e capturar a saída de depuração
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for line in process.stdout:
            print(line.strip())
            if "Error opening output file" in line:
                raise subprocess.CalledProcessError(1, command)
        process.wait()
        
    except subprocess.CalledProcessError as e:

        time.sleep(5)
        
        command = [
            "ffmpeg",
            "-y",
            "-loglevel",
            "debug",
            "-f",
            "dshow",
            "-i",
            f"video={device_video}",
            "-s",
            "1280x720",
            "-r",
            "30",
            "-threads",
            "2",
            "-vcodec",
            "libx264",
            output_file
        ]

        # Executar o comando
        try:
            process = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
            for line in process.stdout:
                print(line.strip())
            
        except subprocess.CalledProcessError as e:
            print('ERRO')
            print(f"Erro ao executar o FFmpeg: {e.output}")

    return 'Online'

@app.route('/stream/encerrar')
def streamEncerrar():
    
    process_name = 'ffmpeg.exe'
    
    try:
        subprocess.run(["taskkill", "/f", "/t", "/im", process_name], check=True)
        print(f"Processo {process_name} encerrado com sucesso.")
    except subprocess.CalledProcessError:
        print(f"Não foi possível encerrar o processo {process_name}.")
    
    return 'encerrado'

@app.route('/dispositivos')
def dispositivos():

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
                array.append(nome.split('@')[0])

        # Você agora tem os nomes dos dispositivos em 'nomes_dispositivos'

    else:
        array.append("Nenhum dispositivo DirectShow encontrado.")


    return f'{array}'

@app.route('/download-video')
def sendVideo():

    video_path = 'C:/Users/udi/Documents/meu bebe/BabyPy/output.mp4'
    return send_file(video_path, as_attachment=True)

@app.route('/converte')
def converte():

    input_file = "input.mp4"
    output_file = "output.avi"

    command = ["ffmpeg", "-i", input_file, output_file]

    try:
        subprocess.run(command, check=True)
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
