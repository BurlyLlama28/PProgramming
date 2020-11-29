from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Time
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(
        String(36),
        primary_key=True,
        nullable=False
    )
    full_name = Column(
        String(1000),
        nullable=False
    )
    birthday = Column(
        Date,
        nullable=True
    )
    email = Column(
        String(345),
        nullable=False
    )
    phone_number = Column(
        String(15),
        nullable=False
    )

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(
        String(36),
        primary_key=True,
        nullable=False
    )
    date = Column(
        Date,
        nullable=False
    )
    occupancy_of_hall = Column(
        Integer,
        nullable=False
    )

class Film(Base):
    __tablename__ = "films"

    id = Column(
        String(36),
        primary_key=True,
        nullable=False
    )
    duration = Column(
        Float(asdecimal=True),
        nullable=False
    )
    name = Column(
        String(1000),
        nullable=False
    )

class FilmsSchedule(Base):
    __tablename__ = "filmsSchedules"

    id = Column(
        String(36),
        primary_key=True,
        nullable=False
    )
    film_id = Column(
        String(36),
        ForeignKey(Film.id),
        nullable=False
    )
    schedule_id = Column(
        String(36),
        ForeignKey(Schedule.id),
        nullable=False
    )

class BusyTime(Base):
    __tablename__ = "busy_times"

    id = Column(
        String(36),
        primary_key=True,
        nullable=False
    )
    film_id = Column(
        String(36),
        ForeignKey(Film.id),
        nullable=False
    )
    schedule_id = Column(
        String(36),
        ForeignKey(Schedule.id),
        nullable=False
    )
    start_time = Column(
        Time,
        nullable=False,
    )
    end_time = Column(
        Time,
        nullable=False
    )