import database
import uuid
import os
from datetime import datetime,timedelta




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
            
def addNewExamenForCourseWithEventAndDefaultGrades(db,courseID,examenName,weight,location,starttime,endtime,describtion):
    eventID = str(uuid.uuid4())
    db.addNewExamen(courseID,eventID,examenName,weight)
    db.addNewGradesForExamForEveryoneInCourse(courseID,eventID)
    db.addNewEvent(eventID,location,starttime,endtime,describtion, 666,courseID)
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


        #Unerblaubte noten
        if grade > 6.5:
            continue
        if grade < 1 and grade != 0:
            continue


        #aktualisierung DB
        db.updateGradeWithEventIDAndUserID(grade,message,fileID,eventID,userID)

        #grade,message,fileID,courseID
        dbGrade = db.getGradeWithEventIDAndUserID(eventID,userID)
        if dbGrade == None:
            continue

        subject = db.getSubjectWithCourseID(dbGrade[3])

        #send messages
        if grade != 0 and dbGrade[0] == 0:
            notification.sentNotificationToUserID(db,userID,"Neue Note",f"Sie haben eine neue Note im Fach {subject}",5)
            continue
        
        if grade != 0 and dbGrade[0] != 0 and grade != dbGrade[0]:
            notification.sentNotificationToUserID(db,userID,"Notenänderung",f"Eine Note im Fach {subject} hat sich von {dbGrade[0]} zu {grade} verändert",5)
            continue
        
        if message != dbGrade[1] or fileID != dbGrade[2]:
            notification.sentNotificationToUserID(db,userID,"Noten Anhang Veränderung",f"Bei einer Note im Fach {subject} haben sich die Anhänge verändert",5)

    return



def getAllExamAndEventDataWithEventID(db,eventID):
    examData = db.getAllExamAndEventDataWithEventID(eventID)

    examDict = {
            "testName": examData[0],
            "weight": examData[1],
            "location": examData[2],
            "starttime": examData[3],
            "endtime": examData[4],
            "description": examData[5],
            "courseID":examData[6],
            "eventID": examData[7],
            }

    return examDict

def updateAllExamAndEventDataWithEventIDAndCourseID(db,exam):
    if "testName" not in exam:
        return False
    if "weight" not in exam:
        return False
    if "location" not in exam:
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
    starttime = exam["starttime"]
    endtime = exam["endtime"]
    description = exam["description"]
    eventID = exam["eventID"]
    courseID = exam["courseID"]

    db.updateAllExamAndEventDataWithEventID(testName,weight,location,starttime,endtime,description,courseID,eventID)

    return True

def postFcmToken(db,userID,fcmToken):
    if db.isFcmTokenExistWithUserID(userID,fcmToken):
        return


    print("EINE NEUE EINTRAG MUSSTE ERSTELLT WERDEN")
    db.addNewFcmToken(userID,fcmToken)
    return


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

    
    if not (notifAbsenceOfTeacherToday == 0 or notifAbsenceOfTeacherToday == 1) :
        return False
    if not (notifAbsenceOfTeacherTomorrow != 0 or notifAbsenceOfTeacherTomorrow != 1) :
        return False
    if not (notifExamTomorrow == 0 or notifExamTomorrow == 1) :
        return False
    if not (notifEventTomorrow == 0 or notifEventTomorrow == 1) :
        return False
    if not (notifAbsenceDueTomorrow == 0 or notifAbsenceDueTomorrow == 1) :
        return False
    db.updateUserDataFromUserWithUserID(userID,userName,email,notifAbsenceOfTeacherToday,notifAbsenceOfTeacherTomorrow,notifExamTomorrow,notifEventTomorrow,notifAbsenceDueTomorrow)
    return True


