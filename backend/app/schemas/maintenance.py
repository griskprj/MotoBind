from marshmallow import Schema, fields, validate, post_load
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from app.models.maintenance import Maintenance, PlannedMaintenance

class MaintenanceCreateSchema(Schema):
    """ Схема для создания выполненного обслуживания """
    moto_id = fields.Int(required=True)
    category = fields.Str(required=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=64))
    description = fields.Str(validate=validate.Length(max=2048), allow_none=True)
    mileage = fields.Int(validate=validate.Range(min=0, max=1_000_000), allow_none=True)
    cost = fields.Int(validate=validate.Range(min=0), allow_none=True)
    date = fields.Date(format="%Y-%m-%d", allow_none=True)

class PlannedMaintenanceCreateSchema(Schema):
    """ Схема для создания планового обслуживания """
    moto_id = fields.Int(required=True)
    category = fields.Str(required=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=64))
    description = fields.Str(validate=validate.Length(max=2048), allow_none=True)
    planned_mileage = fields.Int(validate=validate.Range(min=0, max=1_000_000), allow_none=True)

class PlannedMaintenanceUpdateSchema(Schema):
    """ Схема для обновления планового обслуживания """
    maintenanceId = fields.Int(required=True)
    motorcycleId = fields.Int(required=True)
    title = fields.Str(validate=validate.Length(min=1, max=64), allow_none=True)
    description = fields.Str(allow_none=True)
    category = fields.Str(allow_none=True)
    mileage = fields.Int(validate=validate.Range(min=0, max=1_000_000), allow_none=True)

class MarkMaintenanceSchema(Schema):
    """ Схема для отметки планового как выполненного """
    id = fields.Int(required=True)
    mileage = fields.Int(required=True, validate=validate.Range(min=0, max=1_000_000))
    cost = fields.Int(validate=validate.Range(min=0), allow_none=True)
    date = fields.Date(format="%Y-%m-%d", allow_none=True)
    isRepeat = fields.Bool(allow_none=True)
    interval = fields.Int(validate=validate.Range(min=1, max=1_000_000), allow_none=True)

class MaintenanceResponseSchema(SQLAlchemySchema):
    """ Схема для сериализации данных обслуживания """
    class Meta:
        model = Maintenance
        include_fk = True
        load_instance = True
    
    id = auto_field()
    author_id = auto_field()
    moto_id = auto_field()
    title = auto_field()
    description = auto_field()
    mileage = auto_field()
    category = auto_field()
    cost = auto_field()
    date = auto_field()
    photo_url = auto_field()
    created_at = auto_field()
    updated_at = auto_field()

class PlannedMaintenanceResponseSchema(SQLAlchemySchema):
    """ Схема для сериализации данные планового обслуживания """
    class Meta:
        model = PlannedMaintenance
        include_fk = True
        load_instance = True

    id = auto_field()
    author_id = auto_field()
    moto_id = auto_field()
    title = auto_field()
    description = auto_field()
    planned_mileage = auto_field()
    category = auto_field()
    created_at = auto_field()
    updated_at = auto_field()