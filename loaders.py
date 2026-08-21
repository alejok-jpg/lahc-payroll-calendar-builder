from datetime import datetime, date
from typing import Dict, List
import openpyxl
from processes import ProcessType

def generate_multiprocess_template(filepath: str = "template_pay_dates.xlsx", year: int = 2027) -> str:
    """Genera una plantilla Excel con una hoja por cada proceso disponible."""
    wb = openpyxl.Workbook()
    default_sheet = wb.active

    for p in ProcessType:
        ws = wb.create_sheet(title=p.name[:31])
        ws.append(["Period", "Pay_Date (DD/MM/YYYY o YYYY-MM-DD)"])
        for m in range(1, 13):
            ws.append([f"{year}-{m:02d}", ""])
        ws.column_dimensions["A"].width = 15
        ws.column_dimensions["B"].width = 30

    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])

    wb.save(filepath)
    return filepath

def load_multiprocess_pay_dates_from_excel(filepath_or_buffer) -> Dict[str, List[date]]:
    """Lee un Excel con fechas separadas por pestañas según el nombre del proceso."""
    wb = openpyxl.load_workbook(filepath_or_buffer, data_only=True)
    results: Dict[str, List[date]] = {}

    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        dates = []
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row or row[1] is None or str(row[1]).strip() == "":
                continue
            val = row[1]
            if isinstance(val, datetime):
                dates.append(val.date())
            elif isinstance(val, date):
                dates.append(val)
            elif isinstance(val, str):
                for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d"):
                    try:
                        dates.append(datetime.strptime(val.strip(), fmt).date())
                        break
                    except ValueError:
                        pass
        if dates:
            results[sheet_name.upper()] = sorted(list(set(dates)))

    return results