import requests
import websockets
import asyncio

res = requests.post('https://slack.com/api/rtm.start', data={'token': 'xoxb-92362021782-tySZsEKyuOLFjZP9TbZwTNkR'}).json()
url = None

if res.get('ok'):
    url = res.get('url')
else:
    print('RTM Start Failed...')

@asyncio.coroutine
def echo():
    ws = yield from websockets.connect(url)
    while True:
        recv = yield from ws.recv()
        print(recv)


asyncio.get_event_loop().run_until_complete(echo())
asyncio.get_event_loop().run_forever()
