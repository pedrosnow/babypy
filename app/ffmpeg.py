import subprocess

class Ffmpeg():
    
    def __init__(self):
        self._devicevideo = None
        self._deviceaudio = None
        self._outputfile = None
        self._rtmpurl = None
        self._processname = None

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
    

    def start(self):
        
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
            "1280x720",
            "-r",
            "30",
            "-threads",
            "2",
            "-vcodec",
            "libx264",
            "-f",
            "flv",
            self.getrtmpurl(),  # URL RTMP
           "-c:a",
            "aac",  # Codec de áudio AAC
            "-strict",
            "2",
            "-ar",
            "44100",  # Taxa de amostragem de áudio
            "-b:a",
            "128k",  # Taxa de bits de áudio
            self.getoutputfile()  # Nome do arquivo de saída
        ]

        # Executar o comando e capturar a saída de depuração
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            for line in process.stdout:
                print(line.strip())
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

        try:
            subprocess.run(["taskkill", "/f", "/t", "/im", self.getprocessname()], check=True)
            return {"status": "200", "msg": f"Processo {self.getprocessname()} encerrado com sucesso."}
        except subprocess.CalledProcessError:
            return {'status': "500", "msg": f"Não foi possível encerrar o processo {self.getprocessname()}."}
    

    def gravar(self):

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
            "1280x720",
            "-r",
            "30",
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