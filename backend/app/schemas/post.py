from pydantic import BaseModel
from typing import Optional

class PostCreateSchema(BaseModel):
    content: str
    image: Optional[str] = None

class PostUpdateSchema(BaseModel):
    content: Optional[str] = None
    image: Optional[str] = None

class CommentCreateSchema(BaseModel):
    content: str

class CommentUpdateSchema(BaseModel):
    content: str