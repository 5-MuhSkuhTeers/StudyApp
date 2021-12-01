import requests, os
from flask import url_for
from datetime import datetime, timedelta

MAILGUN_DOMAIN = os.environ['MAILGUN_TEST_DOMAIN'] if 'MAILGUN_TEST_DOMAIN' in os.environ \
    else 'DOMAIN'
MAILGUN_API_KEY = os.environ['MAILGUN_TEST_API'] if 'MAILGUN_TEST_API' in os.environ \
    else 'API_KEY'


def send_reset_email(user, token):
    return requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"Study App <mailgun@{MAILGUN_DOMAIN}>",
            "to": [user],
            "subject": "Password Reset Request",
            "text": f'''
			       You are receiving this because a request has been made to change your password.
			       If you did not request to change your password, please ignore this email.
			       Otherwise, follow this link to reset your password:"
				   {url_for('forgotPassword', token=token, _external=True)}
					'''
        }
    )


def setNotifications(user, taskName, dueDate, dueTime):
    delivery = datetime.combine(dueDate, dueTime) - timedelta(hours=24)
    current = datetime.now() + timedelta(seconds=30)
    if delivery < current:
        return requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": f"Study App <mailgun@{MAILGUN_DOMAIN}>",
                "to": [user],
                "subject": f"<<Assigment>> {taskName}",
                "text": f"You are receiving this because a request has been made to reimnd you that an assigment ({taskName}) is due soon-- on {dueDate} at {dueTime}-- please check your planner to vertify!"
            }
        )
    print('scheduled')
    return requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"Study App <mailgun@{MAILGUN_DOMAIN}>",
            "to": [user],
            "subject": f"<<Assigment>> {taskName}",
            "text": f"You are receiving this because a request has been made to reimnd you that an assigment ({taskName}) is due soon-- on {dueDate} at {dueTime}-- please check your planner to vertify!",
            "o:deliverytime": f'{delivery.strftime("%a, %d %b %Y %H:%M:%S")} -0500'
        }
    )

def send_break(user):
    return requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"Study App <mailgun@{MAILGUN_DOMAIN}>",
            "to": [user],
            "subject": "Time to take a break!",
            "text": "You've been working hard recently, make sure to take it easy for a little bit. Eat some food, drink some water, or go for a walk. You'll work better if you're well-rested."
        }
    )
