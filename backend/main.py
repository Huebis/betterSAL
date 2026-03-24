import json
from flask import Flask, request, Response, render_template, g, jsonify,send_from_directory
from database import Database
import service
from flask_cors import CORS
import notification
from datetime import datetime, date
import os
import uuid



#source venv/bin/activate 
def verificationDatatype(parameter, datatype):



    def isValidUuid(uuid4):
    
        if not isinstance(uuid4, str):
            return False

        try:
            u = uuid.UUID(uuid4)
        except ValueError:
            return False
        
        return u.version == 4 and str(u) == uuid4.lower()


    def isDateTimeDay(date):
        if not isinstance(date, str):
            return False

        try:
            dt = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return False

        return dt.strftime("%Y-%m-%d") == date

    def isDateTimeMinute(date):
        if not isinstance(date, str):
            return False

        try:
            dt = datetime.strptime(date, "%Y-%m-%d %H:%M")
        except ValueError:
            return False

        return dt.strftime("%Y-%m-%d %H:%M") == date

    def isString(string):
        return isinstance(string,str)


    def isInt(integer):
        return isinstance(integer, int)
    def isList(liste):
        return isinstance(liste,list)
    def isDict(dicte):
        return isinstance(dicte, dict)
    
    


    match datatype:
        case "dateMinute":
            return isDateTimeMinute(parameter)
        case "dateDay":
            return isDateTimeDay(parameter)
        case "string":
            return isString(parameter)
        case "int":
            return isInt(parameter)
        case "uuid4":
            return isValidUuid(parameter)
        case "list":
            return isList(parameter)
        case "dict":
            return isDict(parameter)
        case _:
            raise Exception("Mistake in Datatype verifikation")
            return False




def get_db():
    db = getattr(g, '_database', None)
    print("1")
    if db is None:
        print("2")
        db = g._database = Database()
    return db
 


def isEveryDataNameinObject(testedObject,dataValues):
    #dataValue list [0] stringname / [1] typ in string
    for value in dataValues:
        if value[0] not in testedObject:
            return False
        
        parameter = testedObject[value[0]]
        
        print("hello")
        print(value)
        if not verificationDatatype(parameter,value[1]):
            print("FEHLER BEI DER EINGABE DER PARAMETER")
            print(parameter)
            print(value)
            return False






    return True



def isAdult(birthDate):
    print(birthDate)
    today = date.today()

    birthDate = datetime.strptime(birthDate, "%Y-%m-%d")
    return (today.year - birthDate.year - 
           ((today.month, today.day) < (birthDate.month, birthDate.day))) >= 18
#return True,UserID, None, None when everything is fine
#return False,None, error, Fehlernummer when something is wrong
def tokenAndRoleVerfication(db,token, allowedRoles = None,parentLock = False): # Bei None sind einfach alle Rollen zugelassen
    if not token:
        return False, None, jsonify({"error": "Token wurden nicht übermittelt"}), 400
    if not verificationDatatype(token,"uuid4"):
        return False, None, jsonify({"error": "Token wurden falsch übermittelt"}), 400


    userID = db.getUseridFromToken(token)

    if userID == False:
        return False, None, jsonify({"error": "token ist nicht valid"}), 450


    role = db.getRolefromUserWithUserID(userID)

    if parentLock: #etwas darf nur von Eltern oder erwachsenen SuS bearbeitet werden
        if role == 1: #Student
            birthDate = db.getBirthdateWithUserID(userID)
            if not isAdult(birthDate):
                return False, None,jsonify({"error": "user do not have the permission to enter the site"}), 403
        

    if role == 0: #Parent
            childUserID = db.getChildUserIDWithParentUserID(userID)
            print(childUserID)
            birthDate = db.getBirthdateWithUserID(childUserID)
            print(birthDate)
            if isAdult(birthDate):
                return False, None,jsonify({"error": "user do not have the permission to enter the site"}), 403
            else:
                userID = childUserID
                role = 1

   


    if allowedRoles == None:
        return True,userID,None,None


    

    if role not in allowedRoles:
        return False, None,jsonify({"error": "user do not have the permission to enter the site"}), 403
    
    return True,userID,None,None

    




app = Flask(__name__)
CORS(app)


#Macht Upload Folder ready und speichert Pfad für später, siehe file
uploadFolder = "userDocuments"
os.makedirs(uploadFolder, exist_ok=True)



#ERRORS:
#450: token is invalid


