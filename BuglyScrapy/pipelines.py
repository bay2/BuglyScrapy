# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings

from .mongodbTool import mongodb




class BuglyscrapyPipeline(object):


    def process_item(self, item, spider):
        mongodb.collection.insert(dict(item))
        return item
