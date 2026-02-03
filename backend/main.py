import json
from flask import Flask, request, Response, render_template, g, jsonify
from database import Database
import service
from flask_cors import CORS


#source venv/bin/activate 



def get_db():
    db = getattr(g, '_database', None)
    print("1")
    if db is None:
        print("2")
        db = g._database = Database()
    return db
 




app = Flask(__name__)
CORS(app)



#ERRORS:
#0:No error
#1:User already exists
#2:


#route musste angepasst werden wegen dem Server
@app.route('/changePassword', methods=["POST"])
def requestChangePassword():


    token = request.headers.get("token")


    if not token:
        return jsonify({"error": "Token wurden nicht übermittelt"}), 400

    data = request.get_json()

    if not data:
        return jsonify({"error": "kein JSON gesendet"}), 400

    if "password" not in data or "newpassword" not in data:
        return jsonify({"error": "password oder/und neues password wurden nicht übermittelt"}), 400



    db = get_db()

    userID = db.getUseridFromToken(token)

    if userID == False:
        return jsonify({"error": "token ist nicht valid"}), 403

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

    if "username" not in data or "password" not in data:
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


@app.route('/userData', methods=["Get"])
def postAllUserInformation():

    token = request.headers.get("token")


    if not token:
        return jsonify({"error": "Token wurden nicht übermittelt"}), 400


    db = get_db()

    userID = db.getUseridFromToken(token)

    if userID == False:
        return jsonify({"error": "token ist nicht valid"}), 403

    userData = db.getAllUserDataWithUserID(userID)


    return jsonify({"data": userData}), 200



@app.route('/getGradesStudent', methods=["Get"])
def postAllGradesFromUser():

    token = request.headers.get("token")


    if not token:
        return jsonify({"error": "Token wurden nicht übermittelt"}), 400





    db = get_db()

    userID = db.getUseridFromToken(token)

    if userID == False:
        return jsonify({"error": "token ist nicht valid"}), 403


    role = db.getRolefromUserWithUserID(userID)
    if role != 1:#überprüft ob es wirklich ein Schüler*in ist
        return jsonify({"error": "user do not have the permission to enter the site"}), 403

    output = service.getAllGradesforStudents(db,userID)


    return jsonify({"subjects": output}), 200



@app.route('/addNewTest', methods=["Post"])
def addNewTest():

    token = request.headers.get("token")


    if not token:
        return jsonify({"error": "Token wurden nicht übermittelt"}), 400


    db = get_db()

    userID = db.getUseridFromToken(token)

    if userID == False:
        return jsonify({"error": "token ist nicht valid"}), 403


    role = db.getRolefromUserWithUserID(userID)
    if role != 2:#überprüft ob es wirklich ein Lehrer*in ist
        return jsonify({"error": "user do not have the permission to change that"}), 403




    #User ist nun Lehrer und hat gültigen Token



    data = request.get_json()

    if not data:
        return jsonify({"error": "kein JSON gesendet"}), 400

    if "courseID" not in data:
        return jsonify({"error": "Einträge im JSON fehlen"}), 400

    if "testName" not in data:
        return jsonify({"error": "Einträge im JSON fehlen"}), 400

    if "weight" not in data:
        return jsonify({"error": "Einträge im JSON fehlen"}), 400

    if "location" not in data:
        return jsonify({"error": "Einträge im JSON fehlen"}), 400

    if "date" not in data:
        return jsonify({"error": "Einträge im JSON fehlen"}), 400
    if "starttime" not in data:
        return jsonify({"error": "Einträge im JSON fehlen"}), 400
    if "endtime" not in data:
        return jsonify({"error": "Einträge im JSON fehlen"}), 400
    if "description" not in data:
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





    

    output = service.getAllGradesforStudents(db,userID)


    return jsonify({"grades": output}), 200


#Teacher only
@app.route('/getAllTests', methods=["get"])
def getAllTests():

    token = request.headers.get("token")


    if not token:
        return jsonify({"error": "Token wurden nicht übermittelt"}), 400


    db = get_db()

    userID = db.getUseridFromToken(token)

    if userID == False:
        return jsonify({"error": "token ist nicht valid"}), 403


    role = db.getRolefromUserWithUserID(userID)
    if role != 2:#überprüft ob es wirklich ein Lehrer*in ist
        return jsonify({"error": "user do not have the permission to change that"}), 403

    output = service.getAllCoursesWithAllExamsFromUserID(db,userID)

    return jsonify({"courses": output}), 200




###########Nicht fertig #####################################
#Teacher only
@app.route('/getAllGradesFromTest', methods=["get"])
def getAllGradesFromTest():

    token = request.headers.get("token")


    if not token:
        return jsonify({"error": "Token wurden nicht übermittelt"}), 400


    db = get_db()

    userID = db.getUseridFromToken(token)

    if userID == False:
        return jsonify({"error": "token ist nicht valid"}), 403


    role = db.getRolefromUserWithUserID(userID)
    if role != 2:#überprüft ob es wirklich ein Lehrer*in ist
        return jsonify({"error": "user do not have the permission to change that"}), 403

    eventID = request.args.get("eventID")
    courseID = request.args.get("courseID")

    if not db.isUserIDinCourse(userID,courseID):
        return jsonify({"error": "user do not have the permission to change that"}), 403




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
