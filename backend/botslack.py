import os
import time
import re
import slack

slack_token = os.environ['SLACK_BOT_TOKEN']
client = slack.WebClient(token=slack_token)

while True:
    client.chat_postMessage(
    channel="testbotmenu",
    text="prova"
    )
    time.sleep(10)