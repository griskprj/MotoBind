from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from datetime import datetime, date


class CreateEventSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=64)
    description: str = Field(..., min_length=1, max_length=2048)
    date: Any = None
    created_at: Any = None
    updated_at: Any = None

    @field_validator('date', mode='before')
    @classmethod
    def parse_date(cls, v: Any) -> Optional[date]:
        """Преобразует любой ввод в объект date или None."""
        if v is None:
            return None
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Неверный формат даты. Используйте ГГГГ-ММ-ДД')
        if isinstance(v, datetime):
            return v.date()
        raise ValueError(f'Неподдерживаемый тип для даты: {type(v)}')
    
class UpdateEventSchema(BaseModel):
    """ Схема для обновления мероприятия """
    title: Optional[str] = Field(..., min_length=1, max_length=64)
    description: Optional[str] = Field(..., min_length=1, max_length=2048)
    date: Optional[Any] = None
    created_at: Optional[Any] = None
    updated_at: Optional[Any] = None
    status: Optional[str] = Field(..., min_length=1)

    @field_validator('status')
    def validate_status(cls, v):
        allowed = ['moderate', 'planned', 'active', 'complete', 'decline']
        if v not in allowed:
            raise ValueError(f'Статус должен быть одним из: {", ".join(allowed)}')

        return v
    
    def get_updates(self) -> dict:
        """Возвращает только установленные поля с корректными типами"""
        updates = {}
        for key, value in self.model_dump(exclude_unset=True, exclude_none=True).items():
            if value is not None:
                # Преобразуем строку в datetime для поля date
                if key == 'date' and isinstance(value, str):
                    try:
                        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        try:
                            date_obj = datetime.strptime(value, '%Y-%m-%d').date()
                            value = datetime.combine(date_obj, datetime.min.time())
                        except ValueError:
                            raise ValueError('Неверный формат даты. Используйте ГГГГ-ММ-ДД или ГГГГ-ММ-ДД ЧЧ:ММ:СС')
                updates[key] = value
        return updates

class UpdateEventStatusSchema(BaseModel):
    """ Схема для обновления статуса мероприятия """
    status: str = Field(..., min_length=1)

    @field_validator('status')
    def validate_status(cls, v):
        allowed = ['moderate', 'planned', 'active', 'complete', 'decline']
        if v not in allowed:
            raise ValueError(f'Статус должен быть одним из: {", ".join(allowed)}')

        return v