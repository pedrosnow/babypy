import sqlite3

class Ffmpeg():
    def __init__(self) -> None:
        pass

    def setCaminho(self, name):
        self._caminho = name
        
    def getCaminho(self):
        return self._caminho

    def select(self):
        
        array = []
        with sqlite3.connect(self.getCaminho()) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM tb_ffmpeg")
            all = cursor.fetchall()

            for row in all:
                array.append({
                    'largura': row[1],
                    'altura': row[2],
                    'taxa_mostragem_audio': row[3],
                    'taxa_bits_audio': row[4],
                    'codec_audio': row[5],
                    'fpd': row[6],
                })

        return array
    
    def updateFps(self, name):

        with sqlite3.connect(self.getCaminho()) as connection:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE tb_ffmpeg SET fps = '{name}' WHERE id = 1")
            return 'sucesso'
    
    def updateCodec(self, name):

        with sqlite3.connect(self.getCaminho()) as connection:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE tb_ffmpeg SET codec_audio = '{name}' WHERE id = 1")
            return 'sucesso'
    
    def updatexabitsaudio(self, name):

        with sqlite3.connect(self.getCaminho()) as connection:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE tb_ffmpeg SET taxa_bits_audio = '{name}' WHERE id = 1")
            return 'sucesso'
    
    def taxmostraudio(self, name):

        with sqlite3.connect(self.getCaminho()) as connection:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE tb_ffmpeg SET taxa_mostragem_audio = '{name}' WHERE id = 1")
            return 'sucesso'
    
    def resolucaoaltura(self, name):

        with sqlite3.connect(self.getCaminho()) as connection:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE tb_ffmpeg SET resolucao_altura = '{name}' WHERE id = 1")
            return 'sucesso'
    
    def resolucaolargura(self, name):

        with sqlite3.connect(self.getCaminho()) as connection:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE tb_ffmpeg SET resolucao_largura = '{name}' WHERE id = 1")
            return 'sucesso'
         



            
        
      