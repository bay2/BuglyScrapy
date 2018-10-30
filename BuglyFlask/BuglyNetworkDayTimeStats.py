from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with
from mongodbTool import mongodb
import time

parser = reqparse.RequestParser()
parser.add_argument('date', type=str, required=False, help='Rate cannot be converted')

api_resource_stats_fields = {
    'hour': fields.String(attribute='_id'),
    'count': fields.Integer,
}

class BuglyNetworkDayTimeStats(Resource):

    @marshal_with(api_resource_stats_fields, envelope='data')
    def get(self):

        args = parser.parse_args()
        date = args['date']

        if date is None:
            date = time.strftime("%Y-%m-%d", time.localtime())
            pass

        return self.getErrorStatsFromDate(date)

    def getErrorStatsFromDate(self, date):

        carshTimeConversionHour = {
            '$addFields': {
                'hour': { 
                    '$hour': {
                        '$dateFromString': {
                            'dateString': '$crashTime'
                        }
                    }
                }
                
            }
        }

        matchDate = {
            '$match': {
                'crashTime': { 
                    "$regex": date
                }
            }
        }

        groupAndSum = {
            '$group': {
                '_id': '$hour',
                'count': {
                    '$sum': 1
                }
            }
        }

        sort = {
            "$sort": {
                "_id": 1
            }
        }

        obj = mongodb.collection.aggregate([
            matchDate,
            carshTimeConversionHour,
            groupAndSum,
            sort
            ])
        
        return list(obj)