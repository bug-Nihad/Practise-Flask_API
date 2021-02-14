from flask import Flask, jsonify, request
from flask_restful import Api, Resource
app = Flask(__name__)
api = Api(app)

def check_posted_data(posted_data, function_name):
    if function_name=="add" or function_name=="subtract" or function_name=='multiply':
        if "x" not in posted_data or "y" not in posted_data:
            return 301
        else:
            return 200
    if function_name=="division":
        if "x" not in posted_data or "y" not in posted_data:
            return 301
        elif int(posted_data["y"])==0:
            return 302
        else:
            return 200


class Add(Resource):
    def post(self):
        #Step 1: Get the posted data
        posted_data = request.json
        #Step 2: Verify Validity of the posted data
        status_code = check_posted_data(posted_data, "add")
        #If status code is not 200
        if status_code != 200:
            ret_map = {
                'Message': 'Data missing here..',
                'Status Code': status_code
            }
            return jsonify(ret_map)
        #If all are ok Add the posted data and return them
        x = posted_data["x"]
        y = posted_data["y"]
        sum = int(x) + int(y)
        ret_map = {
            "Message": sum,
            "Status Code": 200
        }
        return jsonify(ret_map)

    def get(self):
        pass
class Subtraction(Resource):
    def post(self):
        posted_data = request.json
        status_code = check_posted_data(posted_data, 'subtract')
        if (status_code!=200):
            ret_map = {
                'Message': 'Data Missing',
                "Status Code": status_code
            }
            return jsonify(ret_map)
        else:
            x = posted_data["x"]
            y = posted_data["y"]
            result = int(x) - int(y)
            ret_map = {
                "Message": result,
                "Status Code": status_code
            }
            return jsonify(ret_map)
class Multiplication(Resource):
    def post(self):
        posted_data = request.json
        status_code = check_posted_data(posted_data, 'multiply')
        if (status_code != 200):
            ret_map = {
                'Message': 'Data Missing',
                "Status Code": status_code
            }
            return jsonify(ret_map)
        else:
            x = posted_data["x"]
            y = posted_data["y"]
            result = int(x) * int(y)
            ret_map = {
                "Message": result,
                "Status Code": status_code
            }
            return jsonify(ret_map)
class Division(Resource):
    def post(self):
        posted_data = request.json
        status_code = check_posted_data(posted_data, 'division')
        if status_code == 301:
            ret_map = {
                "Message" : "Data Missing",
                "Status Code" : status_code
            }
            return jsonify(ret_map)
        elif status_code==302:
            ret_map = {
                "Message": "Zero Division Error. 2nd parameter can't be zero.",
                "Status Code": status_code
            }
            return jsonify(ret_map)

        else:
            x = posted_data["x"]
            y = posted_data["y"]
            result = int(x)/int(y)
            ret_map = {
                "Message": result,
                "Status Code": status_code
            }
            return jsonify(ret_map)

# @app.route('/')
# def root():
#     return 'Hello World'
#
# @app.route('/who')
# def who():
#     who_json = {
#         'name' : 'Tahsin Sayed NIhad',
#         'age' : 22,
#         'gender' : 'M',
#         'phones': [
#             {
#                 'phonename' : 'Nokia',
#                 'phonenumber' : 123
#             },
#             {
#                 'phonename' : 'Xiaomi',
#                 'phonenumber' : 324
#             }
#         ]
#     }
#     return jsonify(who_json)
#
# @app.route('/bye')
# def bye():
#     return 'Get the hell out of here.'

# @app.route('/add_two_nums', methods=["POST"])
# def add_two_nums():
#     dataDict = request.json
#     print(dataDict)
#     total = dataDict['x'] + dataDict['y']
#     return str(total), 200

api.add_resource(Add, '/add')
api.add_resource(Subtraction, '/subtract')
api.add_resource(Multiplication, '/multiply')
api.add_resource(Division, '/division')
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80, debug=True)