import facebook
import json
from pprint import pprint
# get token from Graph Explorer API, give user access options by checkmarks
#token = 'EAACEdEose0cBABOZA77ZC1JNNu7ptgEdZCaSwqnqG0NwZB2uYZADNwHxKCmDmZAMERMfRINxSjdYgys0xnnWpbCLu5ke2hxAoqYiBeDNuPL95WA0yvmhO67c4HWDZBkTlWUE4SoPQ5oyXb4ZA3GdfaBU9yTmZBGYdbjxfyZAeoAp9GM7VR0wGXFx19hy3pWf4moloZD'
token = '1506656972703387|XWNdzbKLOrqwT61ylrtH_kQZgkk'
graph = facebook.GraphAPI(access_token=token, version=2.10)
page = graph.get_object(id='459693560717220/feed')

all_info = {}
for i, post in enumerate(page["data"]):
	all_info[i] = (post["message"], post["updated_time"])
pprint(all_info)

