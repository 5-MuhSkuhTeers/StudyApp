from api import db
from api.models import User, Assignment, Course
from datetime import datetime, time


def DummyData():
    db.drop_all()
    db.create_all()
    User(name='Test User', email='user@buffalo.edu', password='password').save_to_db()
    user_id = User.find_by_email('user@buffalo.edu').id
    Assignment(name='HW1', course='CSE431', due_date=datetime(2021,11,7,11,59,0),
               user_id=user_id).save_to_db()
    Course(course_num='CSE442', start_time=time(15,0,0),
           end_time=time(15,50,0), day_of_week='10101',
           user_id=user_id).save_to_db()
    Course(course_num='CSE431', start_time=time(13,50,0),
           end_time=time(14,40,0), day_of_week='10101',
           user_id=user_id).save_to_db()
    Course(course_num='CSE365', start_time=time(12,40,0),
           end_time=time(13,30,0), day_of_week='10101',
           user_id=user_id).save_to_db()
    Course(course_num='STA301', start_time=time(12,45,0),
           end_time=time(14,0,0), day_of_week='01010',
           user_id=user_id).save_to_db()

def test_course_and_assignment():
    user = User.find_by_email('user@buffalo.edu')
    assignment = user.assignments
    course = user.courses
    assert(len(assignment)==1)
    assert(len(course)==4)

def test_course():
    user = User.find_by_email('user@buffalo.edu')
    print(user.course_schedule())


if __name__ == '__main__':
    DummyData()
    test_course()
