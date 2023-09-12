import sqlite3

class Paciente():
    def __init__(self) -> None:
        pass

    def setCaminho(self, name):
        self._caminho = name
        
    def getCaminho(self):
        return self._caminho

    
    def insert(self, pacienteid):

        with sqlite3.connect(self.getCaminho()) as connection:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO tb_paciente (pacienteid) VALUES ('{pacienteid}')")
            return 'sucesso'
    
   
