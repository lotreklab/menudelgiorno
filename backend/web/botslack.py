import os
import time
import re
import slack

slack_token = os.environ['SLACK_BOT_TOKEN']
client = slack.WebClient(token=slack_token)

def sendMenuMessage():
    client.chat_postMessage(
    channel="testbotmenu",
    text="Menù di oggi"
    )