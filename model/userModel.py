from sqlalchemy import Boolean,Column,Integer,String
from database.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password= Column(String)
    is_Admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    