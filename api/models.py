from api import db
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as serializer


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    name = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(80), nullable=False, default='Hello There!')
    assignments = db.relationship('Assignment', lazy=True)
    courses = db.relationship('Course', lazy=True)

    def __repr__(self):
        return f"User('{self.id}','{self.name}')"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def reset_token(self, expire=1800):
        token = serializer(current_app.secret_key, expire)
        return token.dumps({'email':self.email}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = serializer(current_app.secret_key)
        try:
            email = s.loads(token)['email']
        except:
            return None
        return User.find_by_email(email)


class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    due_date = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Assignment('{self.user_id}','{self.due_date}')"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_num = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Course('{self.user_id}','{self.course_num}')"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
