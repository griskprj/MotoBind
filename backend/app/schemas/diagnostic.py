from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DiagnosticResultItemSchema(BaseModel):
    """Один результат: id правила + score."""

    rule_id: str = Field(..., min_length=1)
    score: float = Field(..., ge=0.0, le=1.0)


class SaveDiagnosticReportSchema(BaseModel):
    motorcycle_id: Optional[int] = Field(None, alias="motorcycleId")
    mileage: Optional[int] = Field(None, ge=0, le=1_000_000)
    locked_group: Optional[str] = Field(None, alias="lockedGroup", max_length=32)
    symptoms: List[str] = Field(..., min_length=1, max_length=64)
    answers: Dict[str, str] = Field(default_factory=dict)
    results: List[DiagnosticResultItemSchema] = Field(..., min_length=1, max_length=32)

    model_config = {
        "populate_by_name": True,
        "str_strip_whitespace": True,
    }


class DiagnosticReportResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    motorcycle_id: Optional[int] = None
    mileage: Optional[int] = None
    locked_group: Optional[str] = None
    symptoms: List[str] = Field(default_factory=list)
    answers: Dict[str, str] = Field(default_factory=dict)
    results: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: Optional[datetime] = None
