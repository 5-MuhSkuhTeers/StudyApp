import os, secrets, bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


url = os.environ['DATABASE_URL'] if 'DATABASE_URL' in os.environ \
        else 'postgresql://postgres:password@localhost/postgres'
if url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)

secret = os.environ['SECRET_KEY'] if 'SECRET_KEY' in os.environ \
    else '309e1c538594be54f0f55c3f540e7c4b'

server = Flask(__name__)
server.secret_key = secret
server.config['SQLALCHEMY_DATABASE_URI'] = url
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)
bcrypt = Bcrypt(server)


from api import routes