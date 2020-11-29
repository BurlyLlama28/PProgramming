from repository.models import *
from sqlalchemy import insert, MetaData
from app import db
import os
from datetime import date, time

user = User(id="69ec8406-1e24-4f59-ad83-ac206a49cb0d", full_name="Vitalii Yarmus", email="mr.yarmus@gmail.com", phone_number="+380983057271")
schedule = Schedule(id="69ec8406-1e24-4f59-ad83-ac207a49cb0d", date = date(9999, 1, 1), occupancy_of_hall=100)
film = Film(id="69ec8406-1e24-4f59-ad83-ac208a49cb0d", duration = 124.5, name = "Cool film")
filmsSchedule = FilmsSchedule(id="69ec8406-1e24-4f59-ad83-ac209a49cb0d", film_id = "69ec8406-1e24-4f59-ad83-ac208a49cb0d", schedule_id = "69ec8406-1e24-4f59-ad83-ac207a49cb0d")
busyTime = BusyTime(id="69ec8406-1e24-4f59-ad83-ac205a49cb0d", film_id="69ec8406-1e24-4f59-ad83-ac208a49cb0d", schedule_id = "69ec8406-1e24-4f59-ad83-ac207a49cb0d", start_time = time(hour=10, minute=15, second=0), end_time =  time(hour=12, minute=15, second=0))

db.create_all()
db.session.add(user)
db.session.add(schedule)
db.session.add(film)
db.session.add(filmsSchedule)
db.session.add(busyTime)
db.session.commit()