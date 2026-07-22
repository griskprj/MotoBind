from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime

class ManualStepSchema(BaseModel):
    """ Схема шага мануала """
    order: int = Field(..., ge=1)
    title: str = Field(..., min_length=1, max_length=200)
    text: Optional[str] = Field(None, max_length=5000)
    
    @field_validator('order')
    def validate_order(cls, v):
        if v < 1:
            raise ValueError("Порядковый номер должен быть больше 0")
        return v
    
class CreateMaintenanceSchema(BaseModel):
    """ Схема для создания мануала """
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    category: str = Field(..., min_length=1, max_length=100)
    difficult: str = Field(default='easy')
    instrument: Optional[str] = Field(None, max_length=500)
    parts: Optional[str] = Field(None, max_length=500)
    motorcycle: str = Field(..., min_length=1, max_length=100)

    steps: List[ManualStepSchema] = Field(..., min_length=1)

    @field_validator('difficult')
    def validate_difficult(cls, v):
        allowed = ['easy', 'medium', 'hard']
        if v not in allowed:
            raise ValueError(f'Сложность должна быть одной из: {", ".join(allowed)}')
        
        return v
    
    @field_validator('steps')
    def validate_steps_order(cls, v):
        """ Проверяет, что порядок шагов начинается с 1 и идет последовательно """
        if not v: return v

        sorted_steps = sorted(v, key=lambda x: x.order)

        for i, step in enumerate(sorted_steps, start=1):
            if step.order != i:
                raise ValueError(f'Порядок шагов должен быть последовательным. Ожидается {i}, получено {step.order}')
        
        return v
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example" : {
                "title": "Замена масла",
                "description": "Инструкция по замене масла",
                "category": "engine",
                "difficult": "easy",
                "instruments": "Ключ на 18мм, ветошь",
                "parts": "Масло, фильтр",
                "motorcycle": "BMW S1000RR",
                "steps": [
                    {"order": 1, "title": "Подготовка", "text": "Прогрейте двигатель"},
                    {"order": 2, "title": "Слив масла", "text": "Открутите сливную пробку"}
                ]
            }
        }

class UpdateManualSchema(BaseModel):
    """ Схема для обновления мануала """
    title: Optional[str] = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    category: Optional[str] = Field(..., min_length=1, max_length=100)
    difficult: Optional[str] = Field(default='easy')
    instrument: Optional[str] = Field(None, max_length=500)
    parts: Optional[str] = Field(None, max_length=500)
    motorcycle: Optional[str] = Field(..., min_length=1, max_length=100)

    steps: List[ManualStepSchema] = Field(..., min_length=1)

    @field_validator('difficult')
    def validate_difficult(cls, v):
        allowed = ['easy', 'medium', 'hard']
        if v not in allowed:
            raise ValueError(f'Сложность должна быть одной из: {", ".join(allowed)}')
        
        return v
    
    def get_updates(slef) -> dict:
        """ Возвращает только переданные поля """
        return {k: v for k, v in slef.model_dump(exclude_unset=True, exclude_none=True).items() if v is not None}
    
    class Config:
        populate_by_name = True


class ManualResponseSchema(BaseModel):
    """ Схема для ответа с мануалом """
    id: int
    title: str
    description: Optional[str]
    category: str
    difficult: str
    instruments: Optional[str]
    parts: Optional[str]
    motorcycle: str
    status: str
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    steps: List[ManualStepSchema]

    class Config:
        from_attrubutes = True