# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from .mongodbTool import mongodb
from . import items
import time




class BuglyscrapyPipeline(object):


    def process_item(self, item, spider):

        if isinstance(item, items.BuglyscrapyIssueItem):
            mongodb.collection.insert(dict(item))
        elif isinstance(item, items.BuglyscrapyUserSumItem):

            data = {
                '_id': item['date'],
                'date': time.strptime(item['date'], '%Y%m%d%H'),
                'accessUser': item['accessUser']
            }

            print('process_item save')

            mongodb.db['User_Stat'].update({'_id': item['date']}, data, upsert=True)

        
        return item
