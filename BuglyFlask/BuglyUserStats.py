from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with
from mongodbTool import mongodb
import time
import datetime

parser = reqparse.RequestParser()
parser.add_argument('startHour', type=str, required=True)
parser.add_argument('endHour', type=str, required=True)

api_resource_user_sum_fields = {
    
}

class BuglyUserStats(Resource):

    # @marshal_with(api_resource_user_sum_fields, envelope='data')

    def mapUserSumInfo(self, userSumInfo):
        # print(type(userSumInfo['date']))
        timeArr = userSumInfo['date']
        hourDate = datetime.datetime(timeArr[0], timeArr[1], timeArr[2], timeArr[3], timeArr[4], timeArr[5])
        return  {'hour': hourDate.hour, 'accessUser': userSumInfo['accessUser']}
        pass

    def get(self):
        args = parser.parse_args()
        startHour = args['startHour']
        endHour = args['endHour']

        collection = mongodb.db['User_Stat']

        beginTime = time.strptime(startHour, '%Y%m%d%H')
        endTime = time.strptime(endHour, '%Y%m%d%H')
        obj = collection.find({
            'date': {'$gte': beginTime, '$lte': endTime}
        })

        return list(map(self.mapUserSumInfo, list(obj)))

    pass