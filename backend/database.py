import sqlite3
import uuid
from argon2 import PasswordHasher

class Database:

    conn = None
    cursor = None

    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()


    def creatTableUser(self):
        self.cursor.execute("DROP TABLE IF EXISTS user")
        table_creation_query = """
        CREATE TABLE user (
            userid TEXT NOT NULL PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            classname TEXT NOT NULL,
            major TEXT NOT NULL,
            email TEXT NOT NULL,
            teacherboolian INT NOT NULL
        );
        """
        self.cursor.execute(table_creation_query)
        self.conn.commit()
        return True


    def insertTestDataTableUser(self):
        testData = [
            [0,"Emil" , "Emil", "M4G", "B","test@test.ch", False],
            [0,"Nahia" , "Nahia", "M4G", "B","test@test.ch", False],
            [0,"Paul" , "Paul", "M4G", "W","test@test.ch", False],
            [0,"Esben" , "Esben", "M4G", "A","test@test.ch", False],
            [0,"Moritz" , "Moritz", "M4G", "A","test@test.ch", False],
            [0,"Manuel" , "Manuel", "M4G", "W","test@test.ch", False],
            [0,"Aurel" , "Aurel", "M4G", "W","test@test.ch", False],
            [0,"Loic" , "Loic", "M4G", "W","test@test.ch", False],
            [0,"Eliah" , "Eliah", "M4G", "A","test@test.ch", False],
            [0,"Walter" , "Walter", "M4G", "A","test@test.ch", False],
            [0,"Theo" , "Theo", "M4G", "A","test@test.ch", False],
            [0,"Marlon" , "Marlon", "M4G", "A","test@test.ch", False],
        ]

        ph = PasswordHasher()
        for row in testData:
            row[0] = str(uuid.uuid4())
            row[2] = ph.hash(row[2]) 

        stringRows_of_testData = ["""', '""".join(map(str, row)) for row in testData]

        for row in stringRows_of_testData:
            self.cursor.execute("""INSERT INTO user (userid,username,password,classname,major,email,teacherboolian) VALUES ('""" + row + "')""")

        self.conn.commit()
        return True



    def creatTableGrade(self):
        self.cursor.execute("DROP TABLE IF EXISTS grade")
        table_creation_query = """
        CREATE TABLE grade (
            userid TEXT NOT NULL,
            grade INT,
            subject TEXT NOT NULL,
            date TEXT NOT NULL,
            name TEXT NOT NULL,
            change_datum TEXT NOT NULL,
            message TEXT,
            fileid TEXT,
            weight INT NOT NULL
        );
        """
        self.cursor.execute(table_creation_query)
        self.conn.commit()
        return True

    def creatTableAbsence(self):
        self.cursor.execute("DROP TABLE IF EXISTS absence")
        table_creation_query = """
        CREATE TABLE absence (
            userid TEXT NOT NULL,
            subject TEXT NOT NULL,
            date TEXT NOT NULL,
            starttime TEXT NOT NULL,
            endtime TEXT NOT NULL,
            excused INT not NULL
        );
        """
        self.cursor.execute(table_creation_query)
        self.conn.commit()
        return True

    def creatTableSchedule(self):
        self.cursor.execute("DROP TABLE IF EXISTS schedule")
        table_creation_query = """
        CREATE TABLE schedule (
            teachername TEXT NOT NULL,
            subject TEXT NOT NULL,
            date TEXT NOT NULL,
            starttime TEXT NOT NULL,
            endtime TEXT NOT NULL,
            change INT not NULL,
            major TEXT NOT NULL
        );
        """
        self.cursor.execute(table_creation_query)
        self.conn.commit()
        return True

    def creatTableToken(self):
        self.cursor.execute("DROP TABLE IF EXISTS token")
        tableCreationQuery = """
        CREATE TABLE token (
            userid TEXT NOT NULL,
            token TEXT NOT NULL,
            creattime INTEGER NOT NULL
        );
        """
        self.cursor.execute(tableCreationQuery)
        self.conn.commit()
        return True

    def creatTableSubject(self):
        self.cursor.execute("DROP TABLE IF EXISTS subject")
        tableCreationQuery = """
        CREATE TABLE subject (
            listofteachers TEXT NOT NULL,
            name TEXT NOT NULL,
            listofstudents TEXT NOT NULL
        );
        """
        self.cursor.execute(tableCreationQuery)
        self.conn.commit()
        return True



    def creatTableFile(self):
        self.cursor.execute("DROP TABLE IF EXISTS file")
        tableCreationQuery = """
        CREATE TABLE file (
            fileid TEXT NOT NULL,
            namebefor TEXT NOT NULL,
            nameafter TEXT NOT NULL
        );
        """
        self.cursor.execute(tableCreationQuery)
        self.conn.commit()
        return True

    def passwordHashAndSalt(self,password):
        return password

    def addNewFile(self,nameOfFile):
        sql = "INSERT INTO file (fileid,namebefor,nameafter) VALUES (?,?,?)"

        fileId = str(uuid.uuid4())
        newFileName = str(uuid.uuid4())
        self.cursor.execute(sql, (fileId,nameOfFile,newFileName))
        output = self.cursor.fetchone()
        self.conn.commit()
        return fileId, newFileName

    def deleteFile(self,fileId):
        sql = "DELETE FROM file WHERE fileid = ?"
        self.cursor.execute(sql, (fileId,))
        output = self.cursor.fetchone()
        self.conn.commit()
        return True

    def getNamesOfFile(self,fileId):
        sql = "SELECT nameafter,namebefor FROM file WHERE fileid = ?"

        self.cursor.execute(sql, (fileId,))
        output = self.cursor.fetchone()
        self.conn.commit()
        nameBefor = output[0][0]
        nameAfter = output[0][1]

        
        return nameBefor, nameAfter

    def readAndReturnTableFile(self):
        self.cursor.execute("SELECT * FROM file")
        output = self.cursor.fetchall()
        self.conn.commit()
        return output



    def readAndReturnTableUser(self):
        self.cursor.execute("SELECT * FROM user")
        output = self.cursor.fetchall()
        self.conn.commit()
        return output

    def readAndReturnTableGrade(self):
        self.cursor.execute("SELECT * FROM grade")
        output = self.cursor.fetchall()
        self.conn.commit()
        return output

    def readAndReturnTableAbsence(self):
        self.cursor.execute("SELECT * FROM absence")
        output = self.cursor.fetchall()
        self.conn.commit()
        return output

    def readAndReturnTableSchedule(self):
        self.cursor.execute("SELECT * FROM schedule")
        output = self.cursor.fetchall()
        self.conn.commit()
        return output




    def isUserValid_getUserID(self, username, password):
        sql = "SELECT password,userid FROM user WHERE username = ?"
        self.cursor.execute(sql, (username,))
        output = self.cursor.fetchall()
        self.conn.commit()

        

        if output == []:
            return False


        ph = PasswordHasher()
        if not ph.verify(output[0][0], password):
            return False

        return output[0][1]

    def isUserExist(self,username):
        sql = "SELECT COUNT(*) FROM user WHERE username = ?"
        self.cursor.execute(sql, (username,))
        output = self.cursor.fetchone()
        self.conn.commit()

        if output[0] == 1:
            return True
        return False

    def addNewUser(self,username,password,classname,major):

        if isUserExist(username):
            return False


        sql = "INSERT INTO user (userid,username,password,classname,major) VALUES (?,?,?,?,?)"
        self.cursor.execute(sql, (str(uuid.uuid4),username,password,classname,major))
        output = self.cursor.fetchone()
        self.conn.commit()

        
        return True
        

    def addNewToken(self,userid):
        sql = "INSERT INTO token (userid,token,creattime) VALUES (?,?,strftime('%s', 'now'))"
        token = str(uuid.uuid4())


        self.cursor.execute(sql, (userid,token))
        output = self.cursor.fetchone()
        self.conn.commit()
        return token


    def getUseridFromToken(self,token):
        #funktion return False if no userid exist or the token is invalid

        countOfNumbersUntilTokenIsInvalid = 20
        sql = "SELECT * FROM token WHERE token = ? AND creattime > (strftime('%s', 'now') - ?*60)"
        self.cursor.execute(sql, (token,countOfNumbersUntilTokenIsInvalid))
        output = self.cursor.fetchall()
        self.conn.commit()


        if output == []:
            return False

        return output[0][0]


    def deletOldTokens(self):
        countOfNumbersUntilTokenIsInvalid = 20
        sql = "DELETE FROM tokens WHERE creattime < (strftime('%s', 'now') - ?*60"
        self.cursor.execute(sql, (countOfNumbersUntilTokenIsInvalid,))
        self.conn.commit()

    def deletToken(self,token):
        sql = "DELETE FROM tokens WHERE token = ?"
        self.cursor.execute(sql, (token,))
        self.conn.commit()




    """
    creatTableUser()
    insertTestDataTableUser()
    print(readAndReturnTableUser())

    print(isUserValid("Emil","Emil"))
    addNewUser("Gremaud","Gremaud","M4i","Lehrer MA")
    print(readAndReturnTableUser())

    print(isUserValid("Gremaud","Gremaud"))

    #creatTableToken()

    #addNewToken("eliah")


    print(getUseridFromToken("eliah"))
    #creatTableFile()


    print(readAndReturnTableFile())
    #deleteFile("d1072a26-6feb-44b0-bbec-843e00c387bb")
    print(readAndReturnTableFile())

    """

    #print(isUserValid_getUserID("Eliah","Eliah"))

db = Database()

db.creatTableUser()
db.insertTestDataTableUser()

print(db.readAndReturnTableUser())