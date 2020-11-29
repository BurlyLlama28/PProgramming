from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from models import Base
import os

URL = os.getenv("URL")

if not database_exists(URL):
    create_database(URL)

engine = create_engine(URL, echo=True)

Base.metadata.create_all(engine)