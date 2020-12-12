from repository.models import *
from app import db
from datetime import date, time

user = User(id="69ec8406-1e24-4f59-ad83-ac206a49cb0d", full_name="Vitalii Yarmus", email="mr.yarmus@gmail.com", phone_number="+380983057271", password="password;")
film = Film(id="69ec8406-1e24-4f59-ad83-ac208a49cb0d", duration = 124.5, name = "Cool film")
schedule = Schedule(id="69ec8406-1e24-4f59-ad83-ac207a49cb0d", date = date(2020, 1, 1),  user_creator_id="69ec8406-1e24-4f59-ad83-ac206a49cb0d")
filmOccupationTime = FilmOccupationTime(id="69ec8406-1e24-4f59-ad83-ac205a49cb0d", film_id="69ec8406-1e24-4f59-ad83-ac208a49cb0d", schedule_id = "69ec8406-1e24-4f59-ad83-ac207a49cb0d", start_time = time(hour=10, minute=15, second=0), end_time =  time(hour=12, minute=15, second=0))

db.create_all()
db.session.add(user)
db.session.add(film)
db.session.add(schedule)
db.session.add(filmOccupationTime)
db.session.commit()
