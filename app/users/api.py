from datetime import datetime
from flask.views import MethodView
from http import HTTPStatus
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt, jwt_required

from .models import UserModel, Blocklist
from .schemas import UserSchema, UserUpdateSchema

blp = Blueprint("Users", "users", description="Operations on users.")

def authenticate_user(username, password):
    """Helper method to authenticate a user."""
    user = UserModel.find_by_username(username)
    if not user or not check_password_hash(user.password, password):
        abort(HTTPStatus.UNAUTHORIZED, message="Invalid credentials.")
    return user


@blp.route("/user")
class User(MethodView):
    @blp.arguments(UserUpdateSchema)
    @blp.response(HTTPStatus.OK, UserSchema)
    def put(self, user_data):
        """
        Update user password.
        """
        user = authenticate_user(user_data["username"], user_data["password"])
        user.password = generate_password_hash(user_data["new_password"])
        try:
            user.insert_to_db()
        except SQLAlchemyError:
            abort(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                message="An error occurred while updating the user.",
            )
        return user

    @blp.arguments(UserSchema)
    @blp.response(HTTPStatus.OK, UserSchema)
    def delete(self, user_data):
        """
        Delete user.
        """
        user = authenticate_user(user_data["username"], user_data["password"])
        try:
            user.delete_from_db()
        except SQLAlchemyError:
            abort(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                message="An error occurred while deleting the user.",
            )
        return user


@blp.route("/user/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(HTTPStatus.CREATED, UserSchema)
    def post(self, user_data):
        """
        Register new user.
        """
        if UserModel.find_by_username(user_data["username"]):
            abort(HTTPStatus.BAD_REQUEST, message="A user with that username already exists")
        user = UserModel(
            username=user_data["username"],
            password=generate_password_hash(user_data["password"]),
        )
        try:
            user.insert_to_db()
        except SQLAlchemyError:
            abort(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                message="An error occurred while creating the user.",
            )
        return user


@blp.route("/user/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        """
        Login and obtain JWT.
        """
        user = authenticate_user(user_data["username"], user_data["password"])
        return {"access_token": create_access_token(identity=str(user.id), fresh=True)}, HTTPStatus.OK


@blp.route("/user/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        """
        Logout user by adding JWT token to blocklist.
        """
        jwt = get_jwt()
        jti = jwt["jti"]
        expires = datetime.fromtimestamp(jwt["exp"])
        
        blocklist = Blocklist(jti=jti, expires=expires)
        try:
            blocklist.insert_to_db()
        except SQLAlchemyError:
            abort(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                message="An error occurred while logging out.",
            )
        return {"message": "Successfully logged out"}, HTTPStatus.OK
