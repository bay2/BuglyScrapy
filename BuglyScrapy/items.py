# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BuglyscrapyIssueItem(scrapy.Item):

    _id = scrapy.Field(serializer=str)
    
    productVersion = scrapy.Field(serializer=str)
    model = scrapy.Field(serializer=str)
    userId = scrapy.Field(serializer=str)
    deviceId = scrapy.Field(serializer=str)
    processName = scrapy.Field(serializer=str)

    expName = scrapy.Field(serializer=str)
    expMessage = scrapy.Field(serializer=str)

    uploadTime = scrapy.Field(serializer=str)
    crashTime = scrapy.Field(serializer=str)

    valueMapOthers = scrapy.Field(serializer=dict)

    api = scrapy.Field()
    apiParams = scrapy.Field()
    operator = scrapy.Field()
    reachabilityStatus = scrapy.Field()

    pass

class BuglyscrapyUserSumItem(scrapy.Item):
    accessUser = scrapy.Field(serializer=int)
    date = scrapy.Field(serializer=str)


    pass