def getScheduleOfOneDay(db,userID,date,starttime=None,endtime=None):
    schedule = []

    if not db.isHolidateAtdate(date.strftime("%Y-%m-%d %H:%M")):
        schedule = db.getScheduleOfWeekdayWithTimeIntervalWithUserID(userID,date.weekday(),"00:01","23:59", date.strftime("%Y-%m-%d"))


    
    events = db.getEventsAtDayWithUserID(userID,date.strftime("%Y-%m-%d"))
    print("events")
    print(events)
    
    #sind Tuble
    events = [list(t) for t in events]
    #schedule = [list(t) for t in schedule] wird schon in db.getScheduleOfWeekdayWithTimeIntervalWithUserID

    print(schedule)
    print("events")
    print(events)

    for event in events:
        event[0] = datetime.strptime(event[0], "%Y-%m-%d %H:%M")
        event[1] = datetime.strptime(event[1], "%Y-%m-%d %H:%M")

    for lection in schedule:
        lection[0] = datetime.strptime(lection[0], "%Y-%m-%d %H:%M")
        lection[1] = datetime.strptime(lection[1], "%Y-%m-%d %H:%M")
        lection.append("")



    if schedule == []:
        outputDict = []
        for a,lection in enumerate(events):
            lectionDict = {
                "starttime" : lection[0].strftime("%Y-%m-%d %H:%M"),
                "endtime" : lection[1].strftime("%Y-%m-%d %H:%M"),
                "location" : lection[2],
                "courseID" : lection[3],
                "subject" : lection[4],
                "courseName" : lection[5],
                "type" : lection[6],
                "eventID": lection[7]
            }
            outputDict.append(lectionDict)

        return outputDict
            
    
    #event : ev.starttime,ev.endtime,ev.location,ev.courseid,co.subject,co.courseName,ev.type,eventID
    #schedule: sc.starttime,sc.endtime,sc.location,sc.courseid,co.subject,co.courseName, type, "" (als eventID)
    else: 
        #merge Event with Schedule
        output = []



        #Lektionen veränderungen

        for event in events:
            if event[6] == 301:
                for lection in schedule:
                    if lection[3] == event[3]:
                        if lection[0] == event[0] and lection[1] == event[1]:
                            lection = event



        #Lektionen absagen
        for event in events:
            if event[6] == 400:
                for lection in schedule:
                    if lection[3] == event[3]:
                        if lection[0] == event[0] and lection[1] == event[1]:
                            lection = event


        #Overwrite schedule with examens
        for event in events:
            if event[6] == 666:
                for lection in schedule:
                    if lection[3] == event[3]:
                        if lection[0] > event[0] and lection[0] < event[1]:
                            lection[0] = event[1]

                        if lection[1] > event[0] and lection[1] < event[1]:
                            lection[1] = event[0]
                print("EVENT NDNDNDNDNN")
                output.append(event)


        #Urlaubsgesuche überschreiben
        for event in events:
            if event[6] == 150:
                for lection in schedule:
                    if lection[0] > event[0] and lection[0] < event[1]:
                        lection[0] = event[1]

                    if lection[1] > event[0] and lection[1] < event[1]:
                        lection[1] = event[0]
                
                output.append(event)
                print("djdjdjdj")
        


        print("Zuvor")
        print(output)
        output.extend(schedule)

        print("OUTput")
        print(output)


        if starttime != None:
            #starttime = datetime.strptime(starttime, "%Y-%m-%d %H:%M")

            #Hier werden die Termine abgeschnitten, je nach starttime
            """
            for lection in output:
                if lection[0] < starttime:
                    lection[0] = starttime
            """
        
        if endtime != None:
            #endtime = datetime.strptime(starttime, "%Y-%m-%d %H:%M")

            #Hier werden die Termine abgeschnitten, je nach starttime
            """
            for lection in output:
                if lection[1] > endtime:
                    lection[1] = endtime

            """
        

        for a in range(len(output)-1,-1,-1):
            if output[a][0] >= output[a][1]:
                output.pop(a)
        

        
    #schedule: sc.starttime,sc.endtime,sc.location,sc.courseid,co.subject,co.courseName
        outputDict = []
        for a,lection in enumerate(output):
            lectionDict = {
                "starttime" : lection[0].strftime("%Y-%m-%d %H:%M"),
                "endtime" : lection[1].strftime("%Y-%m-%d %H:%M"),
                "location" : lection[2],
                "courseID" : lection[3],
                "subject" : lection[4],
                "courseName" : lection[5],
                "type" : lection[6],
                "eventID": lection[7]
            }
            outputDict.append(lectionDict)

        return outputDict
            






