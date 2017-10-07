import re
import json
import facebook
from pprint import pprint

def load_json(filename):
    with open(filename) as json_data:
        data = json.load(json_data)
    return data

def getdata(message):
    data = load_json('keywords.json')

    startFound = False
    destFound = False
    searchObj = re.search(r'([a-zA-Z ]*) *(?:-+>*| to ) *([a-zA-Z ]*)', message, re.M|re.I)
    # searchObj = re.search(r'([a-zA-Z]*) (?:to) *([a-zA-Z]*)', message, re.M|re.I)
    if searchObj:
        start = searchObj.group(1)
        dest = searchObj.group(2)

        # print start.lower(), dest.lower()
        for k, v in data["locations"].items():
            # print k, v
            # if start.lower() in v:
            for loc in v:
                if loc in start.lower():
                    start = k
                    startFound = True
                # if dest.lower() in v:
                if loc in dest.lower():
                    dest = k
                    destFound = True
                if startFound and destFound:
                    break
            if startFound and destFound:
                break
        if destFound:
            if not startFound:
                start = "UCLA"
            # print "start: " + start + "\tdest: " + dest
        else:
            # print "Nothing found! for " + message
            start = None
            dest = None
    else:
        # print "Nothing found! for " + message
        start = None
        dest = None

    # returns if driver route (default = False), and start and destination
    if destFound:
        lower_mess = message.lower()
        for keyword in data["driving-keys"]:
            if keyword in lower_mess:
                return True, start, dest
        for keyword in data["riding-keys"]:
            if keyword in lower_mess:
                return False, start, dest
        for unclear_word in data["ambiguous-keys"]:
            if unclear_word in lower_mess:
                if '?' in lower_mess:
                    return False, start, dest
                return True, start, dest
    return False, start, dest

def main():
    # get token from Graph Explorer API, give user access options by checkmarks
    token = '1506656972703387|XWNdzbKLOrqwT61ylrtH_kQZgkk'
    graph = facebook.GraphAPI(access_token=token, version=2.10)
    page = graph.get_object(id='459693560717220/feed', limit="100", fields="updated_time, message, from")
    routeTypeList = []
    startList = []
    destList = []
    timeList = []
    nameList = []
    linkList = []

    # all_info = {}
    for i, post in enumerate(page["data"]):
        is_driving_route, start, dest = getdata(post["message"])
        time = post["updated_time"]
        name = post["from"]["name"]
        link = "http://www.facebook.com/" + post["id"] 
        if start and dest:
            routeTypeList.append("Driving" if is_driving_route else "Riding")
            startList.append(start)
            destList.append(dest)
            timeList.append(time)
            nameList.append(name)
            linkList.append(link)

    for i in range(len(startList)):
        print routeTypeList[i], startList[i], destList[i], timeList[i], nameList[i], linkList[i]
        # print i, post
    #     all_info[i] = (post["message"], post["updated_time"])

    # pprint(all_info)
    # getdata(line)

if __name__ == "__main__":
    main()
