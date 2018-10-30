# -*- coding: utf-8 -*-
import scrapy
from ..login import BuglyLogin
import time
import json
from ..stringTool import StringTool
from scrapy.loader import ItemLoader
from ..items import BuglyscrapyIssueItem
from ..mongodbTool import mongodb
from scrapy.conf import settings
import pymongo

class BuglySpider(scrapy.Spider):
    name = 'bugly'
    allowed_domains = ['bugly.qq.com']
    start_urls = ['http://bugly.qq.com/']

    def start_requests(self):
        bugly = BuglyLogin()
        bugly.login(settings['BUGLY_USERNAME'], settings['BUGLY_PASSWORD'])

        self.header = bugly.get_header('https://bugly.qq.com/v2/users/null/appList')
        self.cookies = bugly.get_cookies()

        while(len(self.header) == 0):
            time.sleep(1)
            self.header = bugly.get_header('https://bugly.qq.com/v2/users/null/appList')
            self.cookies = bugly.get_cookies()
            pass


        return [scrapy.Request("https://bugly.qq.com/v2/users/null/appList?" + "userId=" + settings['BUGLY_USERNAME'], 
        callback=self.appListParse,
        headers=self.header,
        cookies=self.cookies)]

    def start_requestIssueList(self, appId, errorCode):
        return scrapy.Request("https://bugly.qq.com/v2/issueList?" + 
        'start=0&searchType=errorType&exceptionTypeList=AllCatched,Unity3D,Lua,JS' + 
        '&search=' + errorCode + 
        '&pid=2&platformId=2&sortOrder=desc&rows=50&sortField=uploadTime' + 
        '&appId=' + appId, 
        callback=self.issueListParse,
        headers=self.header,
        cookies=self.cookies
        )

    def start_requestsErrorInfoDetail(self, appId, platformId, hash):
        return scrapy.Request('https://bugly.qq.com/v2/crashDoc/appId/' + appId + '/platformId/' + platformId + '/crashHash/' + hash,
        callback=self.errorInfoParse,
        headers=self.header,
        cookies=self.cookies
        )

    def start_requestsCrashList(self, appId, platformId, issueId, start, rows, callback):
        return scrapy.Request(url='https://bugly.qq.com/v2/crashList?searchType=detail&exceptionTypeList=AllCatched,Unity3D,Lua,JS&pid=2&start=' + 
        start + 
        '&rows=' + rows + 
        '&appId=' + appId +
        '&platformId=' + platformId +
        '&issueId=' + issueId,
        callback=callback,
        headers=self.header,
        cookies=self.cookies
        )

    def crashListParse(self, response):
        crashDatas = json.loads(response.text)['ret'].get('crashDatas', [])

        for crashHash in crashDatas:

            query = mongodb.collection.find_one({"_id": crashHash})

            if query is None:
                yield self.start_requestsErrorInfoDetail(self.appId, self.platformId, crashHash)

        pass

    def errorInfoParse(self, response):

        data = json.loads(response.text)['ret']
        crashMap = data['crashMap']
        fileList = data['detailMap']['fileList']

        il = BuglyscrapyIssueItem()
        il['_id'] = crashMap['id']

        il['productVersion'] = crashMap['productVersion']
        il["model"] = crashMap['model']
        il["userId"] = crashMap['userId']
        il["expName"] = crashMap['expName']
        il["expMessage"] = crashMap['expMessage']
        il["deviceId"] = crashMap['deviceId']
        il["processName"] = crashMap['processName']
        il["uploadTime"] = crashMap['uploadTime']
        il["crashTime"] = crashMap['crashTime']

        for fileInfo in fileList:
            if fileInfo['fileName'] == 'valueMapOthers.txt':
                map = StringTool.valueMapOthersToMap(fileInfo['fileContent'])
                il['api'] = map.get('API Path', "")
                il['apiParams'] =  map.get('请求参数', "") 
                il['reachabilityStatus'] = map.get('ReachabilityStatus', "")
                il['operator'] =  map.get('运营商', "")
            pass

        yield il
        
        pass

    
    def issueListParse(self, response):
        data = json.loads(response.text)['ret']
        self.appId = data['appId']
        self.platformId = data['platformId']
        issueList = data['issueList']
        
        for issue in issueList:
            crashNum = int(issue['crashNum'])
            issueId = issue['issueId']
            start = 0
            row = 50

            while(start < crashNum):
                start += row
                yield self.start_requestsCrashList(self.appId, self.platformId, issueId, str(start), str(row), self.crashListParse)
            pass
        pass



    def appListParse(self, response):
        for appInfo in json.loads(response.text)['ret']:
            if appInfo["appName"] == settings['BUGLY_APPNAME']:
                yield self.start_requestIssueList(appInfo["appId"], "-1001")
        pass
