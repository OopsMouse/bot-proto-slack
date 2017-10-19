#!flask/bin/python
from flask import Flask
from flaskrun import flaskrun
import os

application = Flask(__name__)


@application.route('/', methods=['GET'])
def get():
    test = ""
    if "SLACK_BOT_TOKEN" not in os.environ:
        test += "not found SLACK_BOT_TOKEN"
    else:
        test += os.environ["SLACK_BOT_TOKEN"]
    if "AWS_ACCESS_KEY_ID" not in os.environ:
        test += "not found AWS_ACCESS_KEY_ID"
    else:
        test += os.environ["AWS_ACCESS_KEY_ID"]
    if "AWS_SESSION_TOKEN" not in os.environ:
        test += "not found AWS_SESSION_TOKEN"
    else:
        test += os.environ["AWS_SESSION_TOKEN"]

    return '{"Output":"Hello World - GET"} %s' % test


@application.route('/', methods=['POST'])
def post():
    return '{"Output":"Hello World - POST"}'


if __name__ == '__main__':
    flaskrun(application)