def getSchedule(db,userID,starttime,endtime):
    starttime = datetime.strptime(starttime, "%Y-%m-%d %H:%M")
    endtime = datetime.strptime(endtime, "%Y-%m-%d %H:%M")

    if starttime > endtime:
        return False

    ## Get normal Schedule
    output = []
    

    if endtime.date() == starttime.date():
        scheduleDict = getScheduleOfOneDay(db,userID,endtime.date(),starttime,endtime)
        outputDict = {
            "schedule" : scheduleDict,
            "date" : endtime.strftime("%Y-%m-%d")
        }

        output.append(outputDict)
        return output

    else:

        scheduleDict = getScheduleOfOneDay(db,userID,starttime.date(),starttime,None)
        outputDict = {
            "schedule" : scheduleDict,
            "date" : starttime.strftime("%Y-%m-%d")
        }

        output.append(outputDict)
        tempTime = starttime
        
        tempTime = tempTime + timedelta(days=1)
        while tempTime.date() != endtime.date():
            scheduleDict = getScheduleOfOneDay(db,userID,tempTime.date(),starttime,None)
            outputDict = {
            "schedule" : scheduleDict,
            "date" : tempTime.strftime("%Y-%m-%d")
            }
            output.append(outputDict)
            
            tempTime = tempTime + timedelta(days=1)
        
        scheduleDict = getScheduleOfOneDay(db,userID,tempTime.date(),None,endtime)
        outputDict = {
        "schedule" : scheduleDict,
        "date" : tempTime.strftime("%Y-%m-%d")
        }
        output.append(outputDict)


    return output
        







def getAbsenceUser(db,userID):
    #finish Absence
    arrayFinishAbsence = db.getAbsenceWithUserIDAndType(userID,2)

    finishAbsenceDictArray = []
    for absence in arrayFinishAbsence:
        eventDictArray = []
        arrayAbsenceEvent = db.getAllAbsenceEventWithAbsenceID(absence[0],userID)
        for event in arrayAbsenceEvent:
            eventDict = {
                "eventID": event[0],
                "location": event[1],
                "starttime": event[2],
                "endtime": event[3],
                "subject": event[4],
                "courseName": event[5]
            }
            eventDictArray.append(eventDict)
        
        absenceDict = {
            "events": eventDictArray,
            "absenceID": absence[0],
            "endday": absence[1],
            "fileID": absence[2],
            "description": absence[3],
            "excused": 2
        }
        finishAbsenceDictArray.append(absenceDict)

    #Excused Absence
    arrayExcusedAbsence = db.getAbsenceWithUserIDAndType(userID,1)

    excusedAbsenceDictArray = []
    for absence in arrayExcusedAbsence:
        eventDictArray = []
        arrayAbsenceEvent = db.getAllAbsenceEventWithAbsenceID(absence[0],userID)
        for event in arrayAbsenceEvent:
            eventDict = {
                "eventID": event[0],
                "location": event[1],
                "starttime": event[2],
                "endtime": event[3],
                "subject": event[4],
                "courseName": event[5]
            }
            eventDictArray.append(eventDict)
        
        absenceDict = {
            "events": eventDictArray,
            "absenceID": absence[0],
            "endday": absence[1],
            "fileID": absence[2],
            "description": absence[3],
            "excused": 1
        }
        excusedAbsenceDictArray.append(absenceDict)



    #NOT Excused Absence
    arrayNotExcusedAbsence = db.getAbsenceWithUserIDAndType(userID,0)

    notExcusedAbsenceDictArray = []
    for absence in arrayNotExcusedAbsence:
        eventDictArray = []
        arrayAbsenceEvent = db.getAllAbsenceEventWithAbsenceID(absence[0],userID)
        for event in arrayAbsenceEvent:
            eventDict = {
                "eventID": event[0],
                "location": event[1],
                "starttime": event[2],
                "endtime": event[3],
                "subject": event[4],
                "courseName": event[5]
            }
            eventDictArray.append(eventDict)
        
        absenceDict = {
            "events": eventDictArray,
            "absenceID": absence[0],
            "endday": absence[1],
            "fileID": absence[2],
            "description": absence[3],
            "excused": 0
        }
        notExcusedAbsenceDictArray.append(absenceDict)
    

    userinfo = db.getAllUserDataWithUserID(userID)
    outputDict = {
        "userID": userID,
        "firstName": userinfo[5],
        "lastName": userinfo[6],
        "finished": finishAbsenceDictArray,
        "excused": excusedAbsenceDictArray,
        "notExcused": notExcusedAbsenceDictArray
    }
    return outputDict


def getAbsenceTeacher(db,userID):
    className = db.getClassNameWithUserID(userID)


    output = []

    if className == "" or className == None:
        return output
    

    students = db.getUserWithclassName(className)

    for student in students:

        if student[1] != 1: #Teacher ausschliessen
            continue
        
        output.append(getAbsenceUser(db,student[0]))

    return output




def isClassTeacher(db,teacherUserID,studentUserID):
    className = db.getClassNameWithUserID(teacherUserID)



    print("Classname")
    print(className)


    if className == "" or className == None:
        return False
    

    students = db.getUserWithclassName(className)

    print(students)
    print("studentUserID")
    print(studentUserID)

    for student in students:

        if student[0] == studentUserID:
            return True

    return False



def mergeAbsence(db,userID,role,absenceIDlist):

    # userid,endday,excused,description,fileid


    absences = []

    for absenceID in absenceIDlist:
        absence = db.getAbsenceWithAbsenceID(absenceID)
        if absence == []:
            return False
        absences.append(absence)
    

    print(absences)
    for absence in absences:
        if absence[0] != absences[0][0]: # wenn nicht alle userID gleich sind return Fehler
            return False
        if absence[2] != absences[0][2]: # wenn nicht alle Excused type gleich sind return Fehler
            return False



    if absences[0][2] == 2 and role == 2: #Only teacher are able to change that
        return False


    if role == 2 and not isClassTeacher(db,userID,absences[0][0]): # If Teacher, only Classteacher has permisson to change
        return False

    if role < 2 and userID != absences[0][0]: #When User, only User is able to change
        return False

    
    # get one Fileid 
    fileID = ""

    for absence in absences:
        if absence[4] != "" and absence[4] != None:
            fileID = absence[4]
            break

    # get one description
    description = ""

    for absence in absences:
        if absence[3] != "" and absence[3] != None:
            description = absence[3]
            break


    print(absences)
    endday = datetime.strptime(absences[0][1], "%Y-%m-%d")


    for absence in absences:
        if datetime.strptime(absence[1], "%Y-%m-%d") < endday:
            endday = datetime.strptime(absence[1], "%Y-%m-%d")

    

    #Update eines Eintrangs
    db.updateAbsenceWithAbsenceID(absenceIDlist[0],endday.date(),absences[0][2],description,fileID)

    #Löschung der restlichen Einträge Absencen und überschreibung der AbsenceID der AbsenceEvents
    for a in range(1,len(absenceIDlist),1):
        db.updateAbsenceIDOfEventWithAbsenceID(absenceIDlist[a],absenceIDlist[0])
        db.deleteAbsenceWithAbsenceID(absenceIDlist[a])

    return True








    # Delete one Absence

    #rewrite Event with new AbsenceID

    return

def changeAbsence(db,userID,role,absence):
    #userid,endday,excused,description,fileid
    absenceID = absence["absenceID"]
    excused = absence["excused"]
    description = absence["description"]
    fileID = absence["fileID"]

    if excused not in [0,1,2]:
        return False


    #userid,endday,excused,description,fileid
    databaseAbsence = db.getAbsenceWithAbsenceID(absenceID)

    if databaseAbsence == []:
        return False



    print(databaseAbsence)
    print("Ich bin im 1")


    if (databaseAbsence[2] == 2 or excused == 2) and role != 2: #Only teacher are able to change that
        return False
    
    print("Ich bin im 2")

    if role == 2 and not isClassTeacher(db,userID,databaseAbsence[0]): # If Teacher, only Classteacher has permisson to change
        return False
    print("Ich bin im 3")

    print(databaseAbsence)
    print(userID)
    if role < 2 and userID != databaseAbsence[0]: #When User, only User is able to change
        return False
    print("Ich bin im 4")


    #User kann nur etwas verändern, wenn endday noch nicht fertig ist.

    if datetime.today() > datetime.strptime(databaseAbsence[1], "%Y-%m-%d") and role < 2:
        return False

    print("Ich bin im 5")

    
    db.updateAbsenceWithAbsenceID(absenceID,databaseAbsence[1],excused,description,fileID)

    return True



#only for Teacher
def deleteAbsenceEvent(db,teacherUserID,studentUserID,eventID,absenceID):

    if not isClassTeacher(db,teacherUserID,studentUserID):
        return False

    db.deleteEventWithabsenceIDAndEventIDAnd(absenceID,eventID)
    return True




def isEventExists(db,courseID,eventID,starttime,endtime):
    if eventID == "" or eventID == "nothing":
        time1 = datetime.strptime(starttime, "%Y-%m-%d %H:%M")
        time2 = datetime.strptime(endtime, "%Y-%m-%d %H:%M")
        if time1.date() != time2.date():
            
            return False
        return db.isScheduleExistsWithCourseIDStarttimeEndtime(courseID,starttime[-5:],endtime[-5:],time1.weekday())
            
    else:
        return db.isEventExistsWithEventIDCourseIDStarttimeEndtime(eventID,courseID,starttime,endtime)




def getAnwesenheitsliste(db,userID,courseID,eventID,starttime,endtime):
    if not isEventExists(db,courseID,eventID,starttime,endtime):
        return False
    
    if not db.isUserIDinCourse(userID,courseID):
        
        return False

    #alle Schüler User bekommen
    #userID, firstname, lastname,has Event
    students = db.getAllStudentsFromCourse(courseID)

    print(students)
    print(userID)
    print(courseID)
    print(eventID)
    print(starttime)
    print(endtime)


    output = []
    for student in students:
        if db.isAbsenceEventExistWithUserIDCourseIDAndTime(student[0],courseID,starttime,endtime):
            print("HELELEldldldldld")
            absence = 1
        else:
            absence = student[3]
        
        studentDict = {
            "userID":student[0],
            "firstName": student[1],
            "lastName": student[2],
            "absence": absence
        }
        output.append(studentDict)
    
    return output
        
        
def postAnwesenheitsliste(db,userID,courseID,eventID,starttime,endtime,anwesenheitsliste):

    databaseAnwesenheitsliste = getAnwesenheitsliste(db,userID,courseID,eventID,starttime,endtime)

    if databaseAnwesenheitsliste == False:
        return False

    for databaseStudent in databaseAnwesenheitsliste:
        for student in anwesenheitsliste:
            if databaseStudent["userID"] == student["userID"] and databaseStudent["userID"] != None:
                if databaseStudent["absence"] != student["absence"]:
                    if databaseStudent["absence"] == 0 and student["absence"] == 1:
                        absenceID = str(uuid.uuid4())

                        endday = datetime.strptime(endtime, "%Y-%m-%d %H:%M") + timedelta(days=7)
                        db.addAbsence(databaseStudent["userID"],endday.date(),0,absenceID)


                        eventID = str(uuid.uuid4())  

                        db.addAbsenceEventInEvent(eventID,starttime,endtime,courseID,absenceID,databaseStudent["userID"])       
                        

                    if databaseStudent["absence"] == 1 and student["absence"] == 0:
                        #delete AbsenceEvent
                        print("lksadjfosdihfkjd")
                        print(starttime)
                        print(endtime)
                        print(courseID)
                        db.deleteAbsenceEventInEvent(starttime,endtime,courseID,databaseStudent["userID"])
                
                break

    return True       
                    




def isUserHavePermissionToFileID(db,userID,fileID):


    role = db.getRolefromUserWithUserID(userID)


    # is fileID in absence

    # if user, Role == 1: muss userID bei Absence stimmen
    # Oder User ist lehrer, dann muss sie Klassenlehrerin von userID sein.
    databaseUserID = db.getUserIDFromAbsenceWithFileID(fileID)

    if databaseUserID != None:
        if role == 1 and databaseUserID == userID:
            return True
        if role == 2 and isClassTeacher(db,userID,databaseUserID):
            return True

    
    
    
    # is fileID in Event

    # user muss in course sein

    courseID = db.getCourseIDFromEventWithFileID(fileID)
    if db.isUserIDinCourse(userID,courseID):
        return True









    #if fileID in Grades


    # Role = 1, user muss die Grade gehören
    # Falls Lehrer, muss er im Course sein

    if role == 1:
        if userID == db.getUserIDFromGradeWithFileID(fileID):
            return True
    
    if role == 2:
        courseID = db.getCourseIDFromGradeWithFileID(fileID)
        if courseID != None:
            if db.isUserIDinCourse(userID,courseID):
                return True




    return False






