import websockets
import asyncio
from urllib import request, parse
import json


def send_msg():
    data = parse.urlencode({'token': 'xoxb-92362021782-k3xEOKSd2w7CadqRtYmY9jhs', 'channel': '#general', 'text': 'hello!!'})
    data = data.encode('ascii')
    res = request.urlopen('https://slack.com/api/chat.postMessage', data)
    res_dict = json.loads(res.read().decode('utf-8'))
    print(res_dict)


@asyncio.coroutine
def hello():
    # slack bot api token require.
    data = parse.urlencode({'token': 'xoxb-92362021782-k3xEOKSd2w7CadqRtYmY9jhs'})
    data = data.encode('ascii')
    res = request.urlopen('https://slack.com/api/rtm.start', data)
    res_dict = json.loads(res.read().decode('utf-8'))
    websocket = yield from websockets.connect(res_dict['url'])

    while True:
        msg = yield from websocket.recv()
        msg_json = json.loads(msg)
        if msg_json['type'] in ['hello']:
            print("slack bot connect success!, message is {}".format(msg))
        elif msg_json['type'] in ['message'] and msg_json['text'] is not None:
            print(msg)


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()
