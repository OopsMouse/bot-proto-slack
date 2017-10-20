#!flask/bin/python
import sys
from flask import Flask, request, make_response, Response
from flaskrun import flaskrun
import json

from slackclient import SlackClient

application = Flask(__name__)

SLACK_BOT_TOKEN = '8huAA0FFQebvGDJrjhpUVAQk'

# Slack client for Web API requests
slack_client = SlackClient(SLACK_BOT_TOKEN)


json_data = {
    "text": "Would you like to play a game?",
    "replace_original": "true",
    "response_type": "in_channel",
    "attachments": [
    ]
}

attachments = {
    "callback_id":"bla",
    "color": "#3AA3E3",
    "attachment_type": "default",
    "actions": [
    ]
}
actions = {
    "name": "data",
    "text": "-",
    "type": "button",
    "value": "",
    "blabla":"test"
}

line_nb = 3
col_nb = 3

@application.route("/slack/init_display", methods=["POST"])
def init_display():
    return Response(json.dumps(json_data), mimetype='application/json')


@application.route("/slack/game", methods=["POST"])
def game():
    print(request.form)
    sys.stdout.flush()
    form_json = json.loads(request.form["payload"])
    line_col = form_json["actions"][0]["value"].split(':')
    original_msg = json.dumps(form_json["original_message"])
    line = int(line_col[0])
    col = int(line_col[1])
    print(line)
    print(col)
    print(original_msg)
    sys.stdout.flush()

    original_msg["attachments"][line]["actions"][col]["text"] = original_msg["attachments"][line]["actions"][col]["text"]+1
    return Response(json.dumps(original_msg), mimetype='application/json')


def init():
    for i in range(line_nb):
        attachment = attachments.copy()
        for j in range(col_nb):
            actions["value"] = "{line}:{col}".format(line=i, col=j)
            attachment["actions"].append(actions)
        json_data["attachments"].append(attachment)


if __name__ == '__main__':
    init()
    flaskrun(application)
