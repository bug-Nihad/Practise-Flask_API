from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from pymongo import MongoClient
import bcrypt

client = MongoClient("mongodb://localhost:27017")
db = client["SentenceDatabase"]
users = db["users"]

app = Flask(__name__)
api = Api(app)

#Defining all the function required
def verifyPw(username, password):
    hashed_pw = users.find_one({"User name" : username})['Password']
    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return 1
    return 0
def countTokens(username):
    token = users.find_one({"User name": username})["Tokens"]
    return token

#Defining all the resources
class Register(Resource):
    def post(self):
        #Step_1 : Get Posted Data
        posted_data = request.json
        #Step_2: Get the data
        user_name = posted_data['username']
        password = posted_data['password']
        #hash = hash(password, salt)  = aklsgsfakgjsofjawfkf
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        #Store Username and Password
        users.insert_one(
            {
                "User name" : user_name,
                "Password": hashed_pw,
                "Sentence": "",
                "Tokens": 10
            }
        )
        #Return a response
        ret_json = {
            "status": 200,
            "message": "You seccesfully signed up for the API"
        }
        return jsonify(ret_json)

class Store(Resource):
    def post(self):
        #Get the posted Data
        posted_data = request.json
        #Read the data
        username = posted_data['username']
        password = posted_data['password']
        sentence = posted_data['sentence']
        #Verify authentication
        correct_pw = verifyPw(username, password)
        if correct_pw == 0:
            ret_json = {
                'status': 302,
                'message': 'Authentication Invalid'
            }
            return jsonify(ret_json)
        #Verify User have enough tokens
        remaining_tokens = countTokens(username)
        if remaining_tokens == 0:
            ret_json = {
                'status': 301,
                'message': 'You are out of token.'
            }
            return jsonify(ret_json)
        #Store the sentence and return response 200
        users.update({"User name": username},
                     {
                         "$set":{
                             "Sentence": sentence,
                             "Tokens": remaining_tokens - 1
                         }
                     })
        ret_json = {
            "status": 200,
            "message": "Sentences Saved Succesfully."
        }
        return jsonify(ret_json)

class Retrieve_Sentence(Resource):
    def get(self):
        #Getting and Reading the data
        posted_data = request.json
        username = posted_data["username"]
        password = posted_data["password"]
        #Verifying Authentication
        correctPw = verifyPw(username, password)
        if correctPw == 0:
            ret_json = {
                'status': 302,
                'message': 'Authentication Invalid'
            }
            return jsonify(ret_json)
        #Checking for remaining token
        remaining_token = countTokens(username)
        if remaining_token == 0:
            ret_json = {
                'status': 301,
                'message': 'You are out of token.'
            }
            return jsonify(ret_json)
        #If all set, retrieve the sentence and return it as a response
        sentence = users.find_one({"User name": username})["Sentence"]
        users.update({"User name": username},
                     {
                         "$set":{
                             "Tokens": remaining_token - 1
                         }
                     })
        ret_json = {
            "status": 200,
            "message": sentence
        }
        return jsonify(ret_json)


#Link all the resources with url
api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Retrieve_Sentence, '/retrieve')



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80, debug=False)