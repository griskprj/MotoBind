from marshmallow import Schema, fields, validate, post_load
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from datetime import datetime
from app.models.motorcycle import Motorcycle

class MotorcycleCreateSchema(Schema):
    """ Схема для создания мотоцикла """
    name = fields.Str(required=True, validate=validate.Length(min=1, max=64))
    years = fields.Int(validate=validate.Range(min=1900, max=datetime.now().year))
    volume = fields.Int(validate=validate.Range(min=49, max=4000))
    mileage = fields.Int(validate=validate.Range(min=0, max=1_000_000))
    color = fields.Str(validate=validate.Regexp(r'^#[0-9a-fA-F]{3,6}$'), allow_none=True)
    license_plate = fields.Str(validate=validate.Length(max=9), allow_none=True)
    vin = fields.Str(validate=validate.Length(equal=17), allow_none=True)

class MotorcycleUpdateSchema(Schema):
    """ Схема для обновления мотоцикла """
    name = fields.Str(validate=validate.Length(min=1, max=64))
    years = fields.Int(validate=validate.Range(min=1900, max=datetime.now().year))
    volume = fields.Int(validate=validate.Range(min=49, max=4000))
    mileage = fields.Int(validate=validate.Range(min=0, max=1_000_000))
    color = fields.Str(validate=validate.Regexp(r'^#[0-9a-fA-F]{3,6}$'), allow_none=True)
    license_plate = fields.Str(validate=validate.Length(max=9), allow_none=True)
    vin = fields.Str(validate=validate.Length(equal=17), allow_none=True)

class MileageUpdateSchema(Schema):
    """ Схема для обновления только пробега """
    newMileage = fields.Int(required=True, validate=validate.Range(min=0, max=1_000_000))

class MotorcycleResponseSchema(SQLAlchemySchema):
    """ Схема для сериализации данных мотоцикла """
    class Meta:
        model = Motorcycle
        include_fk = True
        load_instance = True
    
    id = auto_field()
    owner_id = auto_field()
    name = auto_field()
    years = auto_field()
    volume = auto_field()
    mileage = auto_field()
    color = auto_field()
    license_plate = auto_field()
    vin = auto_field()
    photo_url = auto_field()
    created_at = auto_field()
    updated_at = auto_field()