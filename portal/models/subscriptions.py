from . import db
from datetime import datetime
from sqlalchemy import Sequence


class Subscription(db.Model):
    __bind_key__ = 'db'
    Id = db.Column(db.Integer, Sequence('user_seq', start=1), unique=True, nullable=False, primary_key=True)
    transaction_id = db.Column(db.String(255))  # fore-ng key
    user_id = db.Column(db.String(255))
    subscription_type = db.Column(db.String(255))
    subscription_status = db.Column(db.String(255))
    subscription_start_date = db.Column(db.TIMESTAMP, default=datetime.now)
    subscription_end_date = db.Column(db.TIMESTAMP, default=datetime.now)

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
