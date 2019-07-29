from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_pymongo import PyMongo
import json
from bson import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydb"

