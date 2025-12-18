import json
from flask import Flask, request, Response, render_template
import database




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



if __name__ == '__main__':
    app.run(host="0.0.0.0")