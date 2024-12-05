from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(
)


def init_app(app):
    db_connection_string = ''
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_BINDS'] = {
        'db': "sqlite:///dsquest.sqlite"
    }
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dsquest.sqlite'
    db.init_app(app)
    app.logger.info('Initialized models')
    with app.app_context():
        from .users import User
        from .problems import Problem
        from .subscriptions import Subscription
        from .user_solutions import UserSolution
        from .cources_status import CoursesStatus
        from .cources import Courses
        from .payment import Payment
        db.create_all()
        db.session.commit()
        app.logger.debug('All tables are created')