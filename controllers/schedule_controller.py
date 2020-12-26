from repository.models import *
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from config import *


def get_current_user():
    return User.query.filter_by(email=get_jwt_identity()).first()


def get_serializable_schedule(schedule):
    # print(schedule.id)
    film_occupation = FilmOccupationTime.query.filter_by(schedule_id=schedule.id).all()
    # print(jsonify(film_occupation))
    films_list = []
    for i in range(len(film_occupation)):
        films_list.append({

                    "film_id": film_occupation[i].film_id,
                    "start_time": str(film_occupation[i].start_time),
                    "end_time": str(film_occupation[i].end_time)
                })
    result = {
        'id': schedule.id,
        'date': str(schedule.date),
        'films': films_list
    }

    return result


def get_serializable_for_film(schedule):
    # print(schedule.id)
    film_occupation = FilmOccupationTime.query.filter_by(schedule_id=schedule.id).all()
    # print(jsonify(film_occupation))
    films_list = []
    for i in range(len(film_occupation)):
        films_list.append({

                    "film_id": film_occupation[i].film_id,
                    "start_time": str(film_occupation[i].start_time),
                    "end_time": str(film_occupation[i].end_time)
                })
    result = {
        'films': films_list
    }

    return result


@app.route('/schedule', methods=['POST'])
@jwt_required
def create_schedule():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    user_creator_id = get_current_user().id
    date = request.json.get('date', None)
    films = request.json.get('films', None)
    date_check = Schedule.query.filter_by(date=date).first()
    if date_check is not None:
        return jsonify({"msg": "Schedule with such date already exists"}), 409
    if not date:
        return jsonify({"msg": "Invalid body supplied"}), 400
    db.session.add(Schedule(date=date, user_creator_id=user_creator_id))
    db.session.commit()
    for i in range(len(films)):
        db.session.add(FilmOccupationTime(film_id=films[i]["film_id"], start_time=films[i]["start_time"],
                                      end_time=films[i]["end_time"],
                                      schedule_id=Schedule.query.filter_by(date=date).first().id))
    db.session.commit()
    return jsonify({"Success": "Schedule has been added"}), 200


@app.route('/schedule', methods=['GET'])
def get_all_schedules():
    schedules = Schedule.query.all()
    schedule_list = []
    for var in schedules:
        schedule_list.append(get_serializable_schedule(var))
    print(schedule_list)
    if len(schedule_list) == 0:
        return jsonify({"msg": "No schedules found"}), 404
    else:
        return jsonify([i for i in schedule_list]), 200


@app.route('/schedule/<scheduleId>', methods=['GET'])
def get_schedule_data(scheduleId):
    try:
        int(scheduleId)
    except ValueError:
        return jsonify({"Error": "Invalid Id supplied"}), 400
    schedule = Schedule.query.filter_by(id=scheduleId).first()
    if schedule is None:
        return jsonify({"Error": "Schedule not found"}), 404
    else:
        return jsonify(get_serializable_schedule(schedule)), 200


@app.route('/schedule/<scheduleId>', methods=['PUT'])
@jwt_required
def put_schedule_data(scheduleId):
    schedule = Schedule.query.filter_by(id=scheduleId).first()
    if schedule is None:
        return jsonify({"Error": "Schedule not found"}), 404
    occupation_check = FilmOccupationTime.query.filter_by(schedule_id=schedule.id).all()
    print(len(occupation_check))
    date = request.json.get('date', schedule.date)
    films = request.json.get('films', get_serializable_for_film(schedule))
    user = User.query.filter_by(id=schedule.user_creator_id).first()
    if date == schedule.date or films == get_serializable_for_film(schedule):
        return jsonify(status='Invalid body supplied'), 400
    if user.email != get_jwt_identity():
        return jsonify({"Error": "User is not authorized"}), 403
    elif date or films:
        Schedule.query.filter_by(id=scheduleId).update(dict(date=date))
        for i in range(len(occupation_check)):
            FilmOccupationTime.query.filter_by(id=occupation_check[i].id).update(dict(film_id=films[i]["film_id"], start_time=films[i]["start_time"], end_time=films[i]["end_time"]))
        db.session.commit()
        return jsonify(status='updated schedule'), 202
