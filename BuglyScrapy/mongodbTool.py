# -*- coding: utf-8 -*-
import pymongo
from . import settings
import time


class MongodbTool:

    def __init__(self):
        connection = pymongo.MongoClient(host=settings.MONGODB_SERVER, port=settings.MONGODB_PORT, username=settings.MONGODB_USERNAME, password=settings.MONGODB_PASSWORD)
        self.db = connection[settings.MONGODB_DB]
        self.collection = self.db[settings.MONGODB_COLLECTION]
        pass


mongodb = MongodbTool()


def main():

    collection = mongodb.db['User_Stat']

    beginTime = time.strptime('2018110500', '%Y%m%d%H')
    endTime = time.strptime('2018110523', '%Y%m%d%H')
    obj = collection.find({
        'date': {'$gte': beginTime, '$lt': endTime}
    })
    dateList = list(obj)

    # obj2 =  obj.aggregate([{"$max": "count"}])
    print(dateList)


    
 

if __name__ == "__main__":
    main()
