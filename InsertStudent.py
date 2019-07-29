from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_pymongo import PyMongo
import json

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydb"

mongo = PyMongo(app)
api = Api(app)

class InsertStudent(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('FirstName', location='json', required=True)
        parser.add_argument('LastName', location='json', required=True)
        parser.add_argument('CourseId', location='json', required=True)
        args = parser.parse_args()
        course_to_insert = ''

        course_data = mongo.db.CourseDetails.find()
        request_data = request.get_json()
        course_to_insert = request_data['CourseId']

        item = []
        for p in course_data:
            item.append(p)


        for i, j in enumerate(course_to_insert):
            print("{} {}".format(i, j))
            for k in item:
                print("the value of k is: ", k)
                if (j == k['CourseName']):
                    request_data['CourseId'][i] = str(k['_id'])

        print(request_data)

        try:
            new_record = mongo.db.Student.insert_one(request_data)
            return jsonify({"message": "Record Inserted Successfully"})
        except Exception as e:
            print(str(e))
            return jsonify({"message": "Error, Record not inserted"})

api.add_resource(InsertStudent, '/create')

if __name__ == "__main__":
    app.run(debug=True)