from flask import Flask, request, jsonify
from con_mongodb import con
from bson.json_util import dumps
from bson.objectid import ObjectId
app = Flask(__name__)
myClient = con();
myCol = myClient['students']
    
#home_page
@app.route('/')
def home():
    return 'Hello World' 

#error function
@app.errorhandler(404)
def not_found(error = None):
    message = {
                'status': 404,'message': 'Not Found ' + request.url
                }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

#create user by post method
@app.route('/postData',methods=['POST'])
def postData():
    _json = request.json
    name = _json['name']
    rollno = _json['rollno']
    if name and rollno and request.method == 'POST':
        myCol.insert_one({'name': name, 'rollno': rollno}) 
        resp = jsonify('user added successfully')
        resp.status_code = 200        
        return resp
    else:
        return not_found()
        
#get user by id using get method
@app.route('/getUser/<id>',methods=['GET'])
def getUser(id):
    user = myCol.find_one({"_id": ObjectId(id)})
    resp = dumps(user)
    return resp 

#get all users by get method
@app.route('/getAllUsers',methods=['GET'])
def getAllData():
    users =  myCol.find()
    resp = dumps(users)
    return resp

#delete user by delete method
@app.route('/deleteUser/<id>', methods = ['DELETE'])
def deleteUser(id):
    try:
        myCol.delete_one({'_id': ObjectId(id)})
        resp = jsonify("user deleted successfully")
        resp.status_code = 200
        return resp
    except:
        return not_found()

#update user in mongodb by put method
@app.route('/updateUser/<id>', methods=['PUT'])
def updateuser(id):
    try:
        json = request.json
        name = json['name']
        rollno = json['rollno']
        myCol.update_one({"_id": ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)}, {'$set': {"name": name, "rollno": rollno}})
        resp = jsonify("User updated successfully")
        return resp
    except:
        return not_found()
        

if __name__ == "__main__":
    app.run()       