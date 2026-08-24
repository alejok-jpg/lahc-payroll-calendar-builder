from datetime import date
from typing import List, Dict
from countries import get_country_calendar
from processes import ProcessType, PROCESS_RULES

def generate_process_calendar(
    country: str,
    process_type: ProcessType,
    pay_dates: List[date]
) -> List[Dict]:
    cal = get_country_calendar(country)
    rules = PROCESS_RULES.get(process_type, [])
    events = []

    sorted_dates = sorted(pay_dates)
    dates_by_month = {}
    for pd in sorted_dates:
        m_key = pd.strftime("%Y-%m")
        dates_by_month.setdefault(m_key, []).append(pd)

    for pay_date in sorted_dates:
        m_key = pay_date.strftime("%Y-%m")
        if len(dates_by_month[m_key]) > 1:
            idx = dates_by_month[m_key].index(pay_date) + 1
            period_label = f"{m_key} (Q{idx})"
        else:
            period_label = m_key

        for rule in rules:
            calculated_date = cal.offset_business_days(pay_date, rule.offset_bh)
            events.append({
                "country": country,
                "process": process_type.name,
                "period": period_label,
                "pay_date": pay_date,
                "activity": rule.activity,
                "offset_bh": rule.offset_bh,
                "time": rule.default_time,
                "date": calculated_date
            })

    return events