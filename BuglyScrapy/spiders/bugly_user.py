# -*- coding: utf-8 -*-
import scrapy
from .. import settings
from ..items import BuglyscrapyUserSumItem
import time
from ..login import BuglyLogin
import json


class BuglyUserSpider(scrapy.Spider):
    name = 'bugly_user'
    allowed_domains = ['bugly.qq.com']
    start_urls = ['http://bugly.qq.com/']


    def start_requests(self):
        bugly = BuglyLogin()
        bugly.login(settings.BUGLY_USERNAME, settings.BUGLY_PASSWORD)

        self.header = bugly.get_header('https://bugly.qq.com/v2/users/null/appList')
        self.cookies = bugly.get_cookies()

        while(len(self.header) == 0):
            time.sleep(1)
            self.header = bugly.get_header('https://bugly.qq.com/v2/users/null/appList')
            self.cookies = bugly.get_cookies()
            pass


        return [scrapy.Request("https://bugly.qq.com/v2/users/null/appList?" + "userId=" + settings.BUGLY_USERNAME, 
        callback=self.appListParse,
        headers=self.header,
        cookies=self.cookies)]

    def appListParse(self, response):
        for appInfo in json.loads(response.text)['ret']:
            if appInfo["appName"] == settings.BUGLY_APPNAME:
                self.appId = appInfo['appId']
                beginTime = time.strftime("%Y%m%d00", time.localtime())
                endTime = time.strftime("%Y%m%d23", time.localtime())
                return self.requestGetRealTimeHourlyStat(self.appId, beginTime, endTime)
        pass

    def requestGetRealTimeHourlyStat(self, appId, startHour, endHour):
        url = 'https://bugly.qq.com/v2/getRealTimeHourlyStat/appId/' + appId + '/platformId/2/version/-1/startHour/' + startHour +  '/endHour/' + endHour + '/type/crash'
        return scrapy.Request(url, callback=self.userSumParse, headers=self.header, cookies=self.cookies)

    def userSumParse(self, response):

        for info in json.loads(response.text)['ret']['data']:
            userSumIt = BuglyscrapyUserSumItem()
            userSumIt['accessUser'] = info['accessUser']
            userSumIt['date'] = info['date']
            yield userSumIt

        pass
        


