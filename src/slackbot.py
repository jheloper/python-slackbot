import json
import websockets
import asyncio
import logging
import requests
import src.commands as cmds

# debug logger...
logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

# sercet file read, this file content is api token, key, and other secrets...
secrets = json.loads(open('../secret.json').read())


class SlackBot:

    def __init__(self, token):
        self.token = token
        self.websocket = None
        self.id = None

    def connect_rtm(self):
        response = requests.post('https://slack.com/api/rtm.start', data={'token': self.token})
        res_json = response.json()
        self.id = res_json['self']['id']

        if res_json['ok'] is True and res_json['url'] is not None:
            return res_json['url']
        else:
            raise Exception('Slack RTM API Connect is failed...')

    @asyncio.coroutine
    def listen_rtm(self):
        self.websocket = yield from websockets.connect(self.connect_rtm())
        while True:
            recv_msg = yield from self.websocket.recv()
            msg_json = json.loads(recv_msg)
            if self.preprocess(msg_json):
                messages = self.parse_message(msg_json.get('text'))
                self.route_commands(messages)

    def preprocess(self, msg_json):
        if msg_json.get('type') == 'hello':
            print('Slack Bot Connect Success! Bot Say Hello!')
            return False
        elif msg_json.get('type') == 'message' and msg_json.get('text') is not None:
            if msg_json.get('text').startswith('<@{0}>'.format(self.id)):
                return True
        else:
            return False

    def parse_message(self, message_text):
        message_text = str(message_text)
        messages = message_text.split(' ', 2)
        return messages[1:]

    def route_commands(self, messages):
        print(messages)
        command = messages[0]
        if command == '지도':
            self.send_message(cmds.search_location(messages[1]))
        elif command == '번역':
            self.send_message(cmds.search_translate(messages[1]))
        else:
            pass

    def send_message(self, message):
        response = requests.post('https://slack.com/api/chat.postMessage',
                                 data={'token': self.token, 'channel': '#general', 'text': message, 'as_user': 'true'})

sb = SlackBot(secrets['SLACK_API_TOKEN'])
asyncio.get_event_loop().run_until_complete(sb.listen_rtm())
asyncio.get_event_loop().run_forever()
