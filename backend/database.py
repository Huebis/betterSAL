import sqlite3
import uuid


conn = sqlite3.connect('database.db')
cursor = conn.cursor()



def creatTableUser():
    cursor.execute("DROP TABLE IF EXISTS user")
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
    cursor.execute(table_creation_query)
    conn.commit()
    return True


def insertTestDataTableUser():
    testData = [
        [0,"Emil" , "Emil", "M4G", "B"],
        [0,"Nahia" , "Nahia", "M4G", "B"],
        [0,"Paul" , "Paul", "M4G", "W"],
        [0,"Esben" , "Esben", "M4G", "A"],
        [0,"Moritz" , "Moritz", "M4G", "A"],
        [0,"Manuel" , "Manuel", "M4G", "W"],
        [0,"Aurel" , "Aurel", "M4G", "W"],
        [0,"Loic" , "Loic", "M4G", "W"],
        [0,"Eliah" , "Eliah", "M4G", "A"],
        [0,"Walter" , "Walter", "M4G", "A"],
        [0,"Theo" , "Theo", "M4G", "A"],
        [0,"Marlon" , "Marlon", "M4G", "A"],
    ]
    for row in testData:
        row[0] = str(uuid.uuid4())

    stringRows_of_testData = ["""', '""".join(map(str, row)) for row in testData]

    for row in stringRows_of_testData:
        cursor.execute("""INSERT INTO user (userid,username,password,classname,major) VALUES ('""" + row + "')""")

    conn.commit()
    return True



def creatTableGrade():
    cursor.execute("DROP TABLE IF EXISTS grade")
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
    cursor.execute(table_creation_query)
    conn.commit()
    return True

def creatTableAbsence():
    cursor.execute("DROP TABLE IF EXISTS absence")
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
    cursor.execute(table_creation_query)
    conn.commit()
    return True

def creatTableSchedule():
    cursor.execute("DROP TABLE IF EXISTS schedule")
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
    cursor.execute(table_creation_query)
    conn.commit()
    return True

def creatTableToken():
    cursor.execute("DROP TABLE IF EXISTS token")
    tableCreationQuery = """
    CREATE TABLE token (
        userid TEXT NOT NULL,
        token TEXT NOT NULL,
        creattime INTEGER NOT NULL
    );
    """
    cursor.execute(tableCreationQuery)
    conn.commit()
    return True

def creatTableSubject():
    cursor.execute("DROP TABLE IF EXISTS subject")
    tableCreationQuery = """
    CREATE TABLE subject (
        listofteachers TEXT NOT NULL,
        name TEXT NOT NULL,
        listofstudents TEXT NOT NULL
    );
    """
    cursor.execute(tableCreationQuery)
    conn.commit()
    return True



def creatTableFile():
    cursor.execute("DROP TABLE IF EXISTS file")
    tableCreationQuery = """
    CREATE TABLE file (
        fileid TEXT NOT NULL,
        namebefor TEXT NOT NULL,
        nameafter TEXT NOT NULL
    );
    """
    cursor.execute(tableCreationQuery)
    conn.commit()
    return True

def addNewFile(nameOfFile):
    sql = "INSERT INTO file (fileid,namebefor,nameafter) VALUES (?,?,?)"

    fileId = str(uuid.uuid4())
    newFileName = str(uuid.uuid4())
    cursor.execute(sql, (fileId,nameOfFile,newFileName))
    output = cursor.fetchone()
    conn.commit()
    return fileId, newFileName

def deleteFile(fileId):
    sql = "DELETE FROM file WHERE fileid = ?"
    cursor.execute(sql, (fileId,))
    output = cursor.fetchone()
    conn.commit()
    return True

def getNamesOfFile(fileId):
    sql = "SELECT nameafter,namebefor FROM file WHERE fileid = ?"

    cursor.execute(sql, (fileId,))
    output = cursor.fetchone()
    conn.commit()
    nameBefor = output[0][0]
    nameAfter = output[0][1]

    
    return nameBefor, nameAfter

def readAndReturnTableFile():
    cursor.execute("SELECT * FROM file")
    output = cursor.fetchall()
    conn.commit()
    return output



def readAndReturnTableUser():
    cursor.execute("SELECT * FROM user")
    output = cursor.fetchall()
    conn.commit()
    return output

def readAndReturnTableGrade():
    cursor.execute("SELECT * FROM grade")
    output = cursor.fetchall()
    conn.commit()
    return output

def readAndReturnTableAbsence():
    cursor.execute("SELECT * FROM absence")
    output = cursor.fetchall()
    conn.commit()
    return output

def readAndReturnTableSchedule():
    cursor.execute("SELECT * FROM schedule")
    output = cursor.fetchall()
    conn.commit()
    return output




def isUserValid_getUserID(username, password):
    sql = "SELECT userid FROM user WHERE username = ? AND password = ?"
    cursor.execute(sql, (username, password))
    output = cursor.fetchall()
    conn.commit()

    if output == []:
        return False


    return output[0][0]

def isUserExist(username):
    sql = "SELECT COUNT(*) FROM user WHERE username = ?"
    cursor.execute(sql, (username,))
    output = cursor.fetchone()
    conn.commit()

    if output[0] == 1:
        return True
    return False

def addNewUser(username,password,classname,major):

    if isUserExist(username):
        return False


    sql = "INSERT INTO user (userid,username,password,classname,major) VALUES (?,?,?,?,?)"
    cursor.execute(sql, (str(uuid.uuid4),username,password,classname,major))
    output = cursor.fetchone()
    conn.commit()

    
    return True
    

def addNewToken(userid):
    sql = "INSERT INTO token (userid,token,creattime) VALUES (?,?,strftime('%s', 'now'))"
    token = str(uuid.uuid4())
    cursor.execute(sql, (userid,token))
    output = cursor.fetchone()
    conn.commit()
    return token


def getUseridFromToken(token):
    #funktion return False if no userid exist or the token is invalid

    countOfNumbersUntilTokenIsInvalid = 20
    sql = "SELECT * FROM token WHERE token = ? AND creattime > (strftime('%s', 'now') - ?*60)"
    cursor.execute(sql, (token,countOfNumbersUntilTokenIsInvalid))
    output = cursor.fetchall()
    conn.commit()


    if output == []:
        return False

    return output[0][0]


def deletOldTokens():
    countOfNumbersUntilTokenIsInvalid = 20
    sql = "DELETE FROM tokens WHERE creattime < (strftime('%s', 'now') - ?*60"
    cursor.execute(sql, (countOfNumbersUntilTokenIsInvalid,))
    conn.commit()





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

print(isUserValid_getUserID("Eliah","Eliah"))