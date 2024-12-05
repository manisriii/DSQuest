from .. import LOG
from ..models.users import User


class AddINSTUSER:
    def __init__(self, db):
        self.db = db

    def run(self):
        self.create_users()
        try:
            self.db.session.commit()
        except Exception as e:
            LOG.error(e)

    def create_users(self):
        user1 = User(Id=1,
                     user_id="2210202200040505442",
                     password="K2Lr1gbcy154tVtwbgko1w==",
                     username="admin",
                     email_id="skr@gmail.com",
                     active='y',
                     status='completed',
                     attributes_1='admin',
                     role='admin',
                     mfa_enabled=False,
                     mfa_secret=None)
        self.db.session.merge(user1)