#route musste angepasst werden wegen dem Server
@app.route('/changePassword', methods=["POST"])
def requestChangePassword():

    data = request.get_json()

    if not data:
        return jsonify({"error": "kein JSON gesendet"}), 400

    if not isEveryDataNameinObject(data, [["password","string"], ["newpassword","string"]]):
        return jsonify({"error": "username und password wurden nicht übermittelt"}), 400



    token = request.headers.get("token")
    db = get_db()
    boolien,userID,json,errorNumber = tokenAndRoleVerfication(db,token)

    if not boolien:
        return json,errorNumber


    password = data["password"]
    newPassword = data["newpassword"]
    output = db.changePassword(userID,password,newPassword)

    if output:
        return jsonify({}), 200
    
    return jsonify({"error": "password ist nicht valid"}), 403


@app.route('/login', methods=["POST"])
def loginUser():
    data = request.get_json()

    if not data:
        return jsonify({"error": "kein JSON gesendet"}), 400

    if not isEveryDataNameinObject(data, [["username","string"],["password","string"]]):
        return jsonify({"error": "username und password wurden nicht übermittelt"}), 400

      

    db = get_db()
    username = data["username"]
    password = data["password"]

    userID = db.isUserValid_getUserID(username,password)
    
    if userID == False:
        return jsonify({"error": "username and password are wrong"}), 400

    token = db.addNewToken(userID)
    role = db.getRolefromUserWithUserID(userID)

    return jsonify({"token": token, "role": role}), 200

@app.route('/endSession', methods=["Get"])
def deletToken():


    token = request.headers.get("token")


    if not token:
        return jsonify({"error": "Token wurden nicht übermittelt"}), 400


    db = get_db()
    db.deletToken(token)

    return jsonify({}), 200

@app.route('/getGradesStudent', methods=["Get"])
def postAllGradesFromUser():

    token = request.headers.get("token")
    db = get_db()
    boolien,userID,json,errorNumber = tokenAndRoleVerfication(db,token,[1])

    if not boolien:
        return json,errorNumber



    output = service.getAllGradesforStudents(db,userID)


    return jsonify({"subjects": output}), 200

@app.route('/addNewTest', methods=["Post"])
def addNewTest():

    token = request.headers.get("token")
    db = get_db()
    boolien,userID,json,errorNumber = tokenAndRoleVerfication(db,token,[2])

    if not boolien:
        return json,errorNumber

    #User ist nun Lehrer und hat gültigen Token



    data = request.get_json()

    if not data:
        return jsonify({"error": "kein JSON gesendet"}), 400


    if not isEveryDataNameinObject(data,[["courseID","uuid4"],["testName","string"],["weight","int"],["location","string"],["starttime","dateMinute"],["endtime","dateMinute"],["description","string"]]):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400


    courseID = data["courseID"]
    testName = data["testName"]
    weight = data["weight"]
    location = data["location"]
    starttime = data["starttime"]
    endtime = data["endtime"]
    describtion = data["description"]

    if not db.isUserIDinCourse(userID,courseID):
        return jsonify({"error": "user do not have the permission to change that"}), 403

    service.addNewExamenForCourseWithEventAndDefaultGrades(db,courseID,testName,weight,location,starttime,endtime,describtion)

    return jsonify({}), 200

#Teacher only
@app.route('/deleteTest', methods=["Post"])
def deleteTest():

    token = request.headers.get("token")
    db = get_db()
    boolien,userID,json,errorNumber = tokenAndRoleVerfication(db,token,[2])

    if not boolien:
        return json,errorNumber

    #User ist nun Lehrer und hat gültigen Token



    data = request.get_json()

    if not data:
        return jsonify({"error": "kein JSON gesendet"}), 400


    if not isEveryDataNameinObject(data,[["eventID","uuid4"]]):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400


    eventID = data["eventID"]


    if not db.isUserIDinEvent(userID,eventID):
        return jsonify({"error": "user do not have the permission to change that"}), 403


    db.deleteAllGradesWithEventID(eventID)
    db.deleteEventWithEventID(eventID)
    db.deleteExamWithEventID(eventID)


    return jsonify({}), 200


#Teacher only
@app.route('/getAllTests', methods=["get"])
def getAllTests():

    token = request.headers.get("token")
    db = get_db()
    boolien,userID,json,errorNumber = tokenAndRoleVerfication(db,token,[2])

    if not boolien:
        return json,errorNumber



    output = service.getAllCoursesWithAllExamsFromUserID(db,userID)

    return jsonify({"courses": output}), 200


