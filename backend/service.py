import database
import uuid
import os


uploadFolder = "user_documents"



def getAllGradesforStudents(db, userID):
    
    courses = db.getALLCourseWithUserID(userID)

    if courses == []:
        return []


    output = []


    for course in courses:
        gradesFromCourse = db.getAllGradesWithCourseIDAndUserID(course[0],userID)
        grades = []
        for grade in gradesFromCourse:
            gradeDict ={
                "testName": grade[0],
                "weight": grade[1],
                "grade": grade[2],
                "message": grade[3],
                "fileID": grade[4],
                "date": grade[5]
                }
            grades.append(gradeDict)
        courseDict = {
            "name" : course[1],
            "grades" : grades
        }
        output.append(courseDict)

    return output
            
def addNewExamenForCourseWithEventAndDefaultGrades(db,courseID,examenName,weight,location,date,starttime,endtime,describtion):
    eventID = str(uuid.uuid4())
    db.addNewExamen(courseID,eventID,examenName,weight)
    db.addNewGradesForExamForEveryoneInCourse(courseID,eventID)
    db.addNewEvent(eventID,location,date,starttime,endtime,describtion, 666,courseID)
    return True

#Teacher Only
def getAllCoursesWithAllExamsFromUserID(db,userID): 
     
    courses = db.getALLCourseWithUserID(userID)

    output = []
    for course in courses:
        exams = db.getAllExamsFromCourseID(course[0])
        examsList = []
        for examen in exams:
            examenDict = {
            "testName": examen[0],
            "weight": examen[1],
            "date": examen[2],
            "eventID": examen[3]
            }
            examsList.append(examenDict)

        courseDict = {
            "courseID": course[0],
            "subject": course[1],
            "courseName": course[2],
            "exams": examsList
        }
        output.append(courseDict)

    return output

def getAllGradesFromAllStudentsOfTest(db, eventID):

    grades = db.getAllGradesPlusNamesWithEventID(eventID)
    gradeslist = []
    for grade in grades:
        gradeDict ={
            "firstName": grade[0],
            "lastName": grade[1],
            "grade": grade[2],
            "message": grade[3],
            "fileID": grade[4],
            "userID": grade[5],
            }
        gradeslist.append(gradeDict)
    
    return gradeslist


def updateAllGradesFromAllStudentsOfTest(db,grades,eventID):
    for gradeDict in grades:
        if "userID" not in gradeDict:
            continue
        if "message" not in gradeDict:
            continue 
        if "fileID" not in gradeDict:
            continue
        if "userID" not in gradeDict:
            continue
        grade = gradeDict["grade"]
        message = gradeDict["message"]
        fileID = gradeDict["fileID"]
        userID = gradeDict["userID"]
        db.updateGradeWithEventIDAndUserID(grade,message,fileID,eventID,userID)
    return



def getAllExamAndEventDataWithEventID(db,eventID):
    examData = db.getAllExamAndEventDataWithEventID(eventID)

    examDict = {
            "testName": examData[0],
            "weight": examData[1],
            "location": examData[2],
            "date":examData[3],
            "starttime": examData[4],
            "endtime": examData[5],
            "description": examData[6],
            "courseID":examData[7],
            "eventID": examData[8],
            }

    return examDict

def updateAllExamAndEventDataWithEventIDAndCourseID(db,exam):
    if "testName" not in exam:
        return False
    if "weight" not in exam:
        return False
    if "location" not in exam:
        return False
    if "date" not in exam:
        return False
    if "starttime" not in exam:
        return False
    if "endtime" not in exam:
        return False
    if "description" not in exam:
        return False
    if "eventID" not in exam:
        return False
    testName = exam["testName"]
    weight = exam["weight"]
    location = exam["location"]
    date = exam["date"]
    starttime = exam["starttime"]
    endtime = exam["endtime"]
    description = exam["description"]
    eventID = exam["eventID"]
    courseID = exam["courseID"]

    db.updateAllExamAndEventDataWithEventID(testName,weight,location,date,starttime,endtime,description,courseID,eventID)

    return True

def postFcmToken(db,userID,fcmToken,hardwareID):
    if db.isFcmTokenExistWithUserIDandHardwareID(userID,hardwareID):
        db.updateFcmTokenWithUserIDAndHardwareToken(userID,fcmToken,hardwareID)
        return hardwareID
    hardwareID = str(uuid.uuid4())
    db.addNewFcmToken(userID,fcmToken,hardwareToken)
    return hardwareID


def getAllUserData(db,userID):
    userData = db.getAllUserDataWithUserID(userID)
    for a in range(7,12,1):
        if userData[a] == None:
            userData[a] = 0


    outputDict = {
        "userName": userData[0],
        "className": userData[1],
        "major": userData[2],
        "email": userData[3],
        "role": userData[4],
        "firstName": userData[5],
        "lastName": userData[6],
        "notifAbsenceOfTeacherToday": userData[7],
        "notifAbsenceOfTeacherTomorrow": userData[8],
        "notifExamTomorrow": userData[9],
        "notifEventTomorrow": userData[10],
        "notifAbsenceDueTomorrow": userData[11]
    }
    return outputDict

def postAllUserInformation(db,data,userID):
    userName = data["userName"]
    email = data["email"]
    notifAbsenceOfTeacherToday = data["notifAbsenceOfTeacherToday"]
    notifAbsenceOfTeacherTomorrow = data["notifAbsenceOfTeacherTomorrow"]
    notifExamTomorrow = data["notifExamTomorrow"]
    notifEventTomorrow = data["notifEventTomorrow"]
    notifAbsenceDueTomorrow = data["notifAbsenceDueTomorrow"]

    if not isinstance(userName,str):
        return False
    if not isinstance(email,str):
        return False

    if not isinstance(notifAbsenceOfTeacherToday,int):
        return False
    
    if not isinstance(notifAbsenceOfTeacherTomorrow,int):
        return False
    if not isinstance(notifExamTomorrow,int):
        return False
    if not isinstance(notifEventTomorrow,int):
        return False
    if not isinstance(notifAbsenceDueTomorrow,int):
        return False
    if notifAbsenceOfTeacherToday != 0 and notifAbsenceOfTeacherToday != 1 :
        return False
    if notifAbsenceOfTeacherTomorrow != 0 and notifAbsenceOfTeacherTomorrow != 1 :
        return False
    if notifExamTomorrow != 0 and notifExamTomorrow != 1 :
        return False
    if notifEventTomorrow != 0 and notifEventTomorrow != 1 :
        return False
    if notifAbsenceDueTomorrow != 0 and notifAbsenceDueTomorrow != 1 :
        return False
    db.updateUserDataFromUserWithUserID(userID,userName,email,notifAbsenceOfTeacherToday,notifAbsenceOfTeacherTomorrow,notifExamTomorrow,notifEventTomorrow,notifAbsenceDueTomorrow)
    return True

################ NOCH NICHT FERTIG ###############################
def saveNewFile(file):
    oldFileName = file.filename
    fileId, newFileName = database.addNewFile(oldFileName)
    file.save(os.path.join(uploadFolder, newFileName))
    return fileId

def lookUpFile(fileId):
    nameBefor,nameAfter = database.getNamesOfFile(FileId)

    path = os.path.join(uploadFolder, nameAfter)
    if not os.path.exists(file_path):
        return False
    
    return 

