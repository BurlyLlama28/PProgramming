from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from models import Base
import os

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

DB = "cinema_db"
URL = "mysql+pymysql://{0}:{1}@{2}:{3}/".format(USER, PASSWORD, HOST, PORT)

print(URL)

if not database_exists(URL+DB):
    create_database(URL+DB)

engine = create_engine(URL+DB, echo=True)

Base.metadata.create_all(engine)