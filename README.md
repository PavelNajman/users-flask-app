# Users

Users is a Flask application that enables users to register, login and receive JWT tokens using a simple API. The user data is stored in a database and consists of a username and a password.

## Development and testing

The development and testing can be done from within the virtual environment with installed requirements.

### Create and activate virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
```

### Install requirements

```sh
pip3 install -r requirements.txt
```

### Run tests

```sh
python3 -m pytest
```

### Run flask development server

```sh
flask --app 'app:create_app("development")' run
```

## Production deployment

Production deployment can utilize the provided Dockerfile that runs the Users app using the gunicorn WSGI server. Before running, the `SECRET_KEY` and `DATABASE_URI` environmental variables should be defined e.g. in a `.env` file.

### Build docker image

```sh
docker build -t users-image .
```

### Run image

```sh
docker run --env-file=.env -d -p 8000:8000 users-image
```

## API Documentation

The API provides the following endpoints for user management:

| Method | Endpoint        | Description                           |
|--------|----------------|---------------------------------------|
| POST   | /user/register | Register a new user                   |
| POST   | /user          | Login and obtain JWT access token     |
| PUT    | /user          | Update user's password                |
| DELETE | /user          | Delete user account                   |

### Endpoints

#### Register a new user

```http
POST /user/register
```

**Request Body:**

```json
{
    "username": "string",
    "password": "string"
}
```

**Response:** `201 Created`

```json
{
    "id": "integer",
    "username": "string"
}
```

**Curl Example:**

```bash
curl -X POST http://localhost:8000/user/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'
```

#### Login

```http
POST /user
```

**Request Body:**

```json
{
    "username": "string",
    "password": "string"
}
```

**Response:** `200 OK`

```json
{
    "access_token": "string"
}
```

**Curl Example:**

```bash
curl -X POST http://localhost:8000/user \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'
```

#### Update Password

```http
PUT /user
```

**Request Body:**

```json
{
    "username": "string",
    "password": "string",
    "new_password": "string"
}
```

**Response:** `200 OK`

```json
{
    "id": "integer",
    "username": "string"
}
```

**Curl Example:**

```bash
curl -X PUT http://localhost:8000/user \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass", "new_password": "newpass"}'
```

#### Delete User

```http
DELETE /user
```

**Request Body:**

```json
{
    "username": "string",
    "password": "string"
}
```

**Response:** `200 OK`

```json
{
    "id": "integer",
    "username": "string"
}
```

**Curl Example:**

```bash
curl -X DELETE http://localhost:8000/user \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'
```
