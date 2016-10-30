import json
import websockets
import asyncio
import logging
import requests
import src.commands as cmds

# debug logger...
logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

# sercet file read, this file content is api token, key, and other secrets...
secrets = open('../secret.json')
secrets_data = json.loads(secrets.read())
SLACK_API_TOKEN = secrets_data.get('SLACK_API_TOKEN')
secrets.close()


class SlackBot:

    def __init__(self, token):
        self.token = token
        self.websocket = None
        self.id = None

    def connect_rtm(self):
        response = requests.post('https://slack.com/api/rtm.start', data={'token': self.token}).json()
        self.id = response.get('self').get('id')

        if response.get('ok') is True and response.get('url') is not None:
            return response.get('url')
        else:
            raise Exception('Slack RTM API Connect is failed...')

    @asyncio.coroutine
    def listen_rtm(self):
        try:
            self.websocket = yield from websockets.connect(self.connect_rtm())
            while True:
                recv_msg = yield from self.websocket.recv()
                msg_json = json.loads(recv_msg)
                print(msg_json)
                channel = msg_json.get('channel')
                user = msg_json.get('user')
                if self.preprocess(msg_json):
                    messages = self.parse_message(msg_json.get('text'))
                    command_result = self.route_commands(messages)
                    yield from self.websocket.send(json.dumps({"id": 1, "type": "message", "channel": channel,
                                                               "text": '<@{0}> {1}'.format(user, command_result)}))
        except Exception as e:
            print(e)

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
        print(len(messages))
        if len(messages) < 3:
            return messages

        if messages[2].find('"') == 0 and messages[2].count('"') == 2:
            sub_msg = messages[2].rsplit('" ', 1)
            messages[2] = sub_msg[0].replace('"', '')
        else:
            messages[1] = 'Invalid Parameter'
        return messages[1:]

    def route_commands(self, messages):
        command = messages[0]

        if command == '/지도':
            command_result = cmds.search_location(messages[1])
        elif command == '/번역':
            command_result = cmds.search_translate(messages[1])
        elif command == '/날씨':
            command_result = cmds.search_weather(messages[1])
        elif command == 'Invalid Parameter':
            command_result = '파라미터가 유효하지 않습니다.'
        else:
            command_result = '무슨 말씀이신지 잘 모르겠어요...'

        return command_result

if __name__ == '__main__':
    sb = SlackBot(SLACK_API_TOKEN)
    asyncio.get_event_loop().run_until_complete(sb.listen_rtm())
