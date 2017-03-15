from models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql://root:fortinet@localhost:3306/Lab_Dev')
DBSession = sessionmaker(bind=engine)
session = DBSession()
user = session.query(User).all()
test_objs = session.query(TestJob).all()
print user
session.close()