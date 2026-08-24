from datetime import date, timedelta
import holidays

# Países habilitados
SUPPORTED_COUNTRIES_INFO = {
    "AR": {"name": "Argentina"},
    "CO": {"name": "Colombia"},
    "CR": {"name": "Costa Rica"}
}

class CountryCalendar:
    def __init__(self, country_code: str):
        self.country_code = country_code.upper()
        if self.country_code not in SUPPORTED_COUNTRIES_INFO:
            raise ValueError(f"País no soportado: {self.country_code}")
        try:
            self.holidays = holidays.country_holidays(self.country_code)
        except NotImplementedError:
            self.holidays = {}

    def is_business_day(self, d: date) -> bool:
        if d.weekday() >= 5:  # Sábado (5) o Domingo (6)
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
    return CountryCalendar(country_code)