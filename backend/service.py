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
    db.addNewEvent(eventID,location,date,starttime,endtime,describtion, 666)
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
            }
        gradeslist.append(gradeDict)
    
    return gradeslist



def getAllExamAndEventDataWithEventID(db,eventID):
    examData = db.getAllExamAndEventDataWithEventID(eventID)

    examDict = {
            "testName": examData[0],
            "weight": examData[1],
            "location": examData[2],
            "starttime": examData[3],
            "endtime": examData[4],
            "describtion": examData[5],
            }

    return examDict
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

