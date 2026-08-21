from datetime import date
from typing import Set, Optional
import holidays

SUPPORTED_COUNTRIES = {
    "AR": "AR",
    "CO": "CO",
    "CR": "CR",
}

def get_holidays(country: str, year: int, custom_holidays: Optional[Set[date]] = None) -> Set[date]:
    """
    Retorna un set de fechas (datetime.date) con los feriados del país y año seleccionados.
    """
    country_code = country.upper().strip()
    
    if country_code not in SUPPORTED_COUNTRIES:
        raise ValueError(
            f"País '{country}' no soportado. Opciones válidas: {list(SUPPORTED_COUNTRIES.keys())}"
        )

    # Invoca la librería oficial instalada
    country_holidays_obj = holidays.country_holidays(country_code, years=year)
    holiday_set: Set[date] = set(country_holidays_obj.keys())

    if custom_holidays:
        holiday_set.update(custom_holidays)

    return holiday_set