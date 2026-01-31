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
                "changedate": grade[2],
                "grade": grade[3],
                "message": grade[4],
                "fileID": grade[5]
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

