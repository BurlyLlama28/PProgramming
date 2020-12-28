from repository.models import *
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from config import *
from datetime import *


def get_serializable_user(user):
    result = {
        'id': user.id,
        'full_name': user.full_name,
        'birthday': user.birthday,
        'email': user.email,
        'phone_number': user.phone_number,
    }

    return result


@app.route('/user', methods=['POST'])
def create_user():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    full_name = request.json.get('full_name', None)
    birthday = request.json.get('birthday', None)
    email = request.json.get('email', None)
    phone_number = request.json.get('phone_number', None)
    password = request.json.get('password', None)
    if not full_name:
        return jsonify({
            "errors": [{
                "status": "400",
                "source": {"pointer": None},
                "title": "Invalid body supplied",
                "detail": "Missing full_name parameter"
            }]}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    if phone_number == '' or password == '' or birthday == '':
        return jsonify({"msg": "Invalid body supplied"}), 400
    email_check = User.query.filter_by(email=email).first()
    if email_check is not None:
        return jsonify({"msg": "User with such email already exists"}), 409
    db.session.add(User(full_name=full_name, birthday=datetime.strptime(birthday, '%Y-%m-%d').date(), email=email, phone_number=phone_number, password=password))
    db.session.commit()
    return jsonify({"Success": "User has been created"}), 201


@app.route('/user/login', methods=['GET'])
def login_user():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    current_user = User.query.filter_by(email=email).first()
    if check_password_hash(current_user.password, password):
        return jsonify(access_token=create_access_token(identity=email)), 200
    else:
        return jsonify({"Error": "Wrong password"}), 401


@app.route('/user/<userId>', methods=['GET'])
@jwt_required
def get_user_data(userId):
    try:
        int(userId)
    except ValueError:
        return jsonify({"Error": "Invalid Id supplied"}), 400
    user = User.query.filter_by(id=userId).first()
    if user is None:
        return jsonify({"Error": "User not found"}), 404
    if user.email != get_jwt_identity():
        return jsonify({"Error": "User is not authorized"}), 403
    else:
        return jsonify(get_serializable_user(user)), 200


@app.route('/user/<userId>', methods=['PUT'])
@jwt_required
def put_user_data(userId):
    user = User.query.filter_by(id=userId).first()
    if user is None:
        return jsonify({"Error": "User not found"}), 404
    full_name = request.json.get('full_name', user.full_name)
    birthday = request.json.get('birthday', user.birthday)
    email = request.json.get('email', user.email)
    phone_number = request.json.get('phone_number', user.phone_number)
    password = request.json.get('password', user.password)
    if full_name == user.full_name and password == user.password and email == user.email and phone_number == user.phone_number and birthday == user.birthday:
        return jsonify(status='Invalid body supplied'), 404
    if user.email != get_jwt_identity():
        return jsonify({"Error": "User is not authorized"}), 403
    elif password or phone_number or email or birthday or full_name:
        if password:
            hashed = generate_password_hash(password)
        else:
            hashed = password
        User.query.filter_by(id=userId).update(dict(full_name=full_name, birthday=datetime.strptime(birthday, '%Y-%m-%d').date(), email=email, phone_number=phone_number, password=hashed))
        db.session.commit()
        return jsonify(status='updated user'), 202
