import os
import re
from datetime import datetime, date
from typing import Dict, List
import streamlit as st

from countries import SUPPORTED_COUNTRIES_INFO
from processes import ProcessType
from generator import generate_process_calendar
from exports import export_multiprocess_calendar_to_excel
from loaders import generate_multiprocess_template, load_multiprocess_pay_dates_from_excel

st.set_page_config(page_title="LAHC Payroll Calendar Builder", page_icon="📅", layout="wide")

st.title("📅 LAHC Payroll Calendar Builder")
st.markdown("Generador corporativo multicliente y multiproceso de calendarios operativos de nómina.")

# Sidebar - Configuración
st.sidebar.header("⚙️ Configuración General")

country_options = list(SUPPORTED_COUNTRIES_INFO.keys())
selected_country = st.sidebar.selectbox(
    "País",
    options=country_options,
    format_func=lambda c: f"{c} - {SUPPORTED_COUNTRIES_INFO[c]['name']}"
)

st.sidebar.subheader("Selección de Procesos")
process_list = list(ProcessType)
selected_processes: List[ProcessType] = []

select_all = st.sidebar.checkbox("Seleccionar todos los procesos", value=False)
if select_all:
    selected_processes = process_list
else:
    for p in process_list:
        if st.sidebar.checkbox(p.name, value=(p == ProcessType.MONTHLY)):
            selected_processes.append(p)

# Sección 1: Cliente
st.subheader("1. Identificación del Cliente")
client_name = st.text_input("Nombre del Cliente (se incluirá en el Excel y nombre de archivo):", value="CLIENTE_DEMO").strip()

# Sección 2: Fechas de Pago por Proceso
st.subheader("2. Carga de Fechas de Pago (Pay Days por Proceso)")

if not selected_processes:
    st.warning("Selecciona al menos un proceso en el menú lateral para configurar sus fechas.")
    process_pay_dates = {}
else:
    mode = st.radio("Método de Carga:", ["✍️ Carga Manual por Proceso", "📂 Carga Masiva vía Excel", "📥 Descargar Plantilla Multiproceso"], horizontal=True)

    process_pay_dates: Dict[str, List[date]] = {}

    if mode == "✍️ Carga Manual por Proceso":
        proc_tabs = st.tabs([p.name for p in selected_processes])
        for idx, p in enumerate(selected_processes):
            with proc_tabs[idx]:
                st.markdown(f"**Fechas de pago para: {p.name}**")
                num_fechas = st.number_input(
                    f"Cantidad de periodos a ingresar ({p.name})",
                    min_value=1,
                    max_value=24,
                    value=2 if p == ProcessType.MONTHLY else 1,
                    key=f"num_{p.name}"
                )
                cols = st.columns(min(int(num_fechas), 4))
                dates_list = []
                for i in range(int(num_fechas)):
                    with cols[i % 4]:
                        d = st.date_input(
                            f"{p.name} #{i+1}",
                            value=date(2027, ((i % 12) + 1), 28 if p == ProcessType.MONTHLY else 15),
                            key=f"date_{p.name}_{i}"
                        )
                        dates_list.append(d)
                process_pay_dates[p.name] = sorted(list(set(dates_list)))
                st.caption(f"Fechas registradas: {', '.join([d.strftime('%d/%m/%Y') for d in process_pay_dates[p.name]])}")

    elif mode == "📂 Carga Masiva vía Excel":
        uploaded_file = st.file_uploader("Subí tu archivo Excel con una pestaña por proceso", type=["xlsx", "xls"])
        if uploaded_file:
            try:
                loaded_dict = load_multiprocess_pay_dates_from_excel(uploaded_file)
                for p in selected_processes:
                    if p.name in loaded_dict:
                        process_pay_dates[p.name] = loaded_dict[p.name]
                        st.success(f"✓ {p.name}: {len(process_pay_dates[p.name])} fechas cargadas.")
                    else:
                        st.warning(f"⚠ No se encontró la pestaña '{p.name}' en el Excel.")
            except Exception as e:
                st.error(f"Error al procesar el Excel: {e}")

    else:
        tpl_year = st.number_input("Año de la plantilla", min_value=2024, max_value=2035, value=2027)
        if st.button("Generar Plantilla"):
            tpl_path = generate_multiprocess_template("template_temp.xlsx", year=tpl_year)
            with open(tpl_path, "rb") as f:
                st.download_button(
                    label="⬇️ Descargar Plantilla Excel Multiproceso",
                    data=f.read(),
                    file_name=f"Template_PayDates_{tpl_year}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

# Sección 3: Logo
st.subheader("3. Personalización Visual (Logo)")
quiere_logo = st.radio("¿Desea incluir un logo en el encabezado del archivo Excel?", ["No", "Sí"], horizontal=True)

uploaded_logo = None
if quiere_logo == "Sí":
    uploaded_logo = st.file_uploader("Seleccione o arrastre la imagen del logo (.png o .jpg)", type=["png", "jpg", "jpeg"])
    if uploaded_logo:
        st.image(uploaded_logo, caption="Vista previa del logo a insertar", width=200)

# Sección 4: Generación y Descarga
st.subheader("4. Generación del Calendario")

if st.button("🚀 Generar Calendario Operativo", type="primary"):
    if not client_name:
        st.error("Debes ingresar el nombre del cliente.")
    elif not selected_processes:
        st.error("Debes seleccionar al menos un proceso.")
    elif not process_pay_dates or not any(process_pay_dates.values()):
        st.error("Debes configurar al menos una fecha de pago para los procesos seleccionados.")
    else:
        try:
            events_by_process = {}
            all_collected_dates = []

            for proc in selected_processes:
                dates = process_pay_dates.get(proc.name, [])
                if dates:
                    events = generate_process_calendar(
                        country=selected_country,
                        process_type=proc,
                        pay_dates=dates
                    )
                    events_by_process[proc.name] = events
                    all_collected_dates.extend(dates)

            # Manejo del archivo temporal del logo
            temp_logo_path = None
            if quiere_logo == "Sí" and uploaded_logo:
                temp_logo_path = f"temp_logo_{uploaded_logo.name}"
                with open(temp_logo_path, "wb") as f:
                    f.write(uploaded_logo.getbuffer())

            # Naming convention: Payroll_Calendar_<CLIENTE>_<PAIS>_<AÑO/PERIODO>.xlsx
            years = sorted(list({d.year for d in all_collected_dates}))
            year_str = "-".join(map(str, years)) if years else "2027"
            clean_client = re.sub(r'[\\/*?:"<>| ]', '_', client_name.strip())
            out_filename = f"Payroll_Calendar_{clean_client}_{selected_country}_{year_str}.xlsx"

            export_multiprocess_calendar_to_excel(
                events_by_process=events_by_process,
                country=selected_country,
                client_name=client_name,
                output_path=out_filename,
                logo_path=temp_logo_path
            )

            if temp_logo_path and os.path.exists(temp_logo_path):
                os.remove(temp_logo_path)

            with open(out_filename, "rb") as f:
                st.success("¡Calendario multiproceso generado exitosamente!")
                st.download_button(
                    label=f"📥 Descargar {out_filename}",
                    data=f.read(),
                    file_name=out_filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        except Exception as e:
            st.error(f"Ocurrió un error durante la generación: {e}")