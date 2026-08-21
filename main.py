import os
import re
from datetime import datetime, date
from typing import List, Optional
from countries import SUPPORTED_COUNTRIES_INFO
from processes import ProcessType
from generator import generate_process_calendar
from exports import export_calendar_to_excel
from loaders import load_pay_dates_from_excel, generate_pay_dates_template

def prompt_client_name() -> str:
    print("\n--- PASO 0: CLIENTE ---")
    while True:
        client = input("Ingrese el nombre del Cliente: ").strip()
        if client:
            return client
        print("El nombre del cliente no puede quedar vacío.")

def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>| ]', '_', name.strip())

def prompt_country() -> str:
    print("\n--- PASO 1: SELECCIONE EL PAÍS ---")
    countries = list(SUPPORTED_COUNTRIES_INFO.keys())
    for idx, code in enumerate(countries, 1):
        info = SUPPORTED_COUNTRIES_INFO[code]
        print(f"[{idx}] {code} - {info['name']}")

    while True:
        choice = input("\nIngrese el número o código del país: ").strip().upper()
        if choice in countries:
            return choice
        if choice.isdigit() and 1 <= int(choice) <= len(countries):
            return countries[int(choice) - 1]
        print("Opción inválida. Intente de nuevo.")

def prompt_processes() -> List[ProcessType]:
    print("\n--- PASO 2: SELECCIONE LOS PROCESOS ---")
    all_processes = list(ProcessType)
    for idx, p in enumerate(all_processes, 1):
        print(f"[{idx}] {p.name}")

    print("\nIngrese los números separados por coma (ejemplo: 1, 2) o 'ALL':")
    while True:
        raw_in = input("> ").strip().upper()
        if raw_in == "ALL":
            return all_processes
        try:
            indices = [int(x.strip()) for x in raw_in.split(",") if x.strip()]
            selected = [all_processes[i - 1] for i in indices if 1 <= i <= len(all_processes)]
            if selected:
                return selected
        except (ValueError, IndexError):
            pass
        print("Selección inválida. Intente de nuevo.")

def parse_date_input(val_str: str) -> date:
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(val_str.strip(), fmt).date()
        except ValueError:
            pass
    return None

def prompt_pay_dates() -> List[date]:
    print("\n--- PASO 3: CARGA DE FECHAS DE PAGO (PAY DAYS) ---")
    print("[1] Carga Masiva vía Excel (.xlsx)")
    print("[2] Carga Manual (Uno o varios meses)")
    print("[3] Generar Plantilla Excel vacía")

    while True:
        opt = input("\nSeleccione una opción (1/2/3): ").strip()

        if opt == "1":
            file_path = input("Ingrese la ruta/nombre del archivo Excel: ").strip()
            if not os.path.exists(file_path):
                print(f"Error: El archivo '{file_path}' no existe. Intente nuevamente.")
                continue
            dates = load_pay_dates_from_excel(file_path)
            if not dates:
                print("Error: No se encontraron fechas válidas en el archivo.")
                continue
            print(f">> Se cargaron exitosamente {len(dates)} fechas de pago.")
            return dates

        elif opt == "2":
            dates = []
            while True:
                val = input("\nIngrese la fecha de pago (DD/MM/YYYY o YYYY-MM-DD): ").strip()
                parsed = parse_date_input(val)
                
                if not parsed:
                    print("   ✗ Formato inválido. Intente con DD/MM/YYYY o YYYY-MM-DD.")
                    continue

                dates.append(parsed)
                print(f"   ✓ Fecha registrada: {parsed.strftime('%d/%m/%Y')} (Periodo: {parsed.strftime('%Y-%m')})")

                seguir = input("\n¿Desea ingresar la fecha de otro mes? (s/n) [Default 'n']: ").strip().lower()
                if seguir not in ("s", "si", "sí", "y", "yes"):
                    break
            
            if dates:
                return sorted(list(set(dates)))
            print("No se ingresó ninguna fecha. Intente nuevamente.")

        elif opt == "3":
            year_input = input("¿Para qué año desea generar la plantilla? (ej. 2026): ").strip()
            y = int(year_input) if year_input.isdigit() else 2026
            tpl_path = generate_pay_dates_template(year=y)
            print(f"\n>> Plantilla generada: '{tpl_path}'. Complétela y luego seleccione la opción [1].")

        else:
            print("Opción inválida. Ingrese 1, 2 o 3.")

def prompt_logo() -> Optional[str]:
    print("\n--- PASO 4: PERSONALIZACIÓN VISUAL ---")
    while True:
        desea_logo = input("¿Desea incluir un logo en el encabezado del Excel? (s/n) [Default 'n']: ").strip().lower()
        if desea_logo in ("n", "no", ""):
            return None
        elif desea_logo in ("s", "si", "sí", "y", "yes"):
            while True:
                logo_path = input("Ingrese la ruta o nombre del archivo de imagen (ej. logo.png): ").strip()
                # Quitar comillas si el usuario copió la ruta desde Windows Explorer
                logo_path = logo_path.replace('"', '').replace("'", "")
                if os.path.exists(logo_path):
                    return logo_path
                print(f"Error: No se encontró el archivo '{logo_path}'. Intente nuevamente.")
        else:
            print("Opción inválida. Responda 's' o 'n'.")

def run():
    print("==================================================")
    print("      LAHC PAYROLL CALENDAR BUILDER (V1)         ")
    print("==================================================")

    client_name = prompt_client_name()
    country = prompt_country()
    selected_processes = prompt_processes()
    pay_dates = prompt_pay_dates()
    logo_path = prompt_logo()

    all_events = []
    for proc in selected_processes:
        events = generate_process_calendar(
            country=country,
            process_type=proc,
            pay_dates=pay_dates
        )
        all_events.extend(events)

    periods = sorted(list({d.strftime("%Y-%m") for d in pay_dates}))
    if len(periods) == 1:
        period_suffix = periods[0]
    else:
        years = sorted(list({d.year for d in pay_dates}))
        period_suffix = "-".join(map(str, years))

    safe_client = sanitize_filename(client_name)
    filename = f"Payroll_Calendar_{safe_client}_{country}_{period_suffix}.xlsx"

    export_calendar_to_excel(
        events=all_events,
        country=country,
        client_name=client_name,
        output_path=filename,
        logo_path=logo_path
    )

    print("\n==================================================")
    print(" ¡CALENDARIO GENERADO CON ÉXITO!")
    print(f" Archivo de salida: {filename}")
    print(f" Cliente: {client_name}")
    print(f" Periodos incluidos: {', '.join(periods)}")
    print(f" Logo incluido: {'Sí' if logo_path else 'No'}")
    print(f" Total eventos calculados: {len(all_events)}")
    print("==================================================")

if __name__ == "__main__":
    run()