from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with
from mongodbTool import mongodb

parser = reqparse.RequestParser()
parser.add_argument('count', type=int, required=False, help='Rate cannot be converted')

api_resource_error_fields = {
    'name': fields.String(attribute='_id'),
    'count': fields.Integer,
}

class BuglyNetworkStats(Resource):

    @marshal_with(api_resource_error_fields, envelope='data')
    def get(self):

        args = parser.parse_args()
        count = args['count']

        aggregate =  [
            {"$group": {"_id": "$api", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
         ]

        if count is not None:
            aggregate.append({'$limit': count})


        obj = mongodb.collection.aggregate(aggregate)
        apiErrorCountList = list(obj)

        return apiErrorCountList
    pass