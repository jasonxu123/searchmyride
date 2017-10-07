import facebook
import json
from pprint import pprint
# get token from Graph Explorer API, give user access options by checkmarks
# 60 day token, no need to refresh periodically
token = '1506656972703387|XWNdzbKLOrqwT61ylrtH_kQZgkk'
graph = facebook.GraphAPI(access_token=token, version=2.10)
page = graph.get_object(id='459693560717220/feed', limit="100", fields="updated_time, message, from")

all_info = {}
for i, post in enumerate(page["data"]):
	all_info[i] = (post["message"], post["updated_time"], post["from"]["name"], "http://www.facebook.com/" + post["id"])
# the u' before strings = unicode
pprint(all_info)

