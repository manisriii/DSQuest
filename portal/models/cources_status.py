from . import db
from datetime import datetime
from sqlalchemy import Sequence


class CoursesStatus(db.Model):
    __bind_key__ = 'db'
    Id = db.Column(db.Integer, Sequence('courses_status_seq1', start=1), unique=True, nullable=False, primary_key=True)
    courses_status_id = db.Column(db.String(255))
    courses_id = db.Column(db.String(255))
    completed_modules = db.Column(db.Text)
    user_id = db.Column(db.String(255))
    percentage_completed = db.Column(db.String(255))
    status_of_course = db.Column(db.String(255),default="In Progress")

    created_date = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_date = db.Column(db.TIMESTAMP, default=datetime.now)
    attributes_1 = db.Column(db.String(255))
    attributes_2 = db.Column(db.String(255))
    attributes_3 = db.Column(db.String(255))
    attributes_4 = db.Column(db.String(255))
    attributes_5 = db.Column(db.String(255))
    attributes_6 = db.Column(db.String(255))
    attributes_7 = db.Column(db.String(255))
    attributes_8 = db.Column(db.String(255))
    attributes_9 = db.Column(db.String(255))
    attributes_10 = db.Column(db.String(255))
    attributes_11 = db.Column(db.String(255))
    attributes_12 = db.Column(db.String(255))
    attributes_13 = db.Column(db.String(255))
    attributes_14 = db.Column(db.String(255))
    attributes_15 = db.Column(db.String(255))
    attributes_16 = db.Column(db.String(255))
    attributes_17 = db.Column(db.String(255))
    attributes_18 = db.Column(db.String(255))
    attributes_19 = db.Column(db.String(255))
    attributes_20 = db.Column(db.String(255))
