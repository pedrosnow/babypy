import sqlite3

class Registro():
    def __init__(self) -> None:
        pass

    def setCaminho(self, name):
        self._caminho = name
        
    def getCaminho(self):
        return self._caminho

    def update(self, chave):
         with sqlite3.connect(self.getCaminho()) as connection:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE tb_registro SET enviado = 1 WHERE chave = '{chave}'")
            return 'sucesso'
   
    def updateErro(self, chave, erro):
         with sqlite3.connect(self.getCaminho()) as connection:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE tb_registro SET enviado = 0, erro = 1, msg_erro = '{erro}' WHERE chave = '{chave}'")
            return 'sucesso'
    
    def insert(self, pacienteid, chave, file, enviado, date):

        with sqlite3.connect(self.getCaminho()) as connection:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO tb_registro (pacienteid,chave,arquivo,enviado,create_at) VALUES ('{pacienteid}','{chave}','{file}','{enviado}','{date}')")
            return 'sucesso'
    
    def select(self):
        array = []
        with sqlite3.connect(self.getCaminho()) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM tb_registro as r WHERE r.enviado = 0 AND r.erro = 0")
            for row in cursor.fetchall():
                array.append({
                    'pacienteid': row[1],
                    'chave': row[2],
                    'arquivo': row[3],
                    'enviado': row[4],
                    'create_at': row[5],
                })
            
            return array
   
    def selectTeste(self):
        array = []
        with sqlite3.connect(self.getCaminho()) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM tb_registro as r WHERE r.enviado = 0 AND r.erro = 0 LIMIT 1")            
            for row in cursor.fetchall():
                array.append({
                    'pacienteid': row[1],
                    'chave': row[2],
                    'arquivo': row[3],
                    'enviado': row[4],
                    'create_at': row[5],
                    'msg_erro': row[6],
                    'erro': row[7],
                })
            
            return array