#Teacher only
@app.route('/getAllGradesFromTest', methods=["get"])
def getAllGradesFromAllStudentsOfTest():

    token = request.headers.get("token")
    db = get_db()
    boolien,userID,json,errorNumber = tokenAndRoleVerfication(db,token,[2])

    if not boolien:
        return json,errorNumber


    eventID = request.args.get("eventID")
    courseID = request.args.get("courseID")

    if eventID == None or courseID == None:
        return jsonify({"error": "Einträge im JSON fehlen"}), 400

    if not verificationDatatype(eventID,"uuid4"):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400
    
    if not verificationDatatype(courseID,"uuid4"):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400




    if not db.isUserIDinCourse(userID,courseID):
        return jsonify({"error": "user do not have the permission to change that"}), 403

    grades = service.getAllGradesFromAllStudentsOfTest(db,eventID)
    exam = service.getAllExamAndEventDataWithEventID(db,eventID)

    return jsonify({"grades": grades,"exam":exam}), 200


@app.route('/testFcmToken', methods=["Post"])
def testFcmToken():

    data = request.get_json()

    if not data:
        return jsonify({"error": "kein JSON gesendet"}), 400

    if not isEveryDataNameinObject(data,[["fcmToken","string"]]):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400


    fcmToken = data["fcmToken"]

    print(fcmToken)
    print("wurde ausgeführt")

    notification.sendNotification(fcmToken,"Test","Der Token funktioniert!!!")


    return jsonify({}), 200


#Only for teacher
@app.route('/postAllGradesFromAllStudentsOfTest', methods=["Post"])
def postAllGradesFromAllStudentsOfTest():

    token = request.headers.get("token")
    db = get_db()
    boolien,userID,json,errorNumber = tokenAndRoleVerfication(db,token,[2])

    if not boolien:
        return json,errorNumber




   
    data = request.get_json()

    if not data:
        return jsonify({"error": "kein JSON gesendet"}), 400

    if not isEveryDataNameinObject(data, [["grades", "list"], ["exam", "dict"]]):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400


    exam = data["exam"]
    grades = data["grades"]

    if not isEveryDataNameinObject(exam, [["courseID", "uuid4"], ["eventID", "uuid4"]]):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400

    courseID = exam["courseID"]
    
    eventID = exam["eventID"]

    if not db.isUserIDinCourse(userID,courseID):
        return jsonify({"error": "user do not have the permission to change that"}), 403
    
    if not db.isUserIDinEvent(userID,eventID):
        return jsonify({"error": "user do not have the permission to change that"}), 403

    print("test 0")



    response = service.updateAllExamAndEventDataWithEventIDAndCourseID(db,exam)
    print("test 0.5")
    if not response:
        return jsonify({"error": "Objekt war falsch"}), 400

    service.updateAllGradesFromAllStudentsOfTest(db,grades,eventID)

    return jsonify({}), 200

@app.route('/postFcmToken', methods=["Post"])
def postFcmToken():

    token = request.headers.get("token")
    db = get_db()
    boolien,userID,json,errorNumber = tokenAndRoleVerfication(db,token)

    if not boolien:
        print("Probleme mit der Token verifikation")
        return json,errorNumber




   
    data = request.get_json()

    if not data:
        print("DATA wird nicht mitgeschickt")
        return jsonify({"error": "kein JSON gesendet"}), 400

    #neuerung, wenn nicht uuid bei hardwareID, dann neuzuweisen und prüfen ob fcmToken stimmt
    if not isEveryDataNameinObject(data, [["fcmToken", "string"]]):
        print("FCM Token wird nicht gesendet")
        return jsonify({"error": "Einträge im JSON fehlen"}), 400
    
    
    fcmToken = data["fcmToken"]
    print(fcmToken)


    service.postFcmToken(db,userID,fcmToken)
    print("alles hat funktioniert mit dem Token")

    
    notification.sentNotificationToUserID(db,userID,"ANGEMOLDEN","Sie haben sich erfolgreich angemolden",5)






    return jsonify({}), 200




@app.route('/getUserData', methods=["Get"])
def getAllUserData():

    token = request.headers.get("token")
    db = get_db()
    boolien,userID,json,errorNumber = tokenAndRoleVerfication(db,token)

    if not boolien:
        return json,errorNumber


    output = service.getAllUserData(db,userID)


    return jsonify(output), 200

