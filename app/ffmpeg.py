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
        self._pidstream = None
        self._chave = None
        self.process = None
        self._pid = None

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
    
    def setprocess(self, name):
        self.process = name

    def getprocess(self):
        return self.process
    
    def setChave(self, name):
        self._chave = name

    def getChave(self):
        return self._chave
    
    def setpid(self, name):
        self._pid = name

    def getpid(self):
        return self._pid
    

    def start(self):

        instance_ffmpeg = FfmpegModel()
        instance_ffmpeg.setCaminho(task_manager)
        configuracao = instance_ffmpeg.select()

        instance_registro = Registro()
        instance_registro.setCaminho(task_manager)

        # Executar o comando e capturar a saída de depuração

        command = [
            "ffmpeg",
            "-stream_loop",
            "-1",
            "-f",
            "dshow",
            "-s",
            f"{configuracao[0]['largura']}x{configuracao[0]['altura']}",
            "-r",
            f"{configuracao[0]['fpd']}",
            "-i",
            f"video={self.getdevicevideo()}:audio={self.getdeviceaudio()}",
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-pix_fmt",
            "yuv420p",
            "-threads",
            "3",
            "-f",
            "flv",
            self.getrtmpurl(),
            self.getoutputfile()
        ]

        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

            self.setprocess(process)
            self.setpid(process.pid)

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

       
    

    # def encerrar(self):

        # return self.process.stdin

        # if self.process:
        #     try:
        #         self.process.stdin.write("q\n")
        #         self.process.stdin.flush()
        #         self.process.terminate()  # Encerre o processo
        #         self.process.wait()  # Aguarde até que o processo seja encerrado
        #         return 'Processo encerrado com sucesso'
        #     except Exception as e:
        #         return f'Erro ao encerrar o processo: {str(e)}'
        # else:
        #     return 'Nenhum processo em execução'

        # instance_registro = Registro()
        # instance_registro.setCaminho(task_manager)

        # pid =instance_registro.SelectPID(self.getChave())

        # try:
        #     subprocess.run(["taskkill", "/f", "/pid", str(pid)], check=True)
        #     return {"status": "200", "msg": f"Processo {self.getprocessname()} encerrado com sucesso."}
        # except subprocess.CalledProcessError:
        #     return {'status': "500", "msg": f"Não foi possível encerrar o processo {self.getprocessname()}."}
    

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
                if "Error opening output file" in line:
                    raise subprocess.CalledProcessError(1, command)
                elif "Error opening input files: I/O error" in line:
                    raise subprocess.CalledProcessError(1, command)
            
            process.wait()
            
            return 'gravação encerrado'
            
        except subprocess.CalledProcessError as e:

            return 'Erro ao gravar'