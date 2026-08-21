from datetime import date, timedelta
import holidays

SUPPORTED_COUNTRIES_INFO = {
    "AR": {"name": "Argentina"},
    "CL": {"name": "Chile"},
    "CO": {"name": "Colombia"},
    "CR": {"name": "Costa Rica"},
    "MX": {"name": "México"},
    "PE": {"name": "Perú"},
    "BR": {"name": "Brasil"},
    "UY": {"name": "Uruguay"}
}

class CountryCalendar:
    def __init__(self, country_code: str):
        self.country_code = country_code.upper()
        # Carga los feriados oficiales usando la librería holidays
        try:
            self.holidays = holidays.country_holidays(self.country_code)
        except NotImplementedError:
            self.holidays = {}

    def is_business_day(self, d: date) -> bool:
        # Lunes=0, Domingo=6. Fines de semana = 5 y 6
        if d.weekday() >= 5:
            return False
        if d in self.holidays:
            return False
        return True

    def offset_business_days(self, base_date: date, offset: int) -> date:
        current = base_date
        step = 1 if offset > 0 else -1
        remaining = abs(offset)

        while remaining > 0:
            current += timedelta(days=step)
            if self.is_business_day(current):
                remaining -= 1

        return current

def get_country_calendar(country_code: str) -> CountryCalendar:
    """Función fábrica para instanciar el calendario del país."""
    return CountryCalendar(country_code)