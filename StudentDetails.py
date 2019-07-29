from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from flask_pymongo import PyMongo
import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydb"

mongo = PyMongo(app)
api = Api(app)

class StudentResults(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='args', required=True)
        args = parser.parse_args()

        course_id = ''
        result = []

        query = {'CourseName': args['name']}
        course_data = mongo.db.CourseDetails.find(query)

        #Below if Condition Checks if Course Exist
        if(course_data.count() == 0):
            print("Zero Records from Mongo")
            raise InvalidUsage('The Course Doesnot Exit, Please give a valid Course Name', 200)

        student_data = mongo.db.Student.find()

        #In Below Loop Extracting ObjectId value and Converting it to String for the query retrieved
        for i in course_data:
            print("The Document fetched from mongo is: ", i)
            course_id = str(i['_id'])
            print("course_id is: ", course_id)

        #In Below Loop, Checking for all the Students for the Course and appending it to result
        for j in student_data:
            course_in_student = j['CourseId']

            for k in course_in_student:
                if(k == course_id):
                    result.append(j)

        f_out = json.dumps(result, cls=JSONEncoder, indent=4)
        print("The Final Output to be sent is: ", f_out)
        final_output = json.loads(f_out)

        return ({"ListofStudents": final_output})

class InvalidUsage(Exception):
    status_code = 400
    def __init__(self, message, status_code=None, payload=None):

        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_bad_request(error):
   response = jsonify(error.to_dict())
   response.status_code = error.status_code
   return response

@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Please Check the request once again"}), 404


api.add_resource(StudentResults, '/course')

if __name__ == "__main__":
    app.run(debug = True)