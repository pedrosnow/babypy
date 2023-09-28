import sqlite3

class taskmanager():
    def __init__(self):
        self._caminho = None
        
    def setCaminho(self, name):
        self._caminho = name
        
    def getCaminho(self):
        return self._caminho
    

    def createTableConexao(self):
        conexao = sqlite3.connect(self.getCaminho())
        cursor = conexao.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS tb_conexao ( id INTEGER PRIMARY KEY, servidor_rmtp VARCHAR(50) NULL, servidor_principal VARCHAR(50) NULL, token VARCHAR(50) NULL, servidor_stream VARCHAR(50) NULL, workstation VARCHAR(50) NULL)')
        conexao.commit()
        conexao.close()
    
    def createTabledispositivo(self):
        conexao = sqlite3.connect(self.getCaminho())
        cursor = conexao.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS tb_dispositivo ( id INTEGER PRIMARY KEY, video VARCHAR(50) NULL, audio VARCHAR(50) NULL)')
        conexao.commit()
        conexao.close()
    
    def createTableFfmpeg(self):
        conexao = sqlite3.connect(self.getCaminho())
        cursor = conexao.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS tb_ffmpeg ( id INTEGER PRIMARY KEY, resolucao_largura INTEGER NULL, resolucao_altura INTEGER NULL, taxa_mostragem_audio VARCHAR(50) NULL, taxa_bits_audio VARCHAR(50) NULL, codec_audio VARCHAR(50) NULL, fps VARCHAR(50) NULL)')
        conexao.commit()
        conexao.close()
    
    def createTableFfmpeg(self):
        conexao = sqlite3.connect(self.getCaminho())
        cursor = conexao.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS tb_registro (id INTEGER PRIMARY KEY, pacienteid INTEGER NULL, chave TEXT NULL, arquivo TEXT NULL, enviado TINYINT NULL, create_at DATETIME NULL, msg_erro TEXT NULL, erro TINYINT NULL, pid INTEGER NULL)')
        conexao.commit()
        conexao.close()



    def InsertdadosPadrao(self):
        conexao = sqlite3.connect(self.getCaminho())
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO tb_ffmpeg (resolucao_largura, resolucao_altura, fps) VALUES ('1280','720','30')")
        conexao.commit()
        conexao.close()
    
