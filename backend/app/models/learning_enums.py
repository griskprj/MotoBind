import enum


class ContentCategory(str, enum.Enum):
    """Категории курсов и статей."""

    RIDING = "riding"
    REPAIR = "repair"
    GEAR = "gear"
    FIRST_AID = "first_aid"
    LAW = "law"
    TRAVEL = "travel"


class CourseLevel(str, enum.Enum):
    """Уровень сложности курса."""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ContentStatus(str, enum.Enum):
    """Статус публикации курса или статьи."""

    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
