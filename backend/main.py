import json
from flask import Flask, request, Response, render_template, g, jsonify
from database import Database
import service
from flask_cors import CORS
import notification


#source venv/bin/activate 



def get_db():
    db = getattr(g, '_database', None)
    print("1")
    if db is None:
        print("2")
        db = g._database = Database()
    return db
 
def isEveryDataNameinObject(testedObject,dataNames):
    for name in dataNames:
        if name not in testedObject:
            return False
    return True


#return True,UserID, None, None when everything is fine
#return False,None, error, Fehlernummer when something is wrong
def tokenAndRoleVerfication(db,token, allowedRoles = None): # Bei None sind einfach alle Rollen zugelassen
    if not token:
        return False, None, jsonify({"error": "Token wurden nicht übermittelt"}), 400


    userID = db.getUseridFromToken(token)

    if userID == False:
        return False, None, jsonify({"error": "token ist nicht valid"}), 450

    if allowedRoles == None:
        return True,userID,None,None


    role = db.getRolefromUserWithUserID(userID)

    if role not in allowedRoles:
        return False, None,jsonify({"error": "user do not have the permission to enter the site"}), 403
    
    return True,userID,None,None

    




app = Flask(__name__)
CORS(app)



#ERRORS:
#450: token is invalid


#route musste angepasst werden wegen dem Server
@app.route('/changePassword', methods=["POST"])
def requestChangePassword():

    data = request.get_json()

    if not data:
        return jsonify({"error": "kein JSON gesendet"}), 400

    if not isEveryDataNameinObject(data, ["password", "newpassword"]):
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

    if not isEveryDataNameinObject(data, ["username", "password"]):
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


    if not isEveryDataNameinObject(data,["courseID","testName","weight","location","date","starttime","endtime","description"]):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400


    courseID = data["courseID"]
    testName = data["testName"]
    weight = data["weight"]
    location = data["location"]
    date = data["date"]
    starttime = data["starttime"]
    endtime = data["endtime"]
    describtion = data["description"]

    if not db.isUserIDinCourse(userID,courseID):
        return jsonify({"error": "user do not have the permission to change that"}), 403

    service.addNewExamenForCourseWithEventAndDefaultGrades(db,courseID,testName,weight,location,date,starttime,endtime,describtion)

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


    if not isEveryDataNameinObject(data,["eventID"]):
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

    if "fcmToken" not in data:
        return jsonify({"error": "Einträge im JSON fehlen"}), 400


    fcmToken = data["fcmToken"]

    print(fcmToken)

    notification.sendPush(fcmToken,"Test","Der Token funktioniert!!!")


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

    if not isEveryDataNameinObject(data, ["grades", "exam"]):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400


    exam = data["exam"]
    grades = data["grades"]

    if not isEveryDataNameinObject(exam, ["courseID", "eventID"]):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400

    courseID = exam["courseID"]
    
    eventID = exam["eventID"]

    if not db.isUserIDinCourse(userID,courseID):
        return jsonify({"error": "user do not have the permission to change that"}), 403

    response = service.updateAllExamAndEventDataWithEventIDAndCourseID(db,exam)
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
        return json,errorNumber




   
    data = request.get_json()

    if not data:
        return jsonify({"error": "kein JSON gesendet"}), 400

    if not isEveryDataNameinObject(data, ["fcmToken", "hardwareID"]):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400

    hardwareID = service.postFcmToken(db,userID,fcmToken,hardwareID)

    return jsonify({"hardwareID": hardwareID}), 200




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


    if not isEveryDataNameinObject(data,["userName","email","notifAbsenceOfTeacherToday","notifAbsenceOfTeacherTomorrow","notifExamTomorrow","notifEventTomorrow","notifAbsenceDueTomorrow"]):
        return jsonify({"error": "Einträge im JSON fehlen"}), 400


    


    boolien = service.postAllUserInformation(db,data,userID)

    if boolien:
        return jsonify({}), 200


    return jsonify({"error": "Einträge im JSON sind falsch"}), 400


###########################################################
#Tests#
########################################




#Testversuch, ob Dateien Hochgeladen werden können und abgespeichert werden
@app.route("/upload", methods=["GET","POST"])
def upload_file():
    if request.method == "GET":
        return render_template("upload.html", message="")



    if "file" not in request.files:
        return render_template("upload.html", message="Keine Datei ausgewählt")

    file = request.files["file"]

    if file.filename == "":
        return render_template("upload.html", message="Keine Datei ausgewählt")


    
    fileId = service.saveNewFile(file)
    return render_template("upload.html", message=f"Datei erfolgreich gespeichert: {fileId}")







if __name__ == '__main__':
    app.run(host="0.0.0.0")
