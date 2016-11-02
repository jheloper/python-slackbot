import asyncio
import json

import requests
import websockets

from src import secrets


@asyncio.coroutine
def echo():
    ws_url = None
    bot_id = None
    res = requests.post('https://slack.com/api/rtm.start',
                        data={'token': secrets.SLACK_API_TOKEN}).json()

    if res.get('ok'):
        bot_id = res.get('self').get('id')
        ws_url = res.get('url')
    else:
        print('RTM Start Failed...')

    ws = yield from websockets.connect(ws_url)

    while True:
        recv_msg = yield from ws.recv()
        print(type(recv_msg))
        recv_json = json.loads(recv_msg)
        if recv_json.get('type') == 'message' and recv_json.get('text').startswith('<@{}>'.format(bot_id)):
            msg = recv_json.get('text').split(' ', 1)
            print(msg)
            yield from ws.send(json.dumps({"id": 1, "type": "message", "channel": recv_json.get('channel'),
                                                   "text": '<@{0}> {1}'.format(recv_json.get('user'), msg[1])}))

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(echo())
