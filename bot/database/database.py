from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from bot.database.models import Base

engine = create_engine("sqlite:///bot.db", echo=True)

session = Session(engine)

def init_database():
    Base.metadata.create_all(engine)