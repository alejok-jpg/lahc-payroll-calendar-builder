from typing import Dict

SUPPORTED_COUNTRIES_INFO: Dict[str, Dict[str, str]] = {
    "AR": {"name": "Argentina", "currency": "ARS"},
    "CO": {"name": "Colombia", "currency": "COP"},
    "CR": {"name": "Costa Rica", "currency": "CRC"},
}

def get_country_name(country_code: str) -> str:
    code = country_code.upper().strip()
    if code in SUPPORTED_COUNTRIES_INFO:
        return SUPPORTED_COUNTRIES_INFO[code]["name"]
    raise ValueError(f"País '{country_code}' no está soportado.")