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
    "text": "Tic tac toe ?",
    "replace_original": "true",
    "response_type": "in_channel",
    "attachments": [
    ]
}


line_nb = 2
col_nb = 2


@application.route("/slack/init_display", methods=["POST"])
def init_display():
    print(json_data)
    sys.stdout.flush()
    return Response(json.dumps(json_data), mimetype='application/json')


@application.route("/slack/game", methods=["POST"])
def game():
    print(request.form)
    sys.stdout.flush()
    form_json = json.loads(request.form["payload"])
    line_col = form_json["actions"][0]["value"].split(':')
    original_msg = form_json["original_message"]
    line = int(line_col[0])
    col = int(line_col[1])
    if original_msg["attachments"][line]["actions"][col]["text"] == "-":
        original_msg["attachments"][line]["actions"][col]["text"] = 1
    else:
        original_msg["attachments"][line]["actions"][col]["text"] = int(original_msg["attachments"][line]["actions"][col]["text"])+1

    return Response(json.dumps(original_msg), mimetype='application/json')


def init():
    for i in range(line_nb):
        print(json.dumps(json_data, indent=4, sort_keys=True))
        attachment = {
            "callback_id":"bla",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
            ]
        }
        for j in range(col_nb):
            act = {
                "name": "data",
                "text": "-",
                "type": "button",
                "value": ""
            }
            act["value"] = "{line}:{col}".format(line=i, col=j)
            print(act["value"])
            attachment["actions"].append(act)

        json_data["attachments"].append(attachment)


if __name__ == '__main__':
    init()
    print(json.dumps(json_data, indent=4, sort_keys=True))
    flaskrun(application)
