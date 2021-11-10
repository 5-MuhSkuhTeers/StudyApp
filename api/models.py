from api import db
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
from datetime import datetime, timedelta, tzinfo


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
        return token.dumps({'email' :self.email}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = serializer(current_app.secret_key)
        try:
            email = s.loads(token)['email']
        except:
            return None
        return User.find_by_email(email)

    def course_schedule(self):
        courses = []
        for i in self.courses:
            courses.append([i.course_num,i.day_of_week,i.start_time])
        courses.sort(key=lambda x: x[2])
        schedule = [[],[],[],[],[]]
        for i in courses:
            if i[1][0] == '1':
                schedule[0].append(i[0])
            if i[1][1] == '1':
                schedule[1].append(i[0])
            if i[1][2] == '1':
                schedule[2].append(i[0])
            if i[1][3] == '1':
                schedule[3].append(i[0])
            if i[1][4] == '1':
                schedule[4].append(i[0])
        max_day = max([len(i) for i in schedule])
        matrix = [[[] for m1 in range(5)] for m2 in range(max_day)]
        for i in range(5):
            for j in range(max_day):
                try:
                    matrix[j][i] = schedule[i][j]
                except:
                    matrix[j][i] = ""
        return matrix

    def user_assignments(self):
        work = []
        for i in self.assignments:
            work.append([i.name,i.due_date])
        return work


class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"Assignment('{self.user_id}','{self.due_date}','{self.name})"

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
    day_of_week = db.Column(db.String(5), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f"Course('{self.user_id}','{self.course_num}','{self.start_time}')"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()