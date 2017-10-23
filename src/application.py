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


line_nb = 3
col_nb = 3
creator_symbol = "X"


@application.route("/slack/init_display", methods=["POST"])
def init_display():
    print('----------- REQ INIT -----------')
    print(request.form)
    sys.stdout.flush()
    set_user(request.form["user_id"])
    return Response(json.dumps(json_data), mimetype='application/json')


def count_x_o(json_displayed):
    x_o_number = {
        "X": 0,
        "O": 0,
        "?": 0
    }
    for attachment in json_displayed["attachments"]:
        for action in attachment["actions"]:
            x_o_number[action["text"]] = x_o_number[action["text"]]+1

    return x_o_number


def is_my_turn(username, game_creator, json_displayed):
    x_o_number = count_x_o(json_displayed)
    print('X_O_NUMBER ', x_o_number)
    if x_o_number['X'] <= x_o_number['O']:
        return username == game_creator
    return username != game_creator



def check_win_condition(json_displayed, symbol):
    att = json_displayed["attachments"]
    if (att[0]["actions"][0]["text"] == att[0]["actions"][1]["text"] == att[0]["actions"][2]["text"] == symbol) or \
    (att[1]["actions"][0]["text"] == att[1]["actions"][1]["text"] == att[1]["actions"][2]["text"] == symbol) or \
    (att[2]["actions"][0]["text"] == att[2]["actions"][1]["text"] == att[2]["actions"][2]["text"] == symbol) or \
    (att[0]["actions"][0]["text"] == att[1]["actions"][0]["text"] == att[2]["actions"][0]["text"] == symbol) or \
    (att[0]["actions"][1]["text"] == att[1]["actions"][1]["text"] == att[2]["actions"][1]["text"] == symbol) or \
    (att[0]["actions"][2]["text"] == att[1]["actions"][2]["text"] == att[2]["actions"][2]["text"] == symbol) or \
    (att[0]["actions"][0]["text"] == att[1]["actions"][1]["text"] == att[2]["actions"][2]["text"] == symbol) or \
    (att[0]["actions"][2]["text"] == att[1]["actions"][1]["text"] == att[2]["actions"][0]["text"] == symbol):
        return True
    return False

@application.route("/slack/game", methods=["POST"])
def game():
    print('----------- REQ GAME -----------')
    print(request.form)
    sys.stdout.flush()
    form_json = json.loads(request.form["payload"])
    game_creator = form_json["callback_id"]
    print("GC ",game_creator)
    print("CU ",form_json["user"]["id"])
    sys.stdout.flush()
    json_displayed = form_json["original_message"]

    if not is_my_turn(form_json["user"]["id"], game_creator, json_displayed):
        return Response(json.dumps(form_json["original_message"]), mimetype='application/json')

    line_col = form_json["actions"][0]["value"].split(':')
    line = int(line_col[0])
    col = int(line_col[1])
    if json_displayed["attachments"][line]["actions"][col]["text"] != "?":
        return Response(json.dumps(json_displayed), mimetype='application/json')

    symbol = "X" if form_json["user"]["id"] == game_creator else "O"
    print("SYMBOL ", symbol)
    sys.stdout.flush()

    json_displayed["attachments"][line]["actions"][col]["text"] = symbol

    if check_win_condition(json_displayed, symbol):
        return Response("WIN {username}".format(username=form_json["user"]["name"]))

    return Response(json.dumps(json_displayed), mimetype='application/json')


def set_user(username):
    for attachment in json_data["attachments"]:
        attachment["callback_id"] = username


def init():
    for i in range(line_nb):
        attachment = {
            "callback_id":"{username}",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
            ]
        }
        for j in range(col_nb):
            act = {
                "name": "data{line}:{col}".format(line=i, col=j),
                "text": "?",
                "type": "button",
                "value": "{line}:{col}".format(line=i, col=j)
            }
            attachment["actions"].append(act)

        json_data["attachments"].append(attachment)


if __name__ == '__main__':
    init()
    flaskrun(application)
