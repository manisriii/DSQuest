from datetime import datetime
from . import db
from datetime import datetime
from sqlalchemy import Sequence

from . import db


class Problem(db.Model):
    __bind_key__ = 'db'

    Id = db.Column(db.Integer, Sequence('Problem_seq', start=1), unique=True, nullable=False, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(50))
    example_input =db.Column(db.Text)
    example_output =db.Column(db.Text)
    explanation=db.Column(db.Text)
    type = db.Column(db.Text)
    schema = db.Column(db.Text)
    expected_output = db.Column(db.Text, nullable=True)
    test_cases = db.Column(db.Text, nullable=True)
    function_signature =db.Column(db.Text)
    created_date = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_date = db.Column(db.TIMESTAMP, default=datetime.now)
    solution_ = db.Column(db.Text)
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