@app.route('/postUserData', methods=["post"])
def postAllUserInformation():

    token = request.headers.get("token")
    db = get_db()
    boolien,userID,json,errorNumber = tokenAndRoleVerfication(db,token)

    if not boolien:
        return json,errorNumber

    
    data = request.get_json()

    if not data:
        return jsonify({"error": "kein JSON gesendet"}), 400


    if not isEveryDataNameinObject(data,[["userName", "string"],["email", "string"],["notifAbsenceOfTeacherToday","int"],["notifAbsenceOfTeacherTomorrow","int"],["notifExamTomorrow","int"],["notifEventTomorrow","int"],["notifAbsenceDueTomorrow","int"]]):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400


    


    boolien = service.postAllUserInformation(db,data,userID)

    if boolien:
        return jsonify({}), 200


    return jsonify({"error": "Einträge im JSON sind falsch"}), 400


@app.route('/getSchedule', methods=["Get"])
def getSchedule():

    token = request.headers.get("token")
    db = get_db()
    boolien,userID,json,errorNumber = tokenAndRoleVerfication(db,token)

    if not boolien:
        return json,errorNumber


    starttime = request.args.get("starttime")
    endtime = request.args.get("endtime")



    if starttime == None or endtime == None:
        return jsonify({"error": "Fehlender Parameter"}), 400

    if not verificationDatatype(starttime,"dateMinute"):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400
    
    if not verificationDatatype(endtime,"dateMinute"):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400


    output = service.getSchedule(db,userID,starttime,endtime)


    return jsonify({"schedule": output}), 200


@app.route('/absence', methods=["post"])
def changeAndMergeAbsence():

    token = request.headers.get("token")
    db = get_db()
    boolien,userID,json,errorNumber = tokenAndRoleVerfication(db,token)

    if not boolien:
        return json,errorNumber


    data = request.get_json()

    if not data:
        return jsonify({"error": "kein JSON gesendet"}), 400


    requestType = request.args.get("requestType")
    
    if requestType == None:
        jsonify({"error": "Fehlender Parameter"}), 400


    if requestType == "change":
      
        if not isEveryDataNameinObject(data,[["absenceID","uuid4"],["excused","int"],["description", "string"],["fileID", "uuid4"]]):
            return jsonify({"error": "Einträge im JSON fehlen"}), 400
        
        if service.changeAbsence(db,userID,db.getRolefromUserWithUserID(userID),data):
            return jsonify({}), 200
    
    if requestType == "merge":
        if not isEveryDataNameinObject(data,[["absenceIDList","list"]]):
            return jsonify({"error": "Einträge im JSON fehlen"}), 400

            
        
        if service.mergeAbsence(db,userID,db.getRolefromUserWithUserID(userID),data["absenceIDList"]):
            return jsonify({}), 200



    return jsonify({"error": "Ein Fehler ist aufgetreten"}), 400


@app.route('/absence', methods=["get"])
def getAbsence():
    token = request.headers.get("token")
    db = get_db()
    boolien,userID,json,errorNumber = tokenAndRoleVerfication(db,token)

    if not boolien:
        return json,errorNumber
    

    output = []

    role = db.getRolefromUserWithUserID(userID)

    if role == 2:
        output = service.getAbsenceTeacher(db,userID)


    if role < 2:
        output = []
        output.append(service.getAbsenceUser(db,userID))
    

    return jsonify({"absence": output}), 200

    
@app.route('/absence', methods=["delete"])
def deleteAbsenceEvent():

    token = request.headers.get("token")
    db = get_db()
    boolien,userID,json,errorNumber = tokenAndRoleVerfication(db,token,allowedRoles = [2])

    if not boolien:
        return json,errorNumber


    data = request.get_json()

    if not data:
        return jsonify({"error": "kein JSON gesendet"}), 400


    
    if not isEveryDataNameinObject(data,[["userID","uuid4"],["eventID","uuid4"],["absenceID","uuid4"]]):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400
        

    #EventID mit CourseID austauschen::::
    db.deleteAbsenceEventInEvent(userID,data["userID"],data["eventID"],data["absenceID"])




    return jsonify({}), 200




@app.route('/presenceList', methods=["get"])
def getAnwesenheitsliste():
    token = request.headers.get("token")
    db = get_db()
    boolien,userID,json,errorNumber = tokenAndRoleVerfication(db,token,allowedRoles = [2])

    if not boolien:
        return json,errorNumber
    

    starttime = request.args.get("starttime")
    endtime = request.args.get("endtime")
    eventID = request.args.get("eventID")
    courseID = request.args.get("courseID")

    print(eventID)
    print(endtime)
    print(starttime)
    print(courseID)


    if starttime == None or endtime == None or eventID == None or courseID == None :
        return jsonify({"error": "Fehlender Parameter"}), 400
    if not verificationDatatype(starttime,"dateMinute"):
        print("starttime is false")
        print(starttime)
        return jsonify({"error": "Einträge im JSON fehlen"}), 400
    
    if not verificationDatatype(endtime,"dateMinute"):
        print("endtime is false")
        print(endtime)
        return jsonify({"error": "Einträge im JSON fehlen"}), 400
    print("hdhdhdh")
    if not verificationDatatype(eventID,"string"):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400
    print("Hello")
    if not verificationDatatype(courseID,"uuid4"):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400
 

    
    print(eventID)
    



    output = service.getAnwesenheitsliste(db,userID,courseID,eventID,starttime,endtime)

    if output == False:
        return jsonify({"error": "Fehler bei der Verarbeitung"}), 400



    lesson = {
        "eventID": eventID,
        "courseID": courseID,
        "starttime": starttime,
        "endtime": endtime
    }
    

    return jsonify({"anwesenheitsliste": output, "lesson": lesson}), 200



@app.route('/presenceList', methods=["post"])
def postAnwesenheitsliste():
    token = request.headers.get("token")
    db = get_db()
    boolien,userID,json,errorNumber = tokenAndRoleVerfication(db,token,allowedRoles = [2])

    if not boolien:
        return json,errorNumber
    


    data = request.get_json()

    if not data:
        return jsonify({"error": "kein JSON gesendet"}), 400
    
    """

    starttime = request.args.get("starttime")
    endtime = request.args.get("endtime")
    eventID = request.args.get("eventID")
    courseID = request.args.get("courseID")

    if starttime == None or endtime == None or eventID == None or courseID == None :
        return jsonify({"error": "Fehlender Parameter"}), 400
    if not verificationDatatype(starttime,"dateMinute"):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400
    if not verificationDatatype(endtime,"dateMinute"):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400
    if not verificationDatatype(eventID,"string"):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400
    if not verificationDatatype(courseID,"uuid4"):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400
    """
    
    if not isEveryDataNameinObject(data,[["anwesenheitsliste","list"],["lesson","dict"]]):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400
    
    if not isEveryDataNameinObject(data["lesson"],[["eventID","string"],["courseID","uuid4"], ["starttime","dateMinute"],["endtime","dateMinute"]]):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400

    anwesenheitsliste = data["anwesenheitsliste"]

    lesson = data["lesson"]

    courseID = lesson["courseID"]
    eventID = lesson["eventID"]
    starttime = lesson["starttime"]
    endtime = lesson["endtime"]

    



    output = service.postAnwesenheitsliste(db,userID,courseID,eventID,starttime,endtime,anwesenheitsliste)

    if output == False:
        return jsonify({"error": "Fehler bei der Verarbeitung"}), 400
    

    return jsonify({}), 200
    

    


@app.route("/file", methods=["POST"])
def uploadFile():

    token = request.headers.get("token")
    db = get_db()
    boolien,userID,json,errorNumber = tokenAndRoleVerfication(db,token)

    if not boolien:
        return json,errorNumber




    if "file" not in request.files:
        return jsonify({"error": "No file was sent"}), 400

    file = request.files["file"]
    

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400



    #Permission muss zuerst noch abgefragt werden!!!!!!
    #Fehlt noch!!!!!



    oldFileName = file.filename
    fileID, newFileName = db.addNewFile(oldFileName)
    file.save(os.path.join(uploadFolder, newFileName))

    return jsonify({"fileID": fileID}), 200


@app.route("/file/<fileID>", methods=["GET"])
def download_file(fileID):
    
    token = request.headers.get("token")
    db = get_db()
    boolien,userID,json,errorNumber = tokenAndRoleVerfication(db,token)

    if not boolien:
        return json,errorNumber


    if fileID == "" or fileID == None:
        return jsonify({"error": "User do not have permission"}), 400
    if not verificationDatatype(fileID, "uuid4"):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400
    
    if not service.isUserHavePermissionToFileID(db,userID,fileID):
        return jsonify({"error": "User do not have permission"}), 400




    #get File


    nameBefor,nameAfter = db.getNamesOfFile(fileID)

    print(nameBefor)
    print(nameAfter)

    path = os.path.join(uploadFolder, nameAfter)
    if not os.path.exists(path):
         return jsonify({"error": "fileID don't exist"}), 400
    

    return send_from_directory(
        uploadFolder,
        nameAfter,
        as_attachment=True,
        download_name=nameBefor
    )





#Nicht anfassen!!!


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False)
