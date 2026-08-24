from datetime import date, timedelta
from typing import Dict, List
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from processes import ProcessType

def generate_multiprocess_template(output_path: str = "Template_PayDates.xlsx", year: int = 2027) -> str:
    """
    Genera un archivo Excel con una pestaña por cada proceso disponible.
    Para TERMINATION, genera la columna TERMINATION_REQUEST_DATE con ejemplos semanales.
    """
    wb = openpyxl.Workbook()
    
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_body = Font(name="Calibri", size=11)
    fill_header = PatternFill(start_color="2F5597", end_color="2F5597", fill_type="solid")
    fill_term_header = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")

    thin_border = Border(
        left=Side(style="thin", color="D9D9D9"),
        right=Side(style="thin", color="D9D9D9"),
        top=Side(style="thin", color="D9D9D9"),
        bottom=Side(style="thin", color="D9D9D9"),
    )

    for proc in ProcessType:
        ws = wb.create_sheet(title=proc.name)
        ws.views.sheetView[0].showGridLines = True

        # Definir encabezado y fechas de ejemplo según el proceso
        if proc == ProcessType.TERMINATION:
            header_col = "TERMINATION_REQUEST_DATE (DD/MM/YYYY)"
            hdr_fill = fill_term_header
            # Ejemplo: Todos los martes y jueves de enero
            sample_dates = []
            curr = date(year, 1, 1)
            while curr.month == 1:
                if curr.weekday() in (1, 3):  # Martes o Jueves
                    sample_dates.append(curr)
                curr += timedelta(days=1)
        elif proc == ProcessType.BIWEEKLY:
            header_col = "PAY_DATE (DD/MM/YYYY)"
            hdr_fill = fill_header
            sample_dates = [
                date(year, 1, 15), date(year, 1, 29),
                date(year, 2, 15), date(year, 2, 26)
            ]
        elif proc == ProcessType.MONTHLY:
            header_col = "PAY_DATE (DD/MM/YYYY)"
            hdr_fill = fill_header
            sample_dates = [date(year, m, 28) for m in range(1, 13)]
        else:
            header_col = "PAY_DATE (DD/MM/YYYY)"
            hdr_fill = fill_header
            sample_dates = [date(year, 6, 30), date(year, 12, 20)]

        # Escribir encabezado
        cell_hdr = ws.cell(row=1, column=1, value=header_col)
        cell_hdr.font = font_header
        cell_hdr.fill = hdr_fill
        cell_hdr.alignment = Alignment(horizontal="center", vertical="center")
        cell_hdr.border = thin_border
        ws.row_dimensions[1].height = 24

        # Escribir fechas de ejemplo
        for row_idx, d_val in enumerate(sample_dates, 2):
            cell_data = ws.cell(row=row_idx, column=1, value=d_val.strftime("%d/%m/%Y"))
            cell_data.font = font_body
            cell_data.alignment = Alignment(horizontal="center", vertical="center")
            cell_data.border = thin_border
            ws.row_dimensions[row_idx].height = 20

        ws.column_dimensions["A"].width = 36

    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])

    wb.save(output_path)
    return output_path


def load_multiprocess_pay_dates_from_excel(file_content) -> Dict[str, List[date]]:
    """
    Lee el archivo Excel subido por el usuario y extrae las fechas por proceso.
    Soporta columnas: PAY_DATE, TERMINATION_REQUEST_DATE, CUT_OFF_DATE, FECHA, etc.
    """
    excel_file = pd.ExcelFile(file_content)
    result: Dict[str, List[date]] = {}

    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        if df.empty:
            continue

        # Normalizar nombres de columnas para que no dependa de mayúsculas ni espacios
        col_name = None
        for c in df.columns:
            clean_c = str(c).upper()
            if any(k in clean_c for k in ["PAY_DATE", "TERMINATION", "CUT_OFF", "FECHA", "DATE"]):
                col_name = c
                break

        if not col_name:
            # Si no coincide con ninguno, toma la primera columna por defecto
            col_name = df.columns[0]

        extracted_dates = []
        for val in df[col_name].dropna():
            try:
                # Si viene como Timestamp o string de fecha
                dt = pd.to_datetime(val, dayfirst=True)
                extracted_dates.append(dt.date())
            except Exception:
                continue

        if extracted_dates:
            result[sheet_name] = sorted(list(set(extracted_dates)))

    return result