from marshmallow import Schema, fields, validate, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from app.models.manual import Manual, ManualStep

class ManualStepSchema(Schema):
    """ Схема для шага мануала """
    order = fields.Int(required=True, validate=validate.Range(min=0))
    title = fields.Str(required=True, validate=validate.Length(min=1, max=256))
    text = fields.Str(allow_none=True)

class ManualCreateSchema(Schema):
    """ Схема для создания мануала """
    title = fields.Str(required=True, validate=validate.Length(min=1, max=64))
    description = fields.Str(allow_none=True)
    category = fields.Str(required=True)
    difficult = fields.Str(required=True, validate=validate.OneOf(['easy', 'medium', 'hard']))
    instruments = fields.Str(allow_none=True)
    parts = fields.Str(allow_none=True)
    motorcycle = fields.Str(required=True, validate=validate.Length(min=1))
    steps = fields.List(fields.Nested(ManualStepSchema), required=True, validate=validate.Length(min=1))

class ManualResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Manual
        include_fk = True
        load_instance = True
    
    id = auto_field()
    author_id = auto_field()
    title = auto_field()
    description = auto_field()
    category = auto_field
    difficult = auto_field()
    instruments = auto_field()
    parts = auto_field()
    parts = auto_field()
    motorcycle = auto_field()
    status = auto_field()
    rejection_reason = auto_field()
    created_at = auto_field()
    steps = fields.List(fields.Nested(ManualStepSchema))