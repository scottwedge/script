from datetime import datetime
from sqlalchemy import Column, String,Integer,Boolean,ForeignKey,Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import DATETIME,JSON,MEDIUMTEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

 
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(64), unique=True, index=True)
    username = Column(String(64), unique=True, index=True)
    role_id = Column(Integer, ForeignKey('roles.id'))
    password_hash = Column(String(128))
    confirmed = Column(Boolean, default=False)
    name = Column(String(64))
    location = Column(String(64))
    testjobs = relationship('TestJob', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username
    
class TestJob(Base):
    __tablename__ = 'test_jobs'
    id = Column(Integer, primary_key=True)
    
    user_id = Column(Integer, ForeignKey('users.id'))
    
    test_name =  Column(String(64))
    timestamp =  Column(String(64))
    time = Column(DATETIME(fsp=6))
    test_lab =  Column(String(64))
    variables = Column(Text)
    options = Column(Text)
    arguments = Column(Text)
    selection_md5 = Column(String(128))
    selections = Column(MEDIUMTEXT)
    selection_group = Column(MEDIUMTEXT)
    schedule = Column(String(64))

    status = Column(String(64))
    parent_id = Column(Integer)
    test_pid = Column(String(32))
    output_dir = Column(String(128))
    test_command = Column(Text)

    total_count = Column(Integer)
    pass_count = Column(Integer)
    fail_count = Column(Integer)
    running_node = Column(String(1024))
    passed_node = Column(JSON)
    failed_node = Column(JSON)



