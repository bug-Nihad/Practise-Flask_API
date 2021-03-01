from flask_restful import Api, Resource
from flask import request, jsonify, Flask
from pymongo import MongoClient
import bcrypt
import spacy

#Initializing Flask App
app = Flask(__name__)
api = Api(app)

#Setting Up Mongo db
client = MongoClient("mongodb://localhost:27017")
db = client["Plagarism"]
users = db["users"]

#Check if the username already exists or not
def checkUser(username):
    search = users.find({"username": username})
    if search.count() == 0:
        return False
    else:
        return True

#Check Valildity of Auth
def checkValidity(username, password):
    name = users.find_one({"username": username})
    hashedPw = name["password"]
    if bcrypt.hashpw(password.encode('utf8'), hashedPw) == hashedPw:
        return 1
    else:
        return 0

#Check for remaining token of a certain user
def checkToken(username):
    return users.find_one({"username": username})["tokens"]

#Check Similarity of 2 strings.
def checkSimilarity(sentence_1, sentence_2):
    nlp = spacy.load('en_core_web_sm')
    string_1 = nlp(sentence_1)
    string_2 = nlp(sentence_2)
    ratio = string_1.similarity(string_2)
    return ratio

#Resource for registering user
class Register(Resource):
    def post(self):
        #Getting Posted Data
        posted_data = request.json
        username = posted_data["username"]
        password = posted_data["password"]
        #Checking if user exist
        userexist = checkUser(username)
        if userexist:
            retJson = {
                "status": 301,
                "message": "Username exists. Try different one."
            }
            return jsonify(retJson)

        #Hashing the password for storing
        hashedPw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        #If all set, Store the data and return a response
        users.insert_one({
            "username": username,
            "password": hashedPw,
            "tokens": 6
        })
        retJson = {
            "status": 200,
            "message": "User registered successfully."
        }
        return jsonify(retJson)

#Resource for checking similarity of 2 strings.
class Similarity(Resource):
    def post(self):
        #Getting Posted Data
        posted_data = request.json
        username = posted_data["username"]
        password = posted_data["password"]
        sentence_1 = posted_data["sen1"]
        sentence_2 = posted_data["sen2"]

        #Checking for Authentication Validity
        validAuth = checkValidity(username, password)
        if validAuth == 0:
            retJson = {
                "status": 302,
                "message": "Authentication Invalid."
            }
            return jsonify(retJson)

        #Checking if token exists or not
        remainingToken = checkToken(username)
        if remainingToken <=0:
            retJson = {
                "status": 301,
                "message": "You are out of token."
            }
            return jsonify(retJson)

        #If all are ok, Check the similarity, decrease a token and return a response.
        similarityRatio = checkSimilarity(sentence_1, sentence_2)*100
        users.update({"username": username},
                     {
                         "$set":{
                             "tokens": remainingToken -1    #Update token no.
                         }
                     })
        retJson = {
            "status": 200,
            "message": "Similarity Determined Successfully.",
            "percentage": similarityRatio
        }
        return jsonify(retJson)

#Resource for refilling token.
class Refill(Resource):
    def post(self):
        #Get posted Data
        posted_data = request.json
        username = posted_data["username"]
        pw = posted_data["adminpwd"]
        refillAmount = posted_data["refill"]
        adminpw = "xyz123"
        #Check if username exists or not
        if not checkUser(username):
            retJson = {
                "status": 301,
                "message": "Username invalid"
            }
            return jsonify(retJson)
        #Check if admin password is correct
        if pw != adminpw:
            retJson = {
                "status": 304,
                "message": "Invalid Admin Password."
            }
            return jsonify(retJson)

        #All are set. Update the token number.
        remainingToken = checkToken(username)
        users.update({"username": username},{
            "$set": {
                "tokens": remainingToken + refillAmount
            }
        })
        retJson = {
            "status": 200,
            "message": "Token Refilled Successfully."
        }
        return jsonify(retJson)






#Assigning all resources with addresses
api.add_resource(Register, '/register')
api.add_resource(Similarity, '/check')
api.add_resource(Refill, '/refill')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=True)






