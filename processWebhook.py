"""
Author: Justin T Joseph
email: jtjjust@gmail.com

--------------Whatsapp-Jira Bot Integration--------------------------

This bot connects Whatsapp to Jira Work Management Projects, 
allowing users to add messages from Whatsapp to the open board in Jira.


API used for jira: jira
API used for WhatsApp: twilio

I have used Ngrok with Flask for testing, sharing, and 
accessing this applications during development
"""


import os
import json
import flask
from flask import send_from_directory, request
from twilio.rest import Client
import re
from jira import JIRA

app = flask.Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/favicon.png')

@app.route('/')
@app.route('/home')
def home():
    return "Hello World"



@app.route('/webhook', methods=['GET', 'POST']) 
def webhook():
    print(request.get_data())
    message = request.form['Body']
    senderId = request.form['From'].split('+')[1]
    print(f'Message --> {message}')
    print(f'Sender id --> {senderId}')
    create_issue_jira(message)
    print("Issue added successfully")
    return '200'



def create_issue_jira(msg):
    jira_url = 'https://chandlerbing647.atlassian.net/'


    with open("config.json") as config_file:
        config = json.load(config_file)
        
    JIRA_EMAIL = config["JIRA_EMAIL"]
    JIRA_TOKEN = config["JIRA_TOKEN"]
    jira = JIRA(server=jira_url,basic_auth=(JIRA_EMAIL, JIRA_TOKEN))
    issue_dict = {
        'project': {'key': 'DEM'},
        'summary': msg,
        'description': '',
        'issuetype': {'name': 'Task'},
    }
    new_issue = jira.create_issue(fields=issue_dict)


if __name__ == "__main__":
    app.run(port=5000, debug=True)