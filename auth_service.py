from database import db
from models.user import User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

bcrypt = Bcrypt()


def register_user(email, password):
    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return None, "Email already exists"

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    # Create new user
    new_user = User(
        email=email,
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return {
        "id": new_user.id,
        "email": new_user.email
    }, None


def login_user(email, password):
    # Find user by email
    user = User.query.filter_by(email=email).first()

    # Verify password
    if not user or not bcrypt.check_password_hash(user.password, password):
        return None, "Invalid email or password"

    # Generate JWT token
    access_token = create_access_token(identity=str(user.id))

    return {
        "user": {
            "id": user.id,
            "email": user.email
        },
        "token": access_token
    }, None