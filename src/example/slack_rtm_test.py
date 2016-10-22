from urllib import request, parse
import json


# slack bot api token require.
data = parse.urlencode({'token': 'xoxb-92362021782-VSWuGa8F8eYmOpf8eqwuSzEP'})
data = data.encode('ascii')
res = request.urlopen('https://slack.com/api/rtm.start', data)
res_dict = json.loads(res.read().decode('utf-8'))
print(res_dict['url'])
