from sqlalchemy import Column, Integer, String
from config.db_connect import DB

class PersonModel(DB.Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    address = Column(String)
    work = Column(String)
