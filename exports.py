import os
import re
from datetime import date
from typing import List, Dict, Optional
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image

def export_multiprocess_calendar_to_excel(
    events_by_process: Dict[str, List[Dict]],
    country: str,
    client_name: str = "CLIENTE",
    output_path: str = "Payroll_Calendar.xlsx",
    logo_path: Optional[str] = None
) -> str:
    """
    Exporta los eventos a un archivo Excel con una pestaña por proceso, 
    respetando múltiples ciclos o quincenas por mes.
    """
    wb = openpyxl.Workbook()

    font_title = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_body = Font(name="Calibri", size=11)
    
    fill_title = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    fill_header = PatternFill(start_color="2F5597", end_color="2F5597", fill_type="solid")
    fill_zebra = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")

    thin_border = Border(
        left=Side(style="thin", color="D9D9D9"),
        right=Side(style="thin", color="D9D9D9"),
        top=Side(style="thin", color="D9D9D9"),
        bottom=Side(style="thin", color="D9D9D9"),
    )

    for proc_name, events in events_by_process.items():
        if not events:
            continue
        
        ws = wb.create_sheet(title=proc_name[:31])
        ws.views.sheetView[0].showGridLines = True

        # Obtener los periodos únicos ordenados cronológicamente por pay_date
        period_order = []
        for ev in sorted(events, key=lambda x: x["pay_date"]):
            if ev["period"] not in period_order:
                period_order.append(ev["period"])

        total_cols = 3 + len(period_order)

        # Inserción de Logo
        has_logo = logo_path and os.path.exists(logo_path)
        start_row = 1
        if has_logo:
            img = Image(logo_path)
            img.width = 150
            img.height = 50
            ws.add_image(img, "A1")
            ws.row_dimensions[1].height = 22
            ws.row_dimensions[2].height = 22
            ws.row_dimensions[3].height = 12
            start_row = 5

        # Título
        ws.merge_cells(start_row=start_row, start_column=1, end_row=start_row, end_column=total_cols)
        title_cell = ws.cell(
            row=start_row,
            column=1,
            value=f"PAYROLL CALENDAR - {client_name.upper()} | {proc_name} ({country.upper()})"
        )
        title_cell.font = font_title
        title_cell.fill = fill_title
        title_cell.alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[start_row].height = 30

        # Encabezados
        header_row = start_row + 1
        headers = ["Process", "Activity", "Offset (BH)"] + period_order
        ws.row_dimensions[header_row].height = 24

        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=header_row, column=col_num, value=header)
            cell.font = font_header
            cell.fill = fill_header
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = thin_border

        # Matriz
        matrix: Dict[tuple, Dict[str, date]] = {}
        for ev in events:
            key = (ev["process"], ev["activity"], ev["offset_bh"])
            if key not in matrix:
                matrix[key] = {}
            matrix[key][ev["period"]] = ev["date"]

        # Filas de actividades
        current_row = header_row + 1
        for row_idx, ((proc, act, offset), dates_by_period) in enumerate(matrix.items()):
            ws.row_dimensions[current_row].height = 20
            use_zebra = (row_idx % 2 == 1)

            c1 = ws.cell(row=current_row, column=1, value=proc)
            c2 = ws.cell(row=current_row, column=2, value=act)
            c3 = ws.cell(row=current_row, column=3, value=f"{offset} BH")
            c3.alignment = Alignment(horizontal="center", vertical="center")

            for c in (c1, c2, c3):
                c.font = font_body
                c.border = thin_border
                if use_zebra:
                    c.fill = fill_zebra

            for col_offset, period in enumerate(period_order):
                col_num = 4 + col_offset
                date_val = dates_by_period.get(period)
                cell = ws.cell(row=current_row, column=col_num)
                cell.value = date_val.strftime("%d/%m/%Y") if date_val else "-"
                cell.font = font_body
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.border = thin_border
                if use_zebra:
                    cell.fill = fill_zebra

            current_row += 1

        # Ancho de columnas
        for col in ws.columns:
            max_len = max(len(str(cell.value or "")) for cell in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = max(max_len + 4, 15)

    if "Sheet" in wb.sheetnames and len(wb.sheetnames) > 1:
        wb.remove(wb["Sheet"])

    wb.save(output_path)
    return output_path