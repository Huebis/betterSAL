import database
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import uuid



db = database.Database()


def insertTestDataTableUserAndCourse(db):
    testData = [
            [0,"Emil" , "Emil", "M4G", "B","test@test.ch", 1],
            [0,"Nahia" , "Nahia", "M4G", "B","test@test.ch", 1],
            [0,"Paul" , "Paul", "M4G", "W","test@test.ch", 1],
            [0,"Esben" , "Esben", "M4G", "A","test@test.ch", 1],
            [0,"Moritz" , "Moritz", "M4G", "A","test@test.ch", 1],
            [0,"Manuel" , "Manuel", "M4G", "W","test@test.ch", 1],
            [0,"Aurel" , "Aurel", "M4G", "W","test@test.ch", 1],
            [0,"Loic" , "Loic", "M4G", "W","test@test.ch", 1],
            [0,"Eliah" , "Eliah", "M4G", "A","test@test.ch", 1],
            [0,"Walter" , "Walter", "M4G", "A","test@test.ch", 1],
            [0,"Theo" , "Theo", "M4G", "A","test@test.ch", 1],
            [0,"Marlon" , "Marlon", "M4G", "A","test@test.ch", 1],
            [0, "Anklin", "Anklin", "M4G", "", "test@test.ch",2],
            [0, "Zulauf", "Zulauf", "", "", "test@test.ch",2],
            [0, "admin", "admin", "", "", "test@test.ch",5]
        ]

    ph = PasswordHasher()

    FranzösischM4GcourseID = str(uuid.uuid4())
    EnglischM4GcourseID = str(uuid.uuid4())


    for row in testData:
        row[2] = ph.hash(row[2]) 
        row[0] = db.addNewUser(row[1],row[2],row[3],row[4],row[5],row[6])

        if(row[6] == 1 or row[1] == "Anklin"):
            print("hello")
            db.addNewCourse(FranzösischM4GcourseID,row[0],"F","F-M4G-26")
        if(row[6] == 1 or row[1] == "Zulauf"):
            db.addNewCourse(EnglischM4GcourseID,row[0],"E","E-M4G-26")
    

    return True


db.creatTableUser()
db.creatTableToken()
db.creatTableAbsence()
db.creatTableFile()
db.creatTableSchedule()
db.creatTableGrade()
db.creatTableCourse()
db.creatTableExamen()
db.creatTableEvent()

insertTestDataTableUserAndCourse(db)
