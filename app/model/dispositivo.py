import sqlite3

class Dispositivo():
    def __init__(self) -> None:
        pass

    def setCaminho(self, name):
        self._caminho = name
        
    def getCaminho(self):
        return self._caminho

    def select(self, name):
        
        with sqlite3.connect(self.getCaminho()) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM tb_dispositivo where video = '{name}'")
            all = cursor.fetchall()
            if(len(all) != 0):
                return True


    def updateVideo(self, name):
         with sqlite3.connect(self.getCaminho()) as connection:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE tb_dispositivo SET video = '{name}' WHERE id = 1")
            return 'sucesso'
   
    def updateAudio(self, name):
         with sqlite3.connect(self.getCaminho()) as connection:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE tb_dispositivo SET audio = '{name}' WHERE id = 2")
            return 'sucesso'

            
        
      