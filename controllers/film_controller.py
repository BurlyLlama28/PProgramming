from repository.models import *
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from config import *


def get_serializable_film(film):
    result = {
        'id': film.id,
        'duration': film.duration,
        'name': film.name,
    }

    return result


@app.route('/film', methods=['POST'])
@jwt_required
def create_film():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    duration = request.json.get('duration', None)
    name = request.json.get('name', None)
    film_check = Film.query.filter_by(name=name).first()
    if film_check is not None:
        return jsonify({"msg": "Film with such name already exists"}), 409
    if not duration or not name:
        return jsonify({"msg": "Invalid body supplied"}), 400
    db.session.add(Film(duration=duration, name=name))
    db.session.commit()
    return jsonify({"Success": "Film has been added"}), 201


@app.route('/film', methods=['GET'])
def get_all_films():
    films = Film.query.all()
    films_list = []
    for var in films:
        films_list.append(get_serializable_film(var))
    print(films_list)
    if len(films_list) == 0:
        return jsonify({"msg": "No films found"}), 404
    else:
        return jsonify([i for i in films_list]), 200


@app.route('/film/<filmId>', methods=['GET'])
def get_film_data(filmId):
    try:
        int(filmId)
    except ValueError:
        return jsonify({"Error": "Invalid Id supplied"}), 400
    film = Film.query.filter_by(id=filmId).first()
    if film is None:
        return jsonify({"Error": "Film not found"}), 404
    else:
        return jsonify(get_serializable_film(film)), 200


@app.route('/film/<filmId>', methods=['PUT'])
@jwt_required
def put_film_data(filmId):
    film = Film.query.filter_by(id=filmId).first()
    user = User.query.filter_by(id=film.userId).first()
    if film is None:
        return jsonify({"Error": "Film not found"}), 404
    duration = request.json.get('duration', film.duration)
    name = request.json.get('name', film.name)
    if duration == film.duration and name == film.name:
        return jsonify(status='Invalid body supplied'), 400
    if user.email != get_jwt_identity():
        return jsonify({"Error": "User is not authorized"}), 401
    elif duration or name:
        Film.query.filter_by(id=filmId).update(dict(duration=duration, name=name))
        db.session.commit()
        return jsonify(status='updated film'), 202


@app.route('/film/<filmId>', methods=['DELETE'])
@jwt_required
def delete_film_data(filmId):
    film = Film.query.filter_by(id=filmId).first()
    if film is None:
        return jsonify({"Error": "Film not found"}), 404
    db.session.delete(film)
    db.session.commit()
    return jsonify(status='deleted film'), 200