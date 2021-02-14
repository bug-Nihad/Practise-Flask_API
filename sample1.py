from flask_restful import Resource, Api
from flask import Flask, jsonify, request

app = Flask(__name__)
api = Api(app)

data = {
    'nihad' : {
        'name': 'Tahsin Sayed Nihad',
        'age' : 23,
        'gender' : 'male'
    },
    'tarin' : {
        'name' : 'secret',
        'age' : 22,
        'gender' : 'female'
    }
}

class helloworld(Resource):
    # def get(self, name, num):
    #     return {'data': name, 'num' : num}
    # def post(self):
    #     return {'data' : 'posted'}
    def get(self, name):
        return data[name]

class video(Resource):
    # def get(self, video_id):
    #     return
    def post(self):
        da = request.form
        return jsonify(da)



api.add_resource(helloworld, '/hello/<string:name>')
api.add_resource(video, '/video')
if __name__ == "__main__":
    app.run(debug=True)
