from flask.views import MethodView
from http import HTTPStatus
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from .models import UserModel
from .schemas import UserSchema, UserUpdateSchema

blp = Blueprint("Users", "users", description="Operations on users.")


@blp.route("/user")
class User(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        """
        Login and obtain JWT.
        """
        user = UserModel.find_by_username(user_data["username"])
        if not user or not check_password_hash(user.password, user_data["password"]):
            abort(HTTPStatus.UNAUTHORIZED, "Invalid credentials.")
        return {"access_token": create_access_token(identity=user.id, fresh=True)}, HTTPStatus.OK

    @blp.arguments(UserUpdateSchema)
    @blp.response(HTTPStatus.OK, UserSchema)
    def put(self, user_data):
        """
        Update user password.
        """
        user = UserModel.find_by_username(user_data["username"])
        if not user or not check_password_hash(user.password, user_data["password"]):
            abort(HTTPStatus.UNAUTHORIZED, "Invalid credentials.")
        user.password = generate_password_hash(user_data["new_password"])
        try:
            user.insert_to_db()
        except SQLAlchemyError:
            abort(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                message="An error occured while updating the user.",
            )
        return user

    @blp.arguments(UserSchema)
    @blp.response(HTTPStatus.OK, UserSchema)
    def delete(self, user_data):
        """
        Delete user.
        """
        user = UserModel.find_by_username(user_data["username"])
        if not user or not check_password_hash(user.password, user_data["password"]):
            abort(HTTPStatus.UNAUTHORIZED, "Invalid credentials.")
        try:
            user.delete_from_db()
        except SQLAlchemyError:
            abort(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                message="An error occured while deleting the user.",
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
            abort(HTTPStatus.BAD_REQUEST, "A user with that username already exists")
        user = UserModel(
            username=user_data["username"],
            password=generate_password_hash(user_data["password"]),
        )
        try:
            user.insert_to_db()
        except SQLAlchemyError:
            abort(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                message="An error occured while creating the user.",
            )
        return user
