from slacker import Slacker

slack = Slacker('xoxb-92362021782-k3xEOKSd2w7CadqRtYmY9jhs')

res = slack.rtm.start()
print(res.body['url'])
