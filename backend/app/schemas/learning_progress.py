from app.schemas.learning_common import CourseProgressSchema
from pydantic import BaseModel


class CompleteLessonResponseSchema(BaseModel):
    completed: bool
    course_progress: CourseProgressSchema
