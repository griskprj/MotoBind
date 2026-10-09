"""Транслитерация и генерация URL-slug."""
import re

_CYRILLIC = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "e",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "sch",
    "ъ": "",
    "ы": "y",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}


def slugify(value: str) -> str:
    """«Мото-Сервис №1» → «moto-servis-1»"""
    if not value:
        return ""
    value = value.lower().strip()
    value = "".join(_CYRILLIC.get(ch, ch) for ch in value)
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value


def unique_slug(base: str, exists_fn, max_attempts: int = 50) -> str:
    """
    Генерирует slug с суффиксом -1, -2, ... пока не станет уникальным.
    exists_fn: callable(slug) -> bool
    """
    slug = slugify(base) or "item"
    if not exists_fn(slug):
        return slug
    for i in range(1, max_attempts):
        candidate = f"{slug}-{i}"
        if not exists_fn(candidate):
            return candidate
    # крайний случай — добавим хеш
    import uuid

    return f"{slug}-{uuid.uuid4().hex[:6]}"
