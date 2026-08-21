from holidays_engine import get_holidays

def test_country_holidays():
    year = 2026
    for country in ["AR", "CO", "CR"]:
        feriados = get_holidays(country, year)
        print(f"--- Feriados {country} ({year}) --- Total: {len(feriados)}")
        for f in sorted(feriados)[:5]:
            print(f"  - {f}")
        print()

if __name__ == "__main__":
    test_country_holidays()