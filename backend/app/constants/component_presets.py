"""
Базовый набор компонентов для мотоцикла.

Источник интервалов — app.constants.maintenance_presets
(BASE_PRESETS + DRIVE_PRESETS по drive_type), чтобы не дублировать.

В компоненты попадают ТОЛЬКО заменимые расходники.
Проверки/регулировки (tire_pressure, brake_fluid_check, chain_tension,
belt_check) остаются в старой модели Maintenance (quick_start) и
компонентами НЕ становятся.
"""

from app.constants.maintenance_presets import (
    BASE_PRESETS,
    DRIVE_PRESETS,
    calculate_interval,
)

# Ключи пресетов maintenance_presets, которые раскладываются в компоненты.
# Значение — список component-пресетов (ключ, имя, категория, источник интервала).
# source: "preset:<code>" — взять base_interval_* из пресета с этим code;
#         None — без интервала по умолчанию (пользователь задаст сам).

_BASE_COMPONENTS = [
    # oil_change в пресете склеивает масло + фильтр → разбиваем на два компонента
    {
        "key": "engine_oil",
        "name": "Моторное масло",
        "category": "fluid",
        "interval_source": "preset:oil_change",
    },
    {
        "key": "oil_filter",
        "name": "Масляный фильтр",
        "category": "filter",
        "interval_source": "preset:oil_change",
    },
    {
        "key": "air_filter",
        "name": "Воздушный фильтр",
        "category": "filter",
        "interval_source": "preset:air_filter",
    },
    # Свечей в пресетах нет — компонент без интервала по умолчанию
    {
        "key": "spark_plugs",
        "name": "Свечи зажигания",
        "category": "ignition",
        "interval_source": None,
    },
    # brake_pads_check склеивает перед/зад → разбиваем
    {
        "key": "brake_pads_front",
        "name": "Передние тормозные колодки",
        "category": "brake",
        "interval_source": "preset:brake_pads_check",
    },
    {
        "key": "brake_pads_rear",
        "name": "Задние тормозные колодки",
        "category": "brake",
        "interval_source": "preset:brake_pads_check",
    },
    # Тормозная жидкость — компонент (fluid), источник интервала — brake_fluid_check
    {
        "key": "brake_fluid_front",
        "name": "Тормозная жидкость (передний контур)",
        "category": "fluid",
        "interval_source": "preset:brake_fluid_check",
    },
    {
        "key": "brake_fluid_rear",
        "name": "Тормозная жидкость (задний контур)",
        "category": "fluid",
        "interval_source": "preset:brake_fluid_check",
    },
]

_DRIVE_COMPONENTS = {
    "chain": [
        {
            "key": "drive_chain",
            "name": "Приводная цепь",
            "category": "drive",
            "interval_source": "preset:chain_lube",
        },
        {
            "key": "drive_sprocket_front",
            "name": "Ведущая звезда",
            "category": "drive",
            "interval_source": "preset:chain_lube",
        },
        {
            "key": "drive_sprocket_rear",
            "name": "Ведомая звезда",
            "category": "drive",
            "interval_source": "preset:chain_lube",
        },
    ],
    "belt": [
        {
            "key": "drive_belt",
            "name": "Приводной ремень",
            "category": "drive",
            "interval_source": "preset:belt_check",
        },
    ],
    "shaft": [],
}


def _find_preset(code: str, drive_type: str):
    """Ищет preset по code в BASE_PRESETS или DRIVE_PRESETS[drive_type]."""
    for p in BASE_PRESETS:
        if p["code"] == code:
            return p
    for p in DRIVE_PRESETS.get(drive_type, []):
        if p["code"] == code:
            return p
    return None


def get_component_presets_for_motorcycle(drive_type: str = "chain") -> list[dict]:
    """
    Возвращает список component-пресетов для мотоцикла с указанным типом привода.

    Каждый элемент:
      {key, name, category, interval_km, interval_days}
    где interval_* — уже посчитаны через calculate_interval(preset, style, terrain)
    (или None, если у пресета нет источника).
    """
    presets = list(_BASE_COMPONENTS) + list(_DRIVE_COMPONENTS.get(drive_type, []))
    return presets


def resolve_interval(
    component_preset: dict,
    drive_type: str,
    style: str = "normal",
    terrain: str = "mixed",
) -> tuple[int | None, int | None]:
    """
    Возвращает (interval_km, interval_days) для component-пресета.

    interval_source = "preset:<code>" → берём из maintenance_presets и
    прогоняем через calculate_interval (учёт style/terrain).
    interval_source = None → (None, None).
    """
    src = component_preset.get("interval_source")
    if not src:
        return None, None

    if not src.startswith("preset:"):
        return None, None

    code = src.split(":", 1)[1]
    preset = _find_preset(code, drive_type)
    if preset is None:
        return None, None

    interval = calculate_interval(preset, style=style, terrain=terrain)
    return interval["interval_km"], interval["interval_days"]


def build_component_set(
    drive_type: str = "chain", style: str = "normal", terrain: str = "mixed"
) -> list[dict]:
    """
    Готовый набор для создания компонентов:
    [{template_key, name, category, interval_km, interval_days}, ...]
    """
    result = []
    for p in get_component_presets_for_motorcycle(drive_type):
        km, days = resolve_interval(p, drive_type, style=style, terrain=terrain)
        result.append(
            {
                "template_key": p["key"],
                "name": p["name"],
                "category": p["category"],
                "interval_km": km,
                "interval_days": days,
            }
        )
    return result
