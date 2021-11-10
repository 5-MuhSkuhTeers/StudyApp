import requests, os
from flask import url_for
from api import email
from api.models import *
from api.email import *
from datetime import datetime, timedelta


MAILGUN_DOMAIN = os.environ['MAILGUN_TEST_DOMAIN'] if 'MAILGUN_TEST_DOMAIN' in os.environ \
    else 'DOMAIN'

MAILGUN_API_KEY = os.environ['MAILGUN_TEST_API'] if 'MAILGUN_TEST_API' in os.environ \
    else 'API_KEY'

class AssigmentNotifcations:

    # init class
    def __init__(self, taskName, dueDate, dueTime, email):
        self.taskName = taskName
        self.dueDate = dueDate
        self.dueTime = dueTime
        self.email = email

    # convert time format to int- mins
    def convertTimedeltaToMin(self, duration):
      splits = list(str(duration).split(","))
      # if not splits have "_ days" add "0 days"
      if (len(splits) != 2):
        splits =["0 days"] + splits
      days = splits[0].split(" ")[0]
      hrs, mins = splits[1].split(":")[0], splits[1].split(":")[1]
      return int(days)*24*60 + int(hrs)*60 + int(mins)

    # if task due in many days- send email 24 hr before due; if task due in 24- send email 1 hr before due, if task due in 30 mins - send email right now before due
    def setNotifications(self):
        delivery = datetime.combine(self.dueDate, self.dueTime) - timedelta(hours=24)
        return requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": f"Study App <mailgun@{MAILGUN_DOMAIN}>",
                "to": [self.email],
                "subject": f"<<Assigment>> {self.taskName}",
                "text": f"You are receiving this because a request has been made to reimnd you that an assigment ({self.taskName}) is due soon-- on {self.dueDate} at {self.dueTime}-- please check your planner to vertify!",
                "o:deliverytime": f'{delivery.strftime("%a, %d %b %Y %H:%M:%S")} -0500'
            }
        )

