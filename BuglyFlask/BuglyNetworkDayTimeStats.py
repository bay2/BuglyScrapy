from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with
from mongodbTool import mongodb
import time
import datetime

parser = reqparse.RequestParser()
parser.add_argument('date', type=str, required=False, help='Rate cannot be converted')

api_resource_stats_fields = {
    'hour': fields.String,
    'count': fields.Integer,
    'accessUser': fields.Integer
}

class BuglyNetworkDayTimeStats(Resource):

    

    @marshal_with(api_resource_stats_fields, envelope='data')
    def get(self):

        args = parser.parse_args()
        date = args['date']

        if date is None:
            date = time.strftime("%Y-%m-%d", time.localtime())
            pass

        timeErrorList = self.getErrorStatsFromDate(date)
        userSumList = self.getUserSumFromDate(time.localtime())

        outDic = list()

        for timeoutInfo in timeErrorList:

            outInfo = {
                'hour': timeoutInfo['_id'], 
                'count': timeoutInfo['count'], 
                'accessUser': userSumList[timeoutInfo['_id']]['accessUser']}
            outDic.append(outInfo)
            pass

        return outDic

    def mapUserSumInfo(self, userSumInfo):
        # print(type(userSumInfo['date']))
        timeArr = userSumInfo['date']
        hourDate = datetime.datetime(timeArr[0], timeArr[1], timeArr[2], timeArr[3], timeArr[4], timeArr[5])
        return  {'hour': hourDate.hour, 'accessUser': userSumInfo['accessUser']}
        pass

    def getUserSumFromDate(self, date):

        collection = mongodb.db['User_Stat']

        beginTime = time.strptime(time.strftime('%Y%m%d00', date), '%Y%m%d%H')
        endTime = time.strptime(time.strftime('%Y%m%d23', date), '%Y%m%d%H')
        obj = collection.find({
            'date': {'$gte': beginTime, '$lte': endTime}
        })

        return list(map(self.mapUserSumInfo, list(obj)))

        pass

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