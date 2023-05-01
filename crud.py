# Файл связи БД с кодом
from models import User, Check
from db import engine
from sqlalchemy.orm import sessionmaker
from random import randint


session = sessionmaker(bind = engine)


def create_user(s: session(), user: dict): # Функция создания юзера
    user = User(telid = user['telid'], username = user['username'],  name = user['name'], city = user['city'], meet_pref = user['meet_pref'], age = user['age'], smen = user['smen'], about_me = user['about_me'])
    s.add(user)
    s.commit()


def get_all(s: session()):# Функция получения всех юзеров
    users = []
    user = {}
    for row in s.query(User).all():
        user['telid'] = row.telid
        user['username'] = row.username
        user['name'] = row.name
        user['city'] = row.city
        user['age'] = row.age
        user['smen'] = row.smen
        user['about_me'] = row.about_me
        users.insert(len(users), user)
        user = {}
    return users


def check_user(s: session(), telid:str): # Функция проверки пользователя на зарегестрированность
    zn = s.query(User).filter(User.telid == telid).group_by(User).first()
    return zn


def get_random_user(users: dict): # Функция получения рандомного пользователя
    return users[randint(0, len(users) - 1)]


def check_use(s: session(), us_telid: str, telid: str): # Функция проверка на просмотренность
    used = s.query(Check).filter(Check.us_telid == us_telid).all()

    for row in used:
        print(row.telid)
        if row.telid == telid or us_telid == telid:
            return True
    if us_telid != telid:
        return False
    else:
        return True


def create_used(s: session(), used: str, us_telid: str): # Функция добавление просмотренного пользователя
    used = Check(telid = used, us_telid = us_telid)
    s.add(used)
    s.commit()


def get_used_us(s: session(), us_telid: str): # Функция получения всех просмотренных пользователей у юзера
    zn = s.query(Check).filter(Check.us_telid == us_telid).group_by(Check).all()
    k = 0
    for row in zn:
        k += 1
    return k

