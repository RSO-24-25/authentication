from src.db import Base
from src.db import engine
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# creates table if non-existnt
User.metadata.create_all(bind=engine)