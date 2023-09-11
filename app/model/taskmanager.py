import sqlite3

class taskmanager():
    def __init__(self):
        self._caminho = None
        
    def setCaminho(self, name):
        self._caminho = name
        
    def getCaminho(self):
        return self._caminho
    

    # def createTableConfig(self):

    #     conexao = sqlite3.connect(self.getCaminho())
    #     cursor = conexao.cursor()

    #     cursor.execute('''
    #         CREATE TABLE IF NOT EXISTS tb_config(
    #             id INTEGER PRIMARY KEY,
    #             nome VARCHAR(255)
    #         )
    #     ''')

    #     conexao.commit()
    #     conexao.close()
        
    #     return 'Criando data'