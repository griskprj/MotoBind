from pydantic import BaseModel, Field


class SnoozeSchema(BaseModel):
    """
    Валидация для PUT /reminders/<id>/snooze.

    days: сколько дней отложить. Мин 1, макс 30.
    """
    days: int = Field(default=7, ge=1, le=30)