# -*- coding: utf-8 -*-
import pymongo
import settings




class MongodbTool:

    def __init__(self):
        connection = pymongo.MongoClient(host=settings.MONGODB_SERVER, port=settings.MONGODB_PORT, username=settings.MONGODB_USERNAME, password=settings.MONGODB_PASSWORD)
        db = connection[settings.MONGODB_DB]
        self.collection = db[settings.MONGODB_COLLECTION]
        pass


mongodb = MongodbTool()


def main():
    # obj = mongodb.collection.find_one({"_id": "60:D3:BB:AC:40:16:88:4F:0F:54:32:0A:C4:D4:BC:8F"})
    obj = mongodb.collection.aggregate([{"$group": {"_id": "$api", "count": {"$sum": 1}}}, {'maxCount': {'$max': '$group.$count'}}])
    apiErrorCountList = list(obj)

    # obj2 =  obj.aggregate([{"$max": "count"}])
    print(obj)

    for errorCount in apiErrorCountList:
        print('api name:' + errorCount.get('_id', '') + ' ' + str(errorCount.get('count')))
        pass
    
 

if __name__ == "__main__":
    main()
