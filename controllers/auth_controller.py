from flask import request, jsonify
from services.auth_service import register_user, login_user

def register():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'agent')

    if not username or not email or not password:
        return jsonify({"success": False, "message": "Username, email, and password are required"}), 400

    user, error = register_user(username, email, password, role)

    if error:
        return jsonify({"success": False, "message": error}), 400

    return jsonify({"success": True, "data": user, "message": "User registered successfully"}), 201


def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password are required"}), 400

    result, error = login_user(username, password)

    if error:
        return jsonify({"success": False, "message": error}), 401

    return jsonify({"success": True, "data": result, "message": "Login successful"}), 200
