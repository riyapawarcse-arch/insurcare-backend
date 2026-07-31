from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from services.auth_service import bcrypt
from models.user import User
from database import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Missing request body"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"message": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(
        email=email,
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    print("Incoming data:", data)

    if not data:
        return jsonify({"message": "Missing request body"}), 400

    email = data.get("email")
    password = data.get("password")

    print("Email:", email)

    user = User.query.filter_by(email=email).first()

    print("User found:", user)

    if user:
        print("Stored password hash:", user.password)
        print("Password match:", bcrypt.check_password_hash(user.password, password))

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=str(user.id))

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "user": {
                "id": user.id,
                "email": user.email
            }
        }), 200

    return jsonify({"message": "Invalid email or password"}), 401


@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Missing request body"}), 400

    email = data.get("email")
    new_password = data.get("new_password")

    if not email or not new_password:
        return jsonify({"message": "Email and new password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "User with this email does not exist"}), 404

    user.password = bcrypt.generate_password_hash(new_password).decode("utf-8")
    db.session.commit()

    return jsonify({"message": "Password reset successfully. You can now sign in."}), 200



