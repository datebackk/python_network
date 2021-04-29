import sqlite3
import random

conn = sqlite3.connect("database.db")
cursor = conn.cursor()


class Database:

    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()
        self.default = " WHERE id = 1"
        try:
            self.cursor.execute("""CREATE TABLE server
                              (id number UNIQUE, public number, private number)
                           """)
            self.cursor.execute("""CREATE TABLE client
                                  (id number UNIQUE, public number, private number)
                               """)
            self.conn.commit()
        except:
            pass

        try:
            self.cursor.execute("INSERT INTO server (id) values (1)")
            self.cursor.execute("INSERT INTO client (id) values (1)")
            self.conn.commit()
        except:
            pass

    def getServerPublicKey(self, key):
        sql = "SELECT public FROM server" + self.default
        sql1 = f'UPDATE server SET public = {key}' + self.default

        self.cursor.execute(sql)

        if self.cursor.fetchone()[0]:
            return self.cursor.fetchone()[0]
        else:
            self.cursor.execute(sql1)
            self.conn.commit()
            return key


    def getServerPrivateKey(self):
        sql = "SELECT private FROM server" + self.default
        newKey = random.randint(1, 20)
        sql1 = f'UPDATE server SET private = {newKey}' + self.default
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchone()[0]
        except:
            self.cursor.execute(sql1)
            self.conn.commit()
            return newKey



    def getClientPublicKey(self, key):
        sql = "SELECT public FROM client" + self.default
        sql1 = f'UPDATE client SET public = {key}' + self.default

        self.cursor.execute(sql)

        if self.cursor.fetchone()[0]:
            return self.cursor.fetchone()[0]
        else:
            self.cursor.execute(sql1)
            self.conn.commit()
            return key

    def getClientPrivateKey(self):
        sql = "SELECT private FROM client" + self.default
        newKey = random.randint(1, 20)
        sql1 = f'UPDATE client SET private = {newKey}' + self.default
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchone()[0]
        except:
            self.cursor.execute(sql1)
            self.conn.commit()
            return newKey


database = Database()
