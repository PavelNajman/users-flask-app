from marshmallow import Schema, fields
from marshmallow.validate import Length


class UserSchema(Schema):
    username = fields.Str(required=True, validate=Length(max=128))
    password = fields.Str(required=True, load_only=True, validate=Length(max=128))


class UserUpdateSchema(Schema):
    username = fields.Str(required=True, validate=Length(max=128))
    password = fields.Str(required=True, validate=Length(max=128))
    new_password = fields.Str(required=True, validate=Length(max=128))
