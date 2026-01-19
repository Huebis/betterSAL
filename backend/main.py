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

    data = request.get_json()

    if not data:
        return jsonify({"error": "kein JSON gesendet"}), 400

    if "password" not in data or "newpassword" not in data or "token" not in data:
        return jsonify({"error": "password, neues password und token wurden nicht übermittelt"}), 400


    token = data["token"]
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

    return jsonify({"token": token}), 200



@app.route('/endSession', methods=["Post"])
def deletToken():
    data = request.get_json()
    print(data)

    if not data:
        return jsonify({"error": "kein JSON gesendet"}), 400

    if "token" not in data:
        return jsonify({"error": "Token wurden nicht übermittelt"}), 400

    token = data["token"]
    db = get_db()
    db.deletToken(token)

    return jsonify({}), 200


@app.route('/userData', methods=["POST"])
def postAllUserInformation():
    data = request.get_json()

    if not data:
        return jsonify({"error": "kein JSON gesendet"}), 400

    if "token" not in data:
        return jsonify({"error": "token wurden nicht übermittelt"}), 400



    token = data["token"]
    db = get_db()

    userID = db.getUseridFromToken(token)

    if userID == False:
        return jsonify({"error": "token ist nicht valid"}), 403

    userData = db.getAllUserDataWithUserID(userID)


    return jsonify({"data": userData}), 200






###########################################################
#Tests#
########################################


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']


    if database.isUserValid(username,password):
        return render_template("login.html")
    return render_template("loginNotRight.html")



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
