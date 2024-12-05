from . import db
from datetime import datetime
from sqlalchemy import Sequence


class Payment(db.Model):
    __bind_key__ = 'db'
    Id = db.Column(db.Integer, Sequence('Payment', start=1), unique=True, nullable=False, primary_key=True)
    transaction_id = db.Column(db.String(255))  # primary Key
    amount = db.Column(db.String(255))
    card_number =db.Column(db.String(255))
    name_on_card = db.Column(db.String(255))
    expire_year= db.Column(db.String(255))
    expire_month = db.Column(db.String(255))
    cvv_on_card = db.Column(db.String(255))
    payment_status = db.Column(db.String(255))
    payment_method = db.Column(db.String(255), default='CARD')

    payment_date = db.Column(db.TIMESTAMP, default=datetime.now)
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
