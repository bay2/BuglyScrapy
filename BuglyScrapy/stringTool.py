content = 'C03_Process:EAFriendShop;A23:3.5.1(3);C01:44452;F01:1;C03_运营商:中国移动;C03_ReachabilityStatus:WiFi;C03_请求参数:{↵    latitude = 0;↵    longitude = 0;↵    type = 2;↵};C03_API Path:/friendshop/36/home/adinfo2.do;'


class StringTool(object):

    @staticmethod
    def valueMapOthersToMap(valueMapOthers):


        content = valueMapOthers
        # content = content.replace("\\u21b5", "")
        # newcontent = bytes(content, 'utf-8')
        # content = newcontent.decode('unicode_escape')
        mapsStrArr = content.split('C03_')
        attMap = {}
        for str1 in mapsStrArr:

            value = str1.split(':')
            if len(value) == 2:
                attMap[value[0]] = value[1].rstrip(';')
            pass

        pass

        print(attMap)

        return attMap

    pass

def main():
    map = StringTool.valueMapOthersToMap(content)
    print(map)
    
 

if __name__ == "__main__":
    main()


