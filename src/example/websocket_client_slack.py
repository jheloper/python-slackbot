import websockets
import asyncio
from urllib import request, parse
import json


@asyncio.coroutine
def hello():
    # slack bot api token require.
    data = parse.urlencode({'token': 'xoxb-92362021782-VSWuGa8F8eYmOpf8eqwuSzEP'})
    data = data.encode('ascii')
    res = request.urlopen('https://slack.com/api/rtm.start', data)
    res_dict = json.loads(res.read().decode('utf-8'))
    websocket = yield from websockets.connect(res_dict['url'])

    while True:
        msg = yield from websocket.recv()
        msg_json = json.loads(msg)
        if msg_json['type'] in ['hello', 'message']:
            print("< {}".format(msg))

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()
