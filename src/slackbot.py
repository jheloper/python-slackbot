from urllib import request, parse
import json
import websockets
import asyncio
import logging
import requests


# 디버그용 로거, 나중에 삭제할 예정.
logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class SlackBot:

    def __init__(self, token):
        self.token = token
        self.websocket = None
        self.id = None

    def connect_rtm(self):
        connect_data = parse.urlencode({'token': self.token}).encode('ascii')
        response = request.urlopen('https://slack.com/api/rtm.start', connect_data)
        res_json = json.loads(response.read().decode('utf-8'))
        self.id = res_json['self']['id']

        if res_json['ok'] is True and res_json['url'] is not None:
            return res_json['url']
        else:
            raise Exception('slack rtm api connect is fail...')

    @asyncio.coroutine
    def listen_rtm(self):
        self.websocket = yield from websockets.connect(self.connect_rtm())
        while True:
            msg = yield from self.websocket.recv()
            msg_json = json.loads(msg)
            if msg_json['type'] in ['hello']:
                print("slack bot connect success!, message is {}".format(msg))
            elif msg_json['type'] in ['message'] and msg_json.get('text', '') is not None:
                messages = self.convert_message(msg_json.get('text', ''))
                if messages[0] == '<@{}>'.format(self.id):
                    self.check_commands(messages[1:])

    def convert_message(self, message):
        message = str(message)
        if len(message) > 0:
            return message.split()
        else:
            raise Exception('message is not...')

    def check_commands(self, messages):
        messages = list(messages)
        print(messages)
        if len(messages) > 1:
            print(messages[0])
            if messages[0] == '지도':
                t = parse.urlencode({'query': '토즈 홍대점', 'type': 'SITE_1'}).encode('ascii')
                print(t)
                self.send_message('http://map.naver.com/?' + t.decode())
            elif messages[0] == '번역':
                self.send_message('https://translate.google.co.kr/?hl=ko&tab=wT#en/ko/hello+world')
        elif len(messages) > 0:
            self.send_message(messages[0])
        else:
            pass

    def send_message(self, message):
        connect_data = parse.urlencode({'token': self.token, 'channel': '#general', 'text': message, 'as_user': 'true'}).encode('ascii')
        response = request.urlopen('https://slack.com/api/chat.postMessage', connect_data)
        res_json = json.loads(response.read().decode('utf-8'))


sb = SlackBot('xoxb-92362021782-k3xEOKSd2w7CadqRtYmY9jhs')
asyncio.get_event_loop().run_until_complete(sb.listen_rtm())
asyncio.get_event_loop().run_forever()
