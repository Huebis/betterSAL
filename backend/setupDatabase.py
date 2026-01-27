import database
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import uuid



db = database.Database()


def insertTestDataTableUserAndCourse(db):
    testData = [
            [0,"Eliah" , "Eliah", "M4G", "A","test@test.ch", 1],
            [0,"Emil" , "Emil", "M4G", "B","test@test.ch", 1],
            [0,"Nahia" , "Nahia", "M4G", "B","test@test.ch", 1],
            [0,"Paul" , "Paul", "M4G", "W","test@test.ch", 1],
            [0,"Esben" , "Esben", "M4G", "A","test@test.ch", 1],
            [0,"Moritz" , "Moritz", "M4G", "A","test@test.ch", 1],
            [0,"Manuel" , "Manuel", "M4G", "W","test@test.ch", 1],
            [0,"Aurel" , "Aurel", "M4G", "W","test@test.ch", 1],
            [0,"Loic" , "Loic", "M4G", "W","test@test.ch", 1],
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
            #print("hello")
            db.addNewCourse(FranzösischM4GcourseID,row[0],"F","F-M4G-26")
        if(row[6] == 1 or row[1] == "Zulauf"):
            db.addNewCourse(EnglischM4GcourseID,row[0],"E","E-M4G-26")
    
    # [[testname, weight, changedatum, grade, message]]

    testGradesfuerEliahFranzösisch = [
    ["Contrôle de mathématiques", 0.3, "2024-04-12", 1, "Bon travail"],
    ["Examen de physique", 0.4, "2024-05-20", 2, "Résultats satisfaisants"],
    ["Projet d'informatique", 0.2, "2024-06-10", 3, "Excellent projet"],
    ["Test de chimie", 0.1, "2024-03-25", 4, "Des lacunes importantes"],
    ["Examen final de statistiques", 0.5, "2024-07-05", 5, "Très bonne compréhension"]
    ]

    testGradesfuerEliahEnglisch = [
    ["Math Exam", 0.3, "2024-04-12", 6, "Good overall performance"],
    ["Physics Test", 0.4, "2024-05-20", 5.35, "Satisfactory results"],
    ["Computer Science Project", 0.2, "2024-06-10", 3.14159 , "Excellent work"],
    ["Chemistry Quiz", 0.1, "2024-03-25", 2.718, "Needs improvement"],
    ["Statistics Final Exam", 0.5, "2024-07-05", 6.89, "Very good understanding"]
    ]

    testevents = [
    ["Berlin", "2026-02-01", "10:00", "12:00", "Technologie Konferenz", 666],
    ["Hamburg", "2026-02-03", "18:00", "22:00", "Live Konzert in der Innenstadt", 666],
    ["München", "2026-02-05", "09:00", "17:00", "Ganztägiger Workshop", 666],
    ["Köln", "2026-02-10", "20:00", "23:00", "Comedy Abend", 666],
    ["Frankfurt", "2026-02-15", "14:00", "18:00", "Business Networking Event", 666]
    ]


    for a,grade in enumerate(testGradesfuerEliahFranzösisch):
        eventID = str(uuid.uuid4())
        db.addNewExamen(FranzösischM4GcourseID, eventID,grade[0],grade[1])
        db.addNewGrade(testData[0][0], eventID,grade[3],grade[4])
        db.addNewEvent(eventID,testevents[a][0],testevents[a][1],testevents[a][2],testevents[a][3],testevents[a][4],testevents[a][5])
    
    for a,grade in enumerate(testGradesfuerEliahEnglisch):
        eventID = str(uuid.uuid4())
        db.addNewExamen(FranzösischM4GcourseID, eventID,grade[0],grade[1])
        db.addNewGrade(testData[0][0], eventID,grade[3],grade[4])
        db.addNewEvent(eventID,testevents[a][0],testevents[a][1],testevents[a][2],testevents[a][3],testevents[a][4],testevents[a][5])
    


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
