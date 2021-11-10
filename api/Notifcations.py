import requests, os
from flask import url_for
from api import email
from api.models import *
from api.email import *
from datetime import datetime, timedelta
import datetime 


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

    # parse dueDate to format
    def parseDate(self):
        yr,mt,dt = self.dueDate.split("-")
        date = datetime.datetime(int(yr), int(mt), int(dt))
        return #date

    # parse dueTime to format
    def parseTime(self):
      hr, min = self.dueTime.toString().split(":")
      time = datetime.time(int(hr),int(min))
      return time

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
        # this is injected text
        inject = " "
        # grab todays's date
        today = datetime.datetime.today().replace(second= 0, microsecond=0)
        # parse the date and times 
        dueDate = self.parseDate()
        dueTime = self.parseTime()
        dueDateTime = datetime.datetime.combine(dueDate, dueTime)

        #check to see if it is due within 30 mins
        if self.convertTimedeltaToMin(dueDateTime.replace(second= 0, microsecond=0) - today) < (60/2):
          inject = today.strftime("%a, %Y-%b-%d %H:%M:%S -0000")
        #check to see if it is due within the a day (24 hours) but not within 30 mins
        elif self.convertTimedeltaToMin(dueDateTime.replace(second= 0, microsecond=0) - today) < (60*24):
          inject = (dueDateTime - timedelta(hours=1)).strftime("%a, %Y-%b-%d %H:%M:%S -0000")
        #check if it is not due with in (24 hours) and in 30 mins- send email 24 hours before due 
        else:
          inject = (dueDateTime - timedelta(hours=24)).strftime("%a, %Y-%b-%d %H:%M:%S -0000")

        # this is to make the post request to the mailgun api
        postHTTP = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
        auth=("api", MAILGUN_API_KEY)
        # the api mail "o:deliverytime" must be in this format ==>> "o:deliverytime": "Fri, 25 May 2020 23:10:10 -0000"
        data = {
          "from": f"Study App <mailgun@{MAILGUN_DOMAIN}>",
          "to": [self.email],
          "subject": f"<<Assigment>> {self.taskName}",
          "text": f"You are receiving this because a request has been made to reimnd you that an assigment ({self.taskName}) is due soon-- on {self.dueDate} at {self.dueTime}-- please check your planner to vertify!",
          "o:deliverytime": f"{inject}"
        }
        return requests.post(postHTTP, auth=auth, data = data)


