from .. import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), unique=False, nullable=False)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def insert_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Blocklist(db.Model):
    __tablename__ = "blocklist"

    jti = db.Column(db.String(36), primary_key=True)
    expires = db.Column(db.DateTime, nullable=False)

    @classmethod
    def find_by_jti(cls, jti):
        return cls.query.filter_by(jti=jti).first()
    
    def insert_to_db(self):
        db.session.add(self)
        db.session.commit()
