from .. import LOG
from ..models.cources import Courses


class ADDCOURCES:
    def __init__(self, db):
        self.db = db

    def run(self):
        self.create_cources()
        try:
            self.db.session.commit()
        except Exception as e:
            LOG.error(e)

    def create_cources(self):
        user1 = Courses(Id=1,
                        courses_id="2210202200040505444",
                        cource_name='SQL Server',
                        description="Microsoft SQL Server is a robust database system for managing, analyzing, "
                                    "and storing data. It’s ideal for building scalable applications with strong "
                                    "security and performance.",
                        course_image_="/static/img/2.jpg",
                        course_status="active",
                        amount='100',
                        page_to_load='course_sql')
        self.db.session.merge(user1)
        user1 = Courses(Id=2,
                        courses_id="2210202200040505445",
                        cource_name='Python',
                        description="Python is a versatile programming language known for its simplicity and "
                                    "readability. It's widely used in data science, web development, and automation.",
                        course_image_="/static/img/3.jpg",
                        course_status="active",
                        amount='100',
                        page_to_load='course_python')
        self.db.session.merge(user1)
        user1 = Courses(Id=3,
                        courses_id="2210202200040505448",
                        cource_name='Pandas',
                        description="Learn Pandas in this concise course! Master data manipulation, analysis, "
                                    "and visualization with Python. Perfect for beginners and professionals seeking "
                                    "to boost data science and analysis expertise efficiently.",
                        course_image_="/static/images/pandas.png",
                        course_status="active",
                        amount='100',
                        page_to_load='course_pandas')
        self.db.session.merge(user1)
