from datetime import date, timedelta
from typing import Set, Dict, List, Optional
from processes import ProcessType, ActivityType, get_process_activities
from rules import get_offset
from holidays_engine import get_holidays

def is_business_day(target_date: date, holiday_set: Set[date]) -> bool:
    """Retorna True si la fecha es de lunes a viernes y no es feriado."""
    return target_date.weekday() < 5 and target_date not in holiday_set

def shift_business_days(start_date: date, offset_bh: int, holiday_set: Set[date]) -> date:
    """
    Desplaza una fecha 'offset_bh' días hábiles hacia atrás (offset negativo) 
    o adelante (offset positivo). Si offset es 0 y cae en no hábil, retrocede al hábil previo.
    """
    current_date = start_date

    # Ajuste del ancla (PAY_DAY): Si cae sábado, domingo o feriado, retrocede al día hábil previo
    if offset_bh == 0:
        while not is_business_day(current_date, holiday_set):
            current_date -= timedelta(days=1)
        return current_date

    step = -1 if offset_bh < 0 else 1
    days_to_count = abs(offset_bh)

    while days_to_count > 0:
        current_date += timedelta(days=step)
        if is_business_day(current_date, holiday_set):
            days_to_count -= 1

    return current_date

def generate_process_calendar(
    country: str,
    process_type: ProcessType,
    pay_dates: List[date],
    custom_holidays: Optional[Set[date]] = None
) -> List[Dict]:
    """
    Calcula todos los eventos para un país, proceso y lista de fechas de pago.
    """
    # Identificar todos los años involucrados para cargar sus feriados correspondientes
    years = {d.year for d in pay_dates}
    all_holidays: Set[date] = set()
    for y in years:
        all_holidays.update(get_holidays(country=country, year=y, custom_holidays=custom_holidays))

    activities = get_process_activities(process_type)
    calendar_events = []

    for original_pay_date in pay_dates:
        # Calcular fecha real de pago (ajustada a día hábil si correspondía)
        actual_pay_day = shift_business_days(original_pay_date, 0, all_holidays)
        period_label = original_pay_date.strftime("%Y-%m")

        for activity in activities:
            offset = get_offset(activity)
            calculated_date = shift_business_days(actual_pay_day, offset, all_holidays)

            calendar_events.append({
                "period": period_label,
                "country": country.upper(),
                "process": process_type.name,
                "activity": activity.name,
                "offset_bh": offset,
                "date": calculated_date,
                "day_name": calculated_date.strftime("%A"),
            })

    return calendar_events