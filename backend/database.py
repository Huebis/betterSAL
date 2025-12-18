import sqlite3
import uuid




def creatTableUser():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS user")
    table_creation_query = """
    CREATE TABLE user (
        userid TEXT NOT NULL PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        classname TEXT NOT NULL,
        major TEXT NOT NULL
    );
    """
    cursor.execute(table_creation_query)
    conn.commit()
    return True




def creatTableGrade():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS grade")
    table_creation_query = """
    CREATE TABLE grade (
        userid TEXT NOT NULL,
        grade INT NOT NULL,
        subject TEXT NOT NULL,
        date TEXT NOT NULL,
        name TEXT NOT NULL,
        change TEXT NOT NULL,
        message TEXT
    );
    """
    cursor.execute(table_creation_query)
    conn.commit()
    return True

def creatTableAbsence():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
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
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS schedule")
    table_creation_query = """
    CREATE TABLE schedule (
        lessonname TEXT NOT NULL,
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
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
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

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    for row in stringRows_of_testData:
        cursor.execute("""INSERT INTO user (userid,username,password,classname,major) VALUES ('""" + row + "')""")

    conn.commit()
    conn.close()
    return True


def readAndReturnTableUser():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user")
    output = cursor.fetchall()
    conn.commit()
    conn.close()
    return output

def readAndReturnTableGrade():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grade")
    output = cursor.fetchall()
    conn.commit()
    conn.close()
    return output

def readAndReturnTableAbsence():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM absence")
    output = cursor.fetchall()
    conn.commit()
    conn.close()
    return output

def readAndReturnTableSchedule():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM schedule")
    output = cursor.fetchall()
    conn.commit()
    conn.close()
    return output

def isUserValid(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    sql = "SELECT COUNT(*) FROM user WHERE username = ? AND password = ?"
    cursor.execute(sql, (username, password))
    output = cursor.fetchone()
    conn.commit()
    conn.close()

    if output[0] == 1:
        return True
    return False

def isUserExist(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    sql = "SELECT COUNT(*) FROM user WHERE username = ?"
    cursor.execute(sql, (username,))
    output = cursor.fetchone()
    conn.commit()
    conn.close()

    if output[0] == 1:
        return True
    return False

def addNewUser(username,password,classname,major):

    if isUserExist(username):
        return False


    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    sql = "INSERT INTO user (userid,username,password,classname,major) VALUES (?,?,?,?,?)"
    cursor.execute(sql, (str(uuid.uuid4),username,password,classname,major))
    output = cursor.fetchone()
    conn.commit()
    conn.close()

    
    return True
    

def addNewToken(userid):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    sql = "INSERT INTO token (userid,token,creattime) VALUES (?,?,strftime('%s', 'now'))"
    cursor.execute(sql, (userid,str(uuid.uuid4())))
    output = cursor.fetchone()
    conn.commit()
    conn.close()



def getUseridFromToken(token):
    #funktion return False if no userid exist or the token is invalid

    countOfNumbersUntilTokenIsInvalid = 20
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    sql = "SELECT * FROM token WHERE token = ? AND creattime > (strftime('%s', 'now') - ?*60)"
    cursor.execute(sql, (token,countOfNumbersUntilTokenIsInvalid))
    output = cursor.fetchall()
    conn.commit()
    conn.close()

    if output == []:
        return False

    return output[0][0]


def deletOldTokens():
    countOfNumbersUntilTokenIsInvalid = 20
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    sql = "DELETE FROM tokens WHERE creattime < (strftime('%s', 'now') - ?*60"
    cursor.execute(sql, (countOfNumbersUntilTokenIsInvalid,))
    conn.commit()
    conn.close()




"""
creatTableUser()
insertTestDataTableUser()
print(readAndReturnTableUser())

print(isUserValid("Emil","Emil"))
addNewUser("Gremaud","Gremaud","M4i","Lehrer MA")
print(readAndReturnTableUser())

print(isUserValid("Gremaud","Gremaud"))
"""
#creatTableToken()

#addNewToken("eliah")


print(getUseridFromToken("eliah"))
