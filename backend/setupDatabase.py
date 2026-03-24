import database
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import uuid
import service



db = database.Database()


def insertTestDataTableUserAndCourse(db):
    testData = [
        [0,"Eliah","Eliah","M4G","A","test@test.ch",1,"Eliah","Hueber","2005-03-14"],
        [0,"Emil","Emil","M4G","B","test@test.ch",1,"Emil","Peterson","2009-07-22"],
        [0,"Nahia","Nahia","M4G","B","test@test.ch",1,"Nahia","Weyeneth","2008-11-02"],
        [0,"Paul","Paul","M4G","W","test@test.ch",1,"Paul","Konzili","2009-01-18"],
        [0,"Esben","Esben","M4G","A","test@test.ch",1,"Esben","Duss","2008-09-30"],
        [0,"Moritz","Moritz","M4G","A","test@test.ch",1,"Moritz","Brotbeck","2009-05-12"],
        [0,"Manuel","Manuel","M4G","W","test@test.ch",1,"Manuel","Kron","2008-12-03"],
        [0,"Aurel","Aurel","M4G","W","test@test.ch",1,"Aurel","Richterich","2009-04-27"],
        [0,"Loic","Loic","M4G","W","test@test.ch",1,"Loic","Eicher","2008-08-16"],
        [0,"Walter","Walter","M4G","A","test@test.ch",1,"Walter","Kutz","2009-10-09"],
        [0,"Theo","Theo","M4G","A","test@test.ch",1,"Theo","Böhm","2004-06-25"],
        [0,"Marlon","Marlon","M4G","A","test@test.ch",1,"Marlon","Auchli","2004-06-25"],
        [0,"Anklin","Anklin","M4G","","test@test.ch",2,"Melanie","Anklin",None],
        [0,"Zulauf","Zulauf","","","test@test.ch",2,"Lester","Zulauf",None],
        [0,"admin","admin","","","test@test.ch",5,"admin","admin",None]
        ]

    testDataParents = [
        [0,"ParentEliah","ParentEliah","","","test@test.ch",0,"",""],
        [0,"ParentEmil","ParentEmil","","","test@test.ch",0,"",""],
        [0,"ParentNahia","ParentNahia","","","test@test.ch",0,"",""],
        [0,"ParentPaul","ParentPaul","","","test@test.ch",0,"",""],
        [0,"ParentEsben","ParentEsben","","","test@test.ch",0,"",""],
        [0,"ParentMoritz","ParentMoritz","","","test@test.ch",0,"",""],
        [0,"ParentManuel","ParentManuel","","","test@test.ch",0,"",""],
        [0,"ParentAurel","ParentAurel","","","test@test.ch",0,"",""],
        [0,"ParentLoic","ParentLoic","","","test@test.ch",0,"",""],
        [0,"ParentWalter","ParentWalter","","","test@test.ch",0,"",""],
        [0,"ParentTheo","ParentTheo","","","test@test.ch",0,"",""],
        [0,"ParentMarlon","ParentMarlon","","","test@test.ch",0,"",""],
        ]

    ph = PasswordHasher()

    FranzösischM4GcourseID = str(uuid.uuid4())
    EnglischM4GcourseID = str(uuid.uuid4())
    Klasse4MgCourseID = str(uuid.uuid4())


    for row in testData:
        row[2] = ph.hash(row[2]) 
        row[0] = db.addNewUser(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9])

        if(row[6] == 1 or row[1] == "Anklin"):
            #print("hello")
            db.addNewCourse(FranzösischM4GcourseID,row[0],"F","F-M4G-26",1)
            db.addNewCourse(Klasse4MgCourseID,row[0],"K","M4G",0)
        if(row[6] == 1 or row[1] == "Zulauf"):
            db.addNewCourse(EnglischM4GcourseID,row[0],"E","E-M4G-26",1)



    
    for row in testData:
        db.addNewCourse(row[0],row[0],"self","self",0)
    
    # [[testname, weight, changedatum, grade, message]]

    #add ParentUsers
    for a,row in enumerate(testDataParents):
        row[2] = ph.hash(row[2]) 
        row[0] = db.addNewUser(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],None,testData[a][0])

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
    ["Berlin", "2026-02-01", "2026-02-01 10:00", "2026-02-01 12:00", "Technologie Konferenz", 666],
    ["Hamburg", "2026-02-03", "2026-02-02 18:00", "2026-02-01 22:00", "Live Konzert in der Innenstadt", 666],
    ["München", "2026-02-05", "2026-02-03 09:00", "2026-02-01 17:00", "Ganztägiger Workshop", 666],
    ["Köln", "2026-02-10", "2026-02-04 20:00", "2026-02-01 23:00", "Comedy Abend", 666],
    ["Frankfurt", "2026-02-15", "2026-02-05 14:00", "2026-02-01 18:00", "Business Networking Event", 666]
    ]

    
    

    for a,grade in enumerate(testGradesfuerEliahFranzösisch):
        service.addNewExamenForCourseWithEventAndDefaultGrades(db,FranzösischM4GcourseID,grade[0],grade[1],"P001","2026-02-05 11:30","2026-02-05 12:30","Dies ist die Describtion oder Description")
           
    for a,grade in enumerate(testGradesfuerEliahEnglisch):
        eventID = str(uuid.uuid4())
        db.addNewExamen(EnglischM4GcourseID, eventID,grade[0],grade[1])
        db.addNewGrade(testData[0][0], eventID,grade[3],grade[4])
        db.addNewEvent(eventID,testevents[a][0],testevents[a][2],testevents[a][3],testevents[a][4],testevents[a][5],EnglischM4GcourseID)
    



    #creat Schedule
    scheduleData = [
    # Montag
    ["0", 0,    "08:00", "08:45", "A101"],
    ["0", 0,    "08:55", "09:40", "B203"],
    ["0", 0,    "10:00", "10:45", "C315"],
    ["0", 0,    "10:55", "11:40", "D427"],

    # Dienstag
    ["0", 1,   "08:00", "08:45", "E102"],
    ["0", 1,   "08:55", "09:40", "F214"],
    ["0", 1,   "11:50", "12:35", "A326"],
    ["0", 2,   "12:45", "13:30", "B438"],

    # Mittwoch
    ["0", 2, "10:00", "10:45", "C109"],
    ["0", 2, "10:55", "11:40", "D221"],
    ["0", 2, "13:40", "14:25", "E333"],
    ["0", 2, "14:35", "15:20", "F445"],

    # Donnerstag
    ["0", 3,  "08:00", "08:45", "A150"],
    ["0", 3,  "08:55", "09:40", "B262"],
    ["0", 3,  "15:30", "16:15", "C374"],
    ["0", 3,  "16:25", "17:10", "D486"],

    # Freitag
    ["0", 4,    "11:50", "12:35", "E198"],
    ["0", 4,    "12:45", "13:30", "F210"],
    ["0", 4,    "13:40", "14:25", "A322"],
    ["0", 4,    "14:35", "15:20", "B434"],
]


    for a in range(len(scheduleData)):
        if a % 2 == 0:
            scheduleData[a][0] = FranzösischM4GcourseID
        else:
            scheduleData[a][0] = EnglischM4GcourseID
        db.addNewSchedule(scheduleData[a][0],scheduleData[a][1],scheduleData[a][2],scheduleData[a][3],scheduleData[a][4])


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
db.creatTableFcmToken()

insertTestDataTableUserAndCourse(db)
