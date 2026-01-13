import json
from flask import Flask, request, Response, render_template, g, jsonify
from database import Database
import service


#source venv/bin/activate

def get_db():
    db = getattr(g, '_database', None)
    print("1")
    if db is None:
        print("2")
        db = g._database = Database()
    return db
 




app = Flask(__name__)



#ERRORS:
#0:No error
#1:User already exists
#2:

@app.route('/register_user', methods=['GET'])
def register_user():
    data=request.get_json()
    response=0
    #response=createUser(data["username"],data["password"])
    data = json.dumps({"ERROR":response})#{"ERROR: 0"}
    if request.method == 'GET':
        resp = Response(data)
        resp.headers['Content-Type'] = 'application/json'
        return resp


@app.route('/betterSAL/api/login', methods=["POST"])
def loginUser():
    data = request.get_json()
    db = get_db()

    username = data["username"]
    password = data["password"]

    userID = db.isUserValid_getUserID(username,password)

    if userID == False:
        return jsonify({"error": "username and password are wrong"}), 400

    token = db.addNewToken(userID)

    return jsonify({"token": token}), 200




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