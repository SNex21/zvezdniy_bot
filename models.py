from db import Base
from sqlalchemy import Column, String, Integer
from db import engine


class User(Base): # Модель пользователя
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telid = Column(String(100), unique=True, index=True)
    username = Column(String(100), default = None)
    name = Column(String(100), default = None)
    city = Column(String(100), default = None)
    meet_pref = Column(String(100), default = None)
    age = Column(String(100), default = None)
    smen = Column(String(100), default = None)
    about_me = Column(String(100), default = None)
    

class Check(Base):# Модель уже просмотренных пользователей
    __tablename__ = "check"

    id = Column(Integer, primary_key=True, index=True)
    telid = Column(String(100), default = None)
    us_telid = Column(String(100), default = None)


Base.metadata.create_all(engine)# Обновление моделей БД
