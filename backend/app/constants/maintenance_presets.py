"""
Шаблоны базовых обслуживаний для быстрого старта.
Используются при первом создании мотоцикла.
"""

BASE_PRESETS = [
    {
        "code": "oil_change",
        "title": "Замена моторного масла и масляного фильтра",
        "category": "engine",
        "description": "Замена моторного масла и масляного фильтра",
        "base_interval_km": 5000,
        "base_interval_days": 365,
        "affects": ["style", "terrain"],
    },
    {
        "code": "air_filter",
        "title": "Замена воздушного фильтра",
        "category": "engine",
        "description": "Замена воздушного фильтра двигателя",
        "base_interval_km": 10000,
        "base_interval_days": 365,
        "affects": ["terrain"],
    },
    {
        "code": "tire_pressure",
        "title": "Проверка давления в шинах",
        "category": "wheel",
        "description": "Проверка и корректировка давления в шинах",
        "base_interval_km": 500,
        "base_interval_days": 7,
        "affects": [],
    },
    {
        "code": "brake_fluid_check",
        "title": "Проверка уровня тормозной жидкости",
        "category": "brakes",
        "description": "Проверка уровня и состояния тормозной жидкости",
        "base_interval_km": 5000,
        "base_interval_days": 90,
        "affects": ["style"],
    },
    {
        "code": "brake_pads_check",
        "title": "Проверка тормозных колодок",
        "category": "brakes",
        "description": "Проверка толщины и состояния тормозных колодок",
        "base_interval_km": 5000,
        "base_interval_days": 90,
        "affects": ["style", "terrain"],
    },
]


DRIVE_PRESETS = {
    "chain": [
        {
            "code": "chain_lube",
            "title": "Смазка цепи",
            "category": "drive",
            "description": "Очистка и смазка приводной цепи",
            "base_interval_km": 500,
            "base_interval_days": 14,
            "affects": ["terrain"],
        },
        {
            "code": "chain_tension",
            "title": "Регулировка натяжения цепи",
            "category": "drive",
            "description": "Проверка и регулировка натяжения приводной цепи",
            "base_interval_km": 1000,
            "base_interval_days": 30,
            "affects": ["style"],
        },
    ],
    "belt": [
        {
            "code": "belt_check",
            "title": "Проверка ремня привода",
            "category": "drive",
            "description": "Проверка состояния и натяжения ремня привода",
            "base_interval_km": 5000,
            "base_interval_days": 90,
            "affects": ["style"],
        },
    ],
    "shaft": [
        {
            "code": "shaft_oil",
            "title": "Замена масла в редукторе",
            "category": "drive",
            "description": "Замена масла в карданном редукторе",
            "base_interval_km": 20000,
            "base_interval_days": 730,
            "affects": [],
        },
    ],
}


# Множители интервалов
STYLE_MULTIPLIERS = {
    "calm": 1.2,        # Спокойная езда — реже
    "normal": 1.0,      # Обычная
    "aggressive": 0.8,  # Агрессивная — чаще
}

TERRAIN_MULTIPLIERS = {
    "city": 1.0,      # Город
    "highway": 1.1,   # Трасса — реже
    "mixed": 1.0,     # Смешанный
    "dusty": 0.7,     # Пыльная местность — чаще
    "offroad": 0.6,   # Бездорожье — ещё чаще
}


def get_presets_for_motorcycle(drive_type="chain"):
    """Возвращает список шаблонов для мотоцикла с указанным типом привода"""
    presets = list(BASE_PRESETS)
    presets.extend(DRIVE_PRESETS.get(drive_type, DRIVE_PRESETS["chain"]))
    return presets


def calculate_interval(preset, style="normal", terrain="mixed"):
    """
    Рассчитывает интервал обслуживания с учётом стиля езды и местности.
    Множители применяются только к тем работам, у которых в affects
    указан соответствующий параметр.
    """
    style_mult = STYLE_MULTIPLIERS.get(style, 1.0)
    terrain_mult = TERRAIN_MULTIPLIERS.get(terrain, 1.0)

    total_mult = 1.0

    affects = preset.get("affects", [])

    if "style" in affects:
        total_mult *= style_mult

    if "terrain" in affects:
        total_mult *= terrain_mult

    interval_km = round(preset["base_interval_km"] * total_mult / 100) * 100
    interval_days = round(preset["base_interval_days"] * total_mult)

    return {
        "interval_km": max(interval_km, 100),
        "interval_days": max(interval_days, 7),
    }