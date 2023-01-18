from flask import Blueprint, request, jsonify
from neo4j_db import check_password, create_user, get_db, get_user_by_email, get_user_by_id
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, decode_token

auth_route = Blueprint("auth", __name__)

@auth_route.route("/auth/login", methods=["POST"])
def login():
    req = request.get_json()
    email = str(req["email"])
    password_candidate = str(req["password"])

    if not email:
        return {"email": "This field is required."}, 400

    if not password_candidate:
        return {"password": "This field is required."}, 400

    db = get_db()

    result = db.read_transaction(get_user_by_email, email)

    if not result:
        return jsonify({"message":"The email you entered isn't connected to an account."}), 422
    existing_user = result["user"]

    if check_password(existing_user, password_candidate):
        access_token = create_access_token(identity=existing_user["id"])
        resp = jsonify({'message': 'Uspešno prijavljivanje', 'access_token' : access_token})
        return resp, 200
    else:
        return jsonify({"message":"Wrong data"}), 422


@auth_route.route("/auth/register", methods=["GET", "POST"])
def register():
    req = request.get_json()

    name = str(req["name"])
    lastname = str(req["lastname"])
    email = str(req["email"])
    password = str(req["password"])

    # Check if fields are empty

    if not name:
        return {"name": "This field is required."}, 400

    if not lastname:
        return {"lastname": "This field is required."}, 400

    if not email:
        return {"email": "This field is required."}, 400

    if not password:
        return {"password": "This field is required."}, 400

    # Check if email already exists

    db = get_db()

    result = db.read_transaction(get_user_by_email, email)
    if result:
        return jsonify({"message": "Email is already in use."}), 422

    # Create user

    results = db.write_transaction(create_user, name, lastname, email, password)
    user = results["user"]
    return serialize_user(user), 201

@auth_route.route('/auth/current-user', methods=['GET'])
@jwt_required()
def current_user():
    user_id = get_jwt_identity()
    db = get_db()
    results = db.read_transaction(get_user_by_id, user_id)
    user = results["user"]
    return jsonify(serialize_user(user)), 200

def serialize_user(user):
    return {
        "id": user["id"],
        "name": user["name"],
        "lastname": user["lastname"],
        "email": user["email"]
    }