import sqlite3

class Conexao():
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
            cursor.execute(f"SELECT * FROM tb_conexao")
            all = cursor.fetchall()
            for row in all:
                array.append({
                    'rmtp': row[1],
                    'home': row[2],
                })

            return array
        
    def updateRmtp(self, name):
        with sqlite3.connect(self.getCaminho()) as connection:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE tb_conexao SET servidor_rmtp = '{name}' WHERE id = 1")
            return 'sucesso'
    
    def updateservidorPrincipal(self, name):
        with sqlite3.connect(self.getCaminho()) as connection:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE tb_conexao SET servidor_principal = '{name}' WHERE id = 1")
            return 'sucesso'
         
        
      