import re
import json
import facebook
from pprint import pprint
from pymongo import MongoClient

def load_json(filename):
    with open(filename) as json_data:
        data = json.load(json_data)
    return data

def getdata(message):
    data = load_json('keywords.json')

    startFound = False
    destFound = False
    searchObj = re.search(r'([a-zA-Z() ]*)(?:-+>*| to )([a-zA-Z ,.]*)', message, re.M|re.I)
    # searchObj = re.search(r'([a-zA-Z]*) (?:to) *([a-zA-Z]*)', message, re.M|re.I)
    if searchObj:
        start = searchObj.group(1).lower()
        dest = searchObj.group(2).lower()

        # print start.lower(), dest.lower()
        locations = data["locations"].items()
        for k, v in locations:
            # print k, v
            # if start.lower() in v:
            for val in v:
                extra_begin_char = '[A-Za-z0-9]' + val
                extra_end_char = val + '[A-Za-z0-9]'
                if re.search(val, start, re.M|re.I) and not re.search(extra_begin_char, start, re.M|re.I) and not re.search(extra_end_char, start, re.M|re.I):
                    start = k
                    startFound = True
                # if dest.lower() in v:
                if re.search(val, dest, re.M|re.I) and not re.search(extra_begin_char, dest, re.M|re.I) and not re.search(extra_end_char, dest, re.M|re.I):
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
            print "Nothing found! for " + message
            start = None
            dest = None
    else:
        # print "Nothing found! for " + message
        start = None
        dest = None

    # returns if driver route (default = False), and start and destination
    if destFound:
        lower_mess = message.lower()
        for keyword in data["riding-keys"]:
            if re.search(keyword, lower_mess, re.M|re.I):
                return False, start, dest
        for keyword in data["driving-keys"]:
            if re.search(keyword, lower_mess, re.M|re.I):
                return True, start, dest
        for unclear_word in data["ambiguous-keys"]:
            if re.search(unclear_word, lower_mess, re.M|re.I):
                if '?' in lower_mess:
                    return False, start, dest
                return True, start, dest
    return True, start, dest

def main():
    print "\n\n"
    # Get MongoDB collection
    MDB_URL = "mongodb://test:test@ds145329.mlab.com:45329/searchmyride"

    client = MongoClient(MDB_URL)

    db = client["searchmyride"]
    collection = db["names"]
    db.names.delete_many({})

    # get token from Graph Explorer API, give user access options by checkmarks
    token = '1506656972703387|XWNdzbKLOrqwT61ylrtH_kQZgkk'
    graph = facebook.GraphAPI(access_token=token, version=2.10)
    page = graph.get_object(id='459693560717220/feed', limit="100", fields="updated_time, message, from")
    # routeTypeList = []
    # startList = []
    # destList = []
    # timeList = []
    # nameList = []
    # linkList = []
    documentList = []

    # all_info = {}
    for i, post in enumerate(page["data"]):
        if not post.get("message"):
            continue 
        message = post["message"]
        is_driving_route, start, dest = getdata(message)
        if not post.get("updated_time"):
            continue 
        time = post["updated_time"]
        if not post.get("from") or not post["from"].get("name"):
            continue 

        name = post["from"]["name"]
        link = "http://www.facebook.com/" + post["id"] 
        if start and dest:
            document = {}
            document["type"] = "Driving" if is_driving_route else "Riding"
            document["start"] = start
            document["dest"] = dest
            document["time"] = time
            document["name"] = name
            document["link"] = link
            document["message"] = message
            documentList.append(document)

            # routeTypeList.append("Driving" if is_driving_route else "Riding")
            # startList.append(start)
            # destList.append(dest)
            # timeList.append(time)
            # nameList.append(name)
            # linkList.append(link)

    db.names.insert_many(documentList)

    # for i in range(len(documentList)):
    #     print documentList[i]
        # print routeTypeList[i], startList[i], destList[i], timeList[i], nameList[i], linkList[i]
        # print i, post
    #     all_info[i] = (post["message"], post["updated_time"])

    # pprint(all_info)
    # getdata(line)

if __name__ == "__main__":
    main()
