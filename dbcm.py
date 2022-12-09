import sqlite3

class DBCM():

    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):

        self.connect = sqlite3.connect(self.connection)
        self.cursor = self.connect.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace):
        self.connect.commit()
        self.cursor.close()
        self.connect.close()

