from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ManualStepSchema(BaseModel):
    """Схема шага мануала"""

    order: int = Field(..., ge=1)
    title: str = Field(..., min_length=1, max_length=200)
    tip: Optional[str] = Field(None, max_length=256)
    warning: Optional[str] = Field(None, max_length=256)
    text: Optional[str] = Field(None, max_length=5000)

    image: Optional[str] = Field(None)
    result: Optional[str] = Field(None, max_length=500)

    @field_validator("order")
    def validate_order(cls, v):
        if v < 1:
            raise ValueError("Порядковый номер должен быть больше 0")
        return v


class CreateManualSchema(BaseModel):
    """Схема для создания мануала"""

    # Основная информация
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    category: str = Field(..., min_length=1, max_length=100)
    difficult: str = Field(default="easy")
    motorcycle: str = Field(..., min_length=1, max_length=100)

    time_estimate: Optional[str] = Field(None, max_length=64)
    interval: Optional[str] = Field(None, max_length=64)

    safety_tip: Optional[str] = Field(None, max_length=1000)
    warnings: Optional[str] = Field(None, max_length=1000)
    conditions: Optional[str] = Field(None, max_length=1000)

    instruments: Optional[str] = Field(None, max_length=500)
    parts: Optional[str] = Field(None, max_length=500)

    docs_links: Optional[List[str]] = Field(None, max_length=10)

    specs: Optional[Dict[str, Any]] = Field(None)

    aftercare: Optional[str] = Field(None, max_length=2000)
    tip: Optional[str] = Field(None, max_length=256)

    steps: List[ManualStepSchema] = Field(..., min_length=1)

    @field_validator("difficult")
    def validate_difficult(cls, v):
        allowed = ["easy", "medium", "hard"]
        if v not in allowed:
            raise ValueError(f'Сложность должна быть одной из: {", ".join(allowed)}')
        return v

    @field_validator("steps")
    def validate_steps_order(cls, v):
        """Проверяет, что порядок шагов начинается с 1 и идет последовательно"""
        if not v:
            return v

        sorted_steps = sorted(v, key=lambda x: x.order)

        for i, step in enumerate(sorted_steps, start=1):
            if step.order != i:
                raise ValueError(f"Порядок шагов должен быть последовательным. Ожидается {i}, получено {step.order}")
        return v

    @field_validator("docs_links")
    def validate_docs_links(cls, v):
        """Проверяет, что все ссылки валидны"""
        if v is None:
            return v
        for url in v:
            if not url.startswith(("http://", "https://")):
                raise ValueError(f"Некорректный URL: {url}")
        return v

    model_config = ConfigDict(populate_by_name=True)


class UpdateManualSchema(BaseModel):
    """Схема для обновления мануала"""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    difficult: Optional[str] = Field(None)
    motorcycle: Optional[str] = Field(None, min_length=1, max_length=100)

    time_estimate: Optional[str] = Field(None, max_length=64)
    interval: Optional[str] = Field(None, max_length=64)

    safety_tip: Optional[str] = Field(None, max_length=1000)
    warnings: Optional[str] = Field(None, max_length=1000)
    conditions: Optional[str] = Field(None, max_length=1000)

    instruments: Optional[str] = Field(None, max_length=500)
    parts: Optional[str] = Field(None, max_length=500)

    docs_links: Optional[List[str]] = Field(None, max_length=10)
    specs: Optional[Dict[str, Any]] = Field(None)
    aftercare: Optional[str] = Field(None, max_length=2000)

    tip: Optional[str] = Field(None, max_length=256)

    steps: Optional[List[ManualStepSchema]] = Field(None, min_length=1)

    @field_validator("difficult")
    def validate_difficult(cls, v):
        if v is None:
            return v
        allowed = ["easy", "medium", "hard"]
        if v not in allowed:
            raise ValueError(f'Сложность должна быть одной из: {", ".join(allowed)}')
        return v

    @field_validator("docs_links")
    def validate_docs_links(cls, v):
        if v is None:
            return v
        for url in v:
            if not url.startswith(("http://", "https://")):
                raise ValueError(f"Некорректный URL: {url}")
        return v

    def get_updates(self) -> dict:
        """Возвращает только переданные поля"""
        return {k: v for k, v in self.model_dump(exclude_unset=True, exclude_none=True).items() if v is not None}

    model_config = ConfigDict(populate_by_name=True)


class ManualStepResponseSchema(BaseModel):
    """Шаг мануала в ответе API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    manual_id: int
    order: int
    title: str
    text: Optional[str] = None
    tip: Optional[str] = None
    warning: Optional[str] = None
    result: Optional[str] = None
    image: Optional[str] = None


class ManualResponseSchema(BaseModel):
    """Мануал в ответе API. Совпадает с Manual.to_dict()."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int
    author_username: Optional[str] = None
    title: str
    description: Optional[str] = None
    category: str
    difficult: Optional[str] = None
    motorcycle: str

    time_estimate: Optional[str] = None
    interval: Optional[str] = None
    safety_tip: Optional[str] = None
    warnings: Optional[str] = None
    conditions: Optional[str] = None
    docs_links: Optional[list] = None
    specs: Optional[dict] = None
    aftercare: Optional[str] = None

    instruments: Optional[str] = None
    parts: Optional[str] = None
    tip: Optional[str] = None

    status: str
    created_at: Optional[datetime] = None
    steps: list[ManualStepResponseSchema] = []


class MaintenanceManualStepSchema(BaseModel):
    """Шаг мануала для ответа на /api/manual/ (без id и manual_id)."""

    model_config = ConfigDict(from_attributes=True)

    order: int
    title: str
    text: Optional[str] = None
    tip: Optional[str] = None
    warning: Optional[str] = None
    image: Optional[str] = None
    result: Optional[str] = None


class ManualForMaintenanceResponseSchema(BaseModel):
    """Мануал для /api/manual/ (get_manual_for_maintenance_endpoint)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None
    category: str
    difficult: Optional[str] = None
    time_estimate: Optional[str] = None
    interval: Optional[str] = None
    safety_tip: Optional[str] = None
    warnings: Optional[str] = None
    conditions: Optional[str] = None
    docs_links: Optional[list] = None
    specs: Optional[dict] = None
    aftercare: Optional[str] = None
    instruments: Optional[str] = None
    parts: Optional[str] = None
    motorcycle: str
    tip: Optional[str] = None
    steps: list[MaintenanceManualStepSchema] = []
