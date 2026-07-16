from marshmallow import Schema, fields, validate, post_load
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from app.models.user import User

class UserRegisterSchema(Schema):
    """ Схема для регистрации """
    email = fields.Email(required=True, error_messages={"required": "Email обязателен"})
    password = fields.Str(required=True, validate=validate.Length(min=6), error_messages={"required": "Пароль обязателен"})
    username = fields.Str(required=True, validate=validate.Length(min=3, max=64), error_messages={"required": "Имя пользователя обязательно"})
    role = fields.Str(required=True, validate=validate.OneOf(['motorcyclist', 'motoclub']), error_messages={"required": "Роль обязательна"})

class UserLoginSchema(Schema):
    """ Схема для логина """
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class RefreshTokenSchema(Schema):
    """ Схема для обновления токена """
    refresh_token = fields.Str(required=True)


class UserResponseSchema(SQLAlchemySchema):
    """ Схема для сериализации пользователя """
    class Meta:
        model = User
        include_fk = True
        load_instance = True

    id = auto_field()
    email = auto_field()
    username = auto_field()
    role = auto_field()
    status = auto_field()
    created_at = auto_field()