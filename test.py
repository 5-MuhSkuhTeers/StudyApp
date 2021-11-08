import unittest
from api import db
from api.models import User, Assignment, Course
from datetime import datetime, time


class DummyData:
    def __init__(self):
        db.drop_all()
        db.create_all()
        User(name='Test User', email='user@buffalo.edu', password='password').save_to_db()
        user_id = User.find_by_email('user@buffalo.edu').id
        Assignment(name='HW1', course='CSE431', due_date=datetime(2021,11,7,11,59,0),
                   user_id=user_id).save_to_db()
        Course(course_num='CSE442', start_time=time(3,0,0),
               end_time=time(3,50,0), day_of_week='M',
               user_id=user_id).save_to_db()
        Course(course_num='CSE431', start_time=time(1,50,0),
               end_time=time(2,40,0), day_of_week='M',
               user_id=user_id).save_to_db()
        Course(course_num='CSE365', start_time=time(12,40,0),
               end_time=time(1,30,0), day_of_week='M',
               user_id=user_id).save_to_db()
        Course(course_num='STA301', start_time=time(12,45,0),
               end_time=time(2,0,0), day_of_week='T',
               user_id=user_id).save_to_db()


class DatabaseTest(unittest.TestCase):
    def test_course_and_assignment(self):
        user = User.find_by_email('user@buffalo.edu')
        assignment = user.assignments
        course = user.courses
        self.assertEqual(len(assignment),1)
        self.assertEqual(len(course),4)


if __name__ == '__main__':
    DummyData()
    unittest.main()
