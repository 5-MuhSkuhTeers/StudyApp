import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


url = os.environ['DATABASE_URL'] if 'DATABASE_URL' in os.environ \
        else 'postgresql://postgres:password@localhost/postgres'
if url.startswith("postgres://"):
    uri = url.replace("postgres://", "postgresql://", 1)
server = Flask(__name__)
server.secret_key = '415d9fdfcc2175c2e8bd7bdb2729befc1e788b88799c46d41d2c1ac4fb11b7ec'
server.config['SQLALCHEMY_DATABASE_URI'] = url
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)
bcrypt = Bcrypt(server)


from api import routes