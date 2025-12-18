import json

from flask import Flask, request, Response
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



if __name__ == '__main__':
    app.run(host="0.0.0.0")