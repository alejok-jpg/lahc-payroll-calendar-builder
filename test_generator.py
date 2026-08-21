from datetime import date
from processes import ProcessType
from generator import generate_process_calendar

def test_generation():
    # Fechas de pago de ejemplo para Colombia 2026
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

    print(f"--- Eventos Generados para Colombia (MONTHLY - Enero 2026) --- Total eventos: {len(events)}")
    for ev in events[:11]:  # Primer ciclo mensual (11 actividades)
        print(f"{ev['activity']:<20} | Offset: {ev['offset_bh']:>2} BH | Fecha: {ev['date']} ({ev['day_name']})")

if __name__ == "__main__":
    test_generation()