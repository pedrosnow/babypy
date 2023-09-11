import sqlite3

class Config():
    def __init__(self) -> None:
        pass

    def setCaminho(self, name):
        self._caminho = name
        
    def getCaminho(self):
        return self._caminho

    def select(self):
         with sqlite3.connect(self.getCaminho()) as connection:
            cursor = connection.cursor()
            # cursor.execute(f"SELECT * FROM tb_medicos as m WHERE m.CRM = {request.form.get('crm')}")
            cursor.execute(f"SELECT * FROM rb_config")
            query = cursor.fetchall()
            return query