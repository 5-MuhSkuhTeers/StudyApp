import requests, os
from flask import url_for

MAILGUN_DOMAIN = os.environ['MAILGUN_TEST_DOMAIN']
MAILGUN_API_KEY = os.environ['MAILGUN_TEST_API']


def send_reset_email(user, token):
    requests.post(
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
    return
