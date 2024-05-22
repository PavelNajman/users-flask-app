# Users

Users is a Flask application that enables users to register, login and receive JWT tokenis using a simple API. The user data is stored in a database and consists of a username and a password.

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

