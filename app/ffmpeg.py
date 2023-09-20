import subprocess
from app.model.ffmpef import Ffmpeg as FfmpegModel
from app.model.registro import Registro
from app import task_manager

class Ffmpeg():
    
    def __init__(self):
        self._devicevideo = None
        self._deviceaudio = None
        self._outputfile = None
        self._rtmpurl = None
        self._processname = None
        self._pidstream = None
        self._chave = None

    def setdevicevideo(self, name):
        self._devicevideo = name
    
    def getdevicevideo(self):
        return self._devicevideo
    
    def setdeviceaudio(self, name):
        self._deviceaudio = name

    def getdeviceaudio(self):
        return self._deviceaudio
    
    def setoutputfile(self, name):
        self._outputfile = name
    
    def getoutputfile(self):
        return self._outputfile
    
    def setrtmpurl(self, name):
        self._rtmpurl = name

    def getrtmpurl(self):
        return self._rtmpurl
    
    def setprocessname(self, name):
        self._processname = name

    def getprocessname(self):
        return self._processname
    
    def setpidStream(self, name):
        self._pidstream = name
    
    def getpidStream(self):
        return self._pidstream
    
    def setChave(self, name):
        self._chave = name

    def getChave(self):
        return self._chave

    

    def start(self):

        instance_ffmpeg = FfmpegModel()
        instance_ffmpeg.setCaminho(task_manager)
        configuracao = instance_ffmpeg.select()

        instance_registro = Registro()
        instance_registro.setCaminho(task_manager)

        chaveNone = self.getoutputfile()
        chaveNone.split('.')
        chave = chaveNone[0]
        
        # Comando FFmpeg
        command = [
            "ffmpeg",
            "-y",
            "-loglevel",
            "debug",
            "-f",
            "dshow",
            "-i",
            f"video={self.getdevicevideo()}:audio={self.getdeviceaudio()}",
             "-s",
            f"{configuracao[0]['largura']}x{configuracao[0]['altura']}",
            "-r",
            f"{configuracao[0]['fpd']}",
            "-threads",
            "3",
            "-vcodec",
            "libx264",
            "-f",
            "flv",
            self.getrtmpurl(),  # URL RTMP
           "-c:a",
            f"{configuracao[0]['codec_audio']}",  # Codec de áudio AAC
            "-strict",
            "2",
            "-ar",
            f"{configuracao[0]['taxa_mostragem_audio']}",  # Taxa de amostragem de áudio
            "-b:a",
            f"{configuracao[0]['taxa_bits_audio']}",  # Taxa de bits de áudio
            self.getoutputfile()  # Nome do arquivo de saída
        ]

        # Executar o comando e capturar a saída de depuração
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

            ffmpeg_pid = process.pid
            instance_registro.updatePID(self.getChave(), ffmpeg_pid)

            for line in process.stdout:
                # print(line.strip())
                if "Error opening output file" in line:
                    raise subprocess.CalledProcessError(1, command)
                elif "Error opening input files: I/O error" in line:
                    raise subprocess.CalledProcessError(1, command)
            process.wait()

            return 'Live encerrado'
        
        except subprocess.CalledProcessError as e:
            # Handle the error here
            print(f"Error: {e}")
            return f'Erro ao iniciar a live'

       
    

    def encerrar(self):

        instance_registro = Registro()
        instance_registro.setCaminho(task_manager)

        pid =instance_registro.SelectPID(self.getChave())

        try:
            subprocess.run(["taskkill", "/f", "/pid", str(pid)], check=True)
            return {"status": "200", "msg": f"Processo {self.getprocessname()} encerrado com sucesso."}
        except subprocess.CalledProcessError:
            return {'status': "500", "msg": f"Não foi possível encerrar o processo {self.getprocessname()}."}
    

    def gravar(self):

        instance_ffmpeg = FfmpegModel()
        instance_ffmpeg.setCaminho(task_manager)
        configuracao = instance_ffmpeg.select()

        command = [
            "ffmpeg",
            "-y",
            "-loglevel",
            "debug",
            "-f",
            "dshow",
            "-i",
            f"video={self.getdevicevideo()}:audio={self.getdeviceaudio()}",
            "-s",
            f"{configuracao[0]['largura']}x{configuracao[0]['altura']}",
            "-r",
            f"{configuracao[0]['fpd']}",
            "-threads",
            "3",
            "-vcodec",
            "libx264",
            self.getoutputfile()  # Nome do arquivo de saída
        ]

        # Executar o comando
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            for line in process.stdout:
                print(line.strip())
                if "Error opening output file" in line:
                    raise subprocess.CalledProcessError(1, command)
                elif "Error opening input files: I/O error" in line:
                    raise subprocess.CalledProcessError(1, command)
            
            process.wait()
            
            return 'gravação encerrado'
            
        except subprocess.CalledProcessError as e:

            return 'Erro ao gravar'