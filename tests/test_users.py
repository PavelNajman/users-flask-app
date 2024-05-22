import pytest
from http import HTTPStatus
from flask_jwt_extended import decode_token
from app import db, create_app


@pytest.fixture()
def app():
    app = create_app("testing")
    app.config.update({"TESTING": True})

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def register_user(client):
    return client.post(
        "/user/register", json={"username": "test_user", "password": "password"}
    )


def login_user(client, password="password"):
    return client.post("/user", json={"username": "test_user", "password": password})


def delete_user(client, password="password"):
    return client.delete("/user", json={"username": "test_user", "password": password})


def update_user(client, password="password"):
    return client.put(
        "/user",
        json={
            "username": "test_user",
            "password": password,
            "new_password": "new_password",
        },
    )


def check_response(response, expected_status_code):
    assert response.status_code == expected_status_code
    assert response.json["username"] == "test_user"


def test_register_new_user(client):
    """
    A user can be registered with a post request that contains username and password.
    A response contains the sent username.
    """
    response = register_user(client)
    check_response(response, HTTPStatus.CREATED)


def test_register_existing_user(client):
    """
    A new user cannot be registered with a username of already existing user.
    Such a request would yield a 400 error.
    """
    response = register_user(client)
    check_response(response, HTTPStatus.CREATED)
    response = register_user(client)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_invalid_register_user(client):
    """
    A register user request with invalid data yields 422 error.
    """
    response = client.post("/user/register", json={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_login_non_existing_user(client):
    """
    A login request for non-registered user yields 401 error.
    """
    response = login_user(client)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_login_existing_user_with_wrong_password(client):
    """
    A login request for registered user using a wrong password yields 401 error.
    """
    response = register_user(client)
    check_response(response, HTTPStatus.CREATED)
    response = login_user(client, "wrong_password")
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_login_existing_user(client):
    """
    A successful login should yield a valid JWT token and 200 response code.
    """
    response = register_user(client)
    check_response(response, HTTPStatus.CREATED)
    response = login_user(client)
    assert response.status_code == HTTPStatus.OK
    with client.application.app_context():
        decoded_token = decode_token(response.json["access_token"])
        assert decoded_token["sub"] == "test_user"


def test_invalid_login_user(client):
    """
    A login user request with invalid data yields 422 error.
    """
    response = client.post("/user", json={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_delete_non_existing_user(client):
    """
    A delete request for non-registered user yields 401 error.
    """
    response = delete_user(client)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_delete_existing_user_with_wrong_password(client):
    """
    A delete request for registered user using a wrong password yields 401 error.
    """
    response = register_user(client)
    check_response(response, HTTPStatus.CREATED)
    response = delete_user(client, "wrong_password")
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_delete_user(client):
    """
    A successful delete user request should yield the 200 response code and remove user from database.
    """
    response = register_user(client)
    check_response(response, HTTPStatus.CREATED)
    response = delete_user(client)
    check_response(response, HTTPStatus.OK)
    response = login_user(client)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_invalid_delete_user(client):
    """
    A delete user request with invalid data yields 422 error.
    """
    response = client.delete("/user", json={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_non_existing_user(client):
    """
    An update request for non-registered user yields 401 error.
    """
    response = update_user(client)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_update_existing_user_with_wrong_password(client):
    """
    An update request for registered user using a wrong password yields 401 error.
    """
    response = register_user(client)
    check_response(response, HTTPStatus.CREATED)
    response = update_user(client, "wrong_password")
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_update_user(client):
    """
    A successful update user request should yield the 200 response code and change user's password.
    """
    response = register_user(client)
    check_response(response, HTTPStatus.CREATED)
    response = update_user(client)
    check_response(response, HTTPStatus.OK)
    response = login_user(client)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    response = login_user(client, "new_password")
    assert response.status_code == HTTPStatus.OK
    with client.application.app_context():
        decoded_token = decode_token(response.json["access_token"])
        assert decoded_token["sub"] == "test_user"


def test_invalid_update_user(client):
    """
    An update user request with invalid data yields 422 error.
    """
    response = client.put("/user", json={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
