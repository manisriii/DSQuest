import os
from ..models import db
from .add_problems import AddProblems
from .add_users import AddINSTUSER
from .add_cources import ADDCOURCES
from .. import is_development


def init_seeds(app):
    if is_development():
        with app.app_context():
            AddProblems(db).run()
            AddINSTUSER(db).run()
            ADDCOURCES(db).run()
            for folder in app.config["DIRECTORIES"]:
                if not os.path.exists(folder):
                    os.mkdir(folder)
    app.logger.info("Initialized Seeds")
