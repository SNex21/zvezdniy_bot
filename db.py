from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine


SQLALCHEMY_DATABASE_URL = 'mariadb+pymysql://root:Snex2022@127.0.0.1:3306/zvezd' # URL db


engine = create_engine(SQLALCHEMY_DATABASE_URL)


Base = declarative_base()