# -*- coding: utf-8 -*-
import pymongo
from scrapy.conf import settings


class MongodbTool:

    def __init__(self):
        connection = pymongo.MongoClient(host=settings['MONGODB_SERVER'], port=settings['MONGODB_PORT'], username=settings['MONGODB_USERNAME'], password=settings['MONGODB_PASSWORD'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        pass


mongodb = MongodbTool()


def main():
    # obj = mongodb.collection.find_one({"_id": "60:D3:BB:AC:40:16:88:4F:0F:54:32:0A:C4:D4:BC:8F"})
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
                "$regex": '2018-10-24'
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

    sort = {"$sort": {"_id": 1}}

    obj = mongodb.collection.aggregate([
        matchDate,
        carshTimeConversionHour,
        groupAndSum,
        sort
        ])
    apiErrorCountList = list(obj)

    print(apiErrorCountList)

    
 

if __name__ == "__main__":
    main()
