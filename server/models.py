import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    actions = relationship("Action", back_populates="user")

    def __repr__(self):
        return f"<User(id='{self.id}', username='{self.username}', email='{self.email}')>"

class Action(Base):
    __tablename__ = 'actions'
    
    id = Column(Integer, primary_key=True)
    action_name = Column(String, nullable=False)
    action_details = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="actions")
    schedule = relationship("Schedule", back_populates="action", uselist=False)

    def __repr__(self):
        return f"<Action(id='{self.id}', action_name='{self.action_name}', action_details='{self.action_details}')>"

class Schedule(Base):
    __tablename__ = 'schedules'
    
    id = Column(Integer, primary_key=True)
    scheduled_time = Column(DateTime, nullable=False)
    action_id = Column(Integer, ForeignKey('actions.id'))
    action = relationship("Action", back_populates="schedule")

    def __repr__(self):
        return f"<Schedule(id='{self.id}', scheduled_time='{self.scheduled_time}')>"

def create_tables():
    Base.metadata.create_all(engine)

def drop_tables():
    Base.metadata.drop_all(engine)

if __name__ == "__main__":
    create_tables()