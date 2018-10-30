from flask import Flask, jsonify, request
import flask_restful
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with
from flask_cors import CORS, cross_origin
import json
from BuglyNetworkStats import BuglyNetworkStats
from BuglyNetworkDayTimeStats import BuglyNetworkDayTimeStats

app = Flask(__name__)
CORS(app, support_credentials=True)
api = Api(app, default_mediatype='application/json')

api.add_resource(BuglyNetworkStats, '/networkErrorSum')
api.add_resource(BuglyNetworkDayTimeStats, '/daytimestats')

if __name__ == '__main__':
    app.run(debug=True)
