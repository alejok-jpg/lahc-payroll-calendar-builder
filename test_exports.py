from datetime import date
from processes import ProcessType
from generator import generate_process_calendar
from exports import export_calendar_to_excel

def test_export():
    pay_dates_co = [
        date(2026, 1, 29),
        date(2026, 2, 26),
        date(2026, 3, 30),
    ]

    events = generate_process_calendar(
        country="CO",
        process_type=ProcessType.MONTHLY,
        pay_dates=pay_dates_co
    )

    file_path = export_calendar_to_excel(events, country="CO", output_path="Test_Calendar_CO.xlsx")
    print(f"Archivo generado con éxito: {file_path}")

if __name__ == "__main__":
    test_export()