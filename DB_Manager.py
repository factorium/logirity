import sqlite3
from datetime import  datetime
class SQLITEDB:

    def __init__(self):

        self.connection = sqlite3.connect('Trucks')
        self.cursor = self.connection.cursor()
        self.__create_table()

    def __create_table(self):

        comandoCriar = "CREATE TABLE IF NOT EXISTS dados (id INTEGER AUTO_INCREMENT PRIMARY KEY," \
                       " placa TEXT," \
                       " data TEXT, " \
                       "permissao INTEGER)"

        self.cursor.execute(comandoCriar)

    def put_info(self, plate, permission=0):

        id = self.__maxId() + 1
        data = datetime.now()
        data = str(data)
        sql = f"INSERT INTO dados VALUES({id}, '{plate}', '{data}', {permission})"
        self.cursor.execute(sql)
        self.connection.commit()

    def get_data(self, plate):

        sql = f"SELECT * FROM dados WHERE placa == '{plate}'"
        self.cursor.execute(sql)

        resultados = self.cursor.fetchall()
        print(resultados)

    def update(self):

        self.cursor.execute("UPDATE dados SET data = 1 WHERE id = 1")
        self.connection.commit()

    def delete(self):

        self.cursor.execute("DELETE FROM dados WHERE id > 10")
        self.connection.commit()

    def __maxId(self):

        self.cursor.execute('SELECT MAX (id) FROM dados')

        maxId = self.cursor.fetchone()

        if maxId[0] == None:
            maxId = 0
        else:
            maxId = maxId[0]

        return maxId

#-----------------------------------------------------------------------------------------------------------------------

myDB = SQLITEDB()

#myDB.delete()
#myDB.put_info("JOAO-123")
#myDB.update()
#myDB.get_data("JOAO-123")
