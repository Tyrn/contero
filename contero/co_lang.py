"""Labels in supported languages
"""


_EN = {
    "co-toolbar-title": "Power Supplies",
    "co-no-ps-selected": "No power supply selected",
    "co-ps-label-1": "Power supply",
    "co-exit": "Exit",
    "co-discover-ps": "Discover",
    "co-details": "Details",
    "co-details-l": "details",
    "co-about": "About",
    "co-close-button": "CLOSE",
    "co-app-name": "Contero",
    "co-app-running-on": "Running on",
    "co-output-current-l": "output current",
    "co-supplies": "List",
    "co-supply-details": "Details",
}


_RU = {
    "co-toolbar-title": "Источники",
    "co-no-ps-selected": "Источник не выбран",
    "co-ps-label-1": "Источник",
    "co-exit": "Выход",
    "co-discover-ps": "Обнаружить источники",
    "co-details": "Детали",
    "co-details-l": "детали",
    "co-about": "О приложении",
    "co-close-button": "ЗАКРЫТЬ",
    "co-app-name": "Contero",
    "co-app-running-on": "Выполняется на",
    "co-output-current-l": "ток в нагрузке",
    "co-supplies": "Список",
    "co-supply-details": "Детали",
}


_T = _EN


_LANG = {
    "EN": _EN,
    "RU": _RU,
}


def T(key):
    return _T[key]


def languages():
    return _LANG


def set_language(lng):
    global _T
    _T = _LANG[lng]
