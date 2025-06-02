from sqlalchemy import Column, Integer, String
from database import Base

class Dress(Base):
    __tablename__ = "dresses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(String(500))
    style = Column(String(50))
    image_path = Column(String(100))
