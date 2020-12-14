from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config import Base, db
from werkzeug.security import generate_password_hash

# Base = declarative_base()

class User(Base):

    id = Column(db.INTEGER, primary_key=True, nullable=False)
    full_name = Column(String(1000), nullable=False)
    birthday = Column(Date, nullable=True)
    email = Column(String(345), nullable=False)
    phone_number = Column(String(15), nullable=False)
    password = Column(String(5000), nullable=False)

    def __init__(self, full_name, birthday, email, phone_number, password):
        self.full_name = full_name
        self.birthday = birthday
        self.email = email
        self.phone_number = phone_number
        self.password = generate_password_hash(password)


class Film(Base):

    id = Column(db.INTEGER, primary_key=True, nullable=False)
    duration = Column(Float, nullable=False)
    name = Column(String(1000), nullable=False)


class Schedule(Base):

    id = Column(db.INTEGER, primary_key=True, nullable=False)
    date = Column(Date, nullable=False)
    user_creator_id = Column(db.INTEGER, ForeignKey(User.id))
    user_creator = relationship(User)
    films_occupation_times = relationship('FilmOccupationTime')


class FilmOccupationTime(Base):

    id = Column(db.INTEGER, primary_key=True, nullable=False)
    film_id = Column(db.INTEGER, ForeignKey(Film.id))
    film = relationship(Film)
    schedule_id = Column(db.INTEGER, ForeignKey(Schedule.id))
    schedule = relationship(Schedule)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)


db.create_all()