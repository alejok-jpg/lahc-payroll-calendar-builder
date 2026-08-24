import os
import re
from datetime import datetime, date, timedelta
from typing import Dict, List
import streamlit as st

from countries import SUPPORTED_COUNTRIES_INFO
from processes import ProcessType
from generator import generate_process_calendar, generate_termination_calendar_from_cutoffs
from exports import export_multiprocess_calendar_to_excel
from loaders import generate_multiprocess_template, load_multiprocess_pay_dates_from_excel

st.set_page_config(page_title="LAHC Payroll Calendar Builder", page_icon="📅", layout="wide")

st.title("📅 LAHC Payroll Calendar Builder")
st.markdown("Generador corporativo de calendarios operativos y Master Schedule de nómina.")

# Sidebar
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
client_name = st.text_input("Nombre del Cliente:", value="CLIENTE_DEMO").strip()

# Sección 2: Configuración de Fechas
st.subheader("2. Configuración de Fechas por Proceso")

process_events: Dict[str, List[Dict]] = {}
all_collected_dates: List[date] = []

if not selected_processes:
    st.warning("Selecciona al menos un proceso en el panel lateral.")
else:
    proc_tabs = st.tabs([p.name for p in selected_processes])

    for idx, proc in enumerate(selected_processes):
        with proc_tabs[idx]:
            if proc == ProcessType.TERMINATION:
                st.markdown("### ⚙️ Configuración de Bajas (Cálculo desde TERMINATION REQUEST / Cut-Off)")
                
                term_mode = st.radio(
                    "Modalidad para Bajas:",
                    ["📅 Seleccionar Días de la Semana (Cálculo Automático)", "✍️ Ingreso Manual de Fechas de Corte"],
                    key="term_mode_radio"
                )

                if term_mode == "📅 Seleccionar Días de la Semana (Cálculo Automático)":
                    col_days, col_range = st.columns(2)
                    with col_days:
                        st.markdown("**Días de la semana en que inicia el proceso:**")
                        d_lunes = st.checkbox("Lunes (Mon)", value=False)
                        d_martes = st.checkbox("Martes (Tue)", value=True)
                        d_miercoles = st.checkbox("Miércoles (Wed)", value=False)
                        d_jueves = st.checkbox("Jueves (Thu)", value=True)
                        d_viernes = st.checkbox("Viernes (Fri)", value=False)

                    selected_weekdays = []
                    if d_lunes: selected_weekdays.append(0)
                    if d_martes: selected_weekdays.append(1)
                    if d_miercoles: selected_weekdays.append(2)
                    if d_jueves: selected_weekdays.append(3)
                    if d_viernes: selected_weekdays.append(4)

                    with col_range:
                        st.markdown("**Rango de fechas a proyectar:**")
                        start_d = st.date_input("Fecha Inicio", value=date(2027, 1, 1))
                        end_d = st.date_input("Fecha Fin", value=date(2027, 1, 31))

                    if selected_weekdays and start_d <= end_d:
                        cutoff_dates = []
                        curr = start_d
                        while curr <= end_d:
                            if curr.weekday() in selected_weekdays:
                                cutoff_dates.append(curr)
                            curr += timedelta(days=1)

                        events = generate_termination_calendar_from_cutoffs(selected_country, cutoff_dates)
                        process_events[proc.name] = events
                        all_collected_dates.extend(cutoff_dates)
                        st.success(f"✓ Se generaron {len(cutoff_dates)} ciclos de baja proyectados.")
                    else:
                        st.warning("Selecciona al menos un día de la semana y un rango de fechas válido.")

                else:
                    num_fechas = st.number_input("Cantidad de fechas de corte a ingresar", min_value=1, max_value=50, value=2)
                    cols = st.columns(min(int(num_fechas), 4))
                    custom_cutoffs = []
                    for i in range(int(num_fechas)):
                        with cols[i % 4]:
                            cd = st.date_input(f"Corte #{i+1}", value=date(2027, 1, (i+1)*5), key=f"cut_{i}")
                            custom_cutoffs.append(cd)
                    
                    events = generate_termination_calendar_from_cutoffs(selected_country, custom_cutoffs)
                    process_events[proc.name] = events
                    all_collected_dates.extend(custom_cutoffs)

            else:
                st.markdown(f"**Carga de Fechas de Pago (Pay Days) para {proc.name}**")
                num_fechas = st.number_input(
                    f"Cantidad de periodos ({proc.name})",
                    min_value=1,
                    max_value=24,
                    value=2 if proc == ProcessType.MONTHLY else 1,
                    key=f"num_{proc.name}"
                )
                cols = st.columns(min(int(num_fechas), 4))
                dates_list = []
                for i in range(int(num_fechas)):
                    with cols[i % 4]:
                        d = st.date_input(
                            f"{proc.name} #{i+1}",
                            value=date(2027, ((i % 12) + 1), 28 if proc == ProcessType.MONTHLY else 15),
                            key=f"date_{proc.name}_{i}"
                        )
                        dates_list.append(d)
                
                sorted_p_dates = sorted(list(set(dates_list)))
                events = generate_process_calendar(selected_country, proc, sorted_p_dates)
                process_events[proc.name] = events
                all_collected_dates.extend(sorted_p_dates)
                st.caption(f"Fechas registradas: {', '.join([d.strftime('%d/%m/%Y') for d in sorted_p_dates])}")

# Sección 3: Logo
st.subheader("3. Personalización Visual (Logo)")
quiere_logo = st.radio("¿Desea incluir un logo en el encabezado del archivo Excel?", ["No", "Sí"], horizontal=True)
uploaded_logo = None
if quiere_logo == "Sí":
    uploaded_logo = st.file_uploader("Subí el logo (.png o .jpg)", type=["png", "jpg", "jpeg"])
    if uploaded_logo:
        st.image(uploaded_logo, caption="Vista previa", width=180)

# Sección 4: Generación
st.subheader("4. Generación del Calendario")

if st.button("🚀 Generar Calendario Operativo", type="primary"):
    if not client_name:
        st.error("Debes ingresar el nombre del cliente.")
    elif not selected_processes:
        st.error("Debes seleccionar al menos un proceso.")
    elif not process_events:
        st.error("No hay eventos configurados para generar.")
    else:
        try:
            temp_logo_path = None
            if quiere_logo == "Sí" and uploaded_logo:
                temp_logo_path = f"temp_{uploaded_logo.name}"
                with open(temp_logo_path, "wb") as f:
                    f.write(uploaded_logo.getbuffer())

            years = sorted(list({d.year for d in all_collected_dates}))
            year_str = "-".join(map(str, years)) if years else "2027"
            clean_client = re.sub(r'[\\/*?:"<>| ]', '_', client_name.strip())
            out_filename = f"Payroll_Calendar_{clean_client}_{selected_country}_{year_str}.xlsx"

            export_multiprocess_calendar_to_excel(
                events_by_process=process_events,
                country=selected_country,
                client_name=client_name,
                output_path=out_filename,
                logo_path=temp_logo_path
            )

            if temp_logo_path and os.path.exists(temp_logo_path):
                os.remove(temp_logo_path)

            with open(out_filename, "rb") as f:
                st.success("¡Calendario multiproceso con MASTER VIEW generado exitosamente!")
                st.download_button(
                    label=f"📥 Descargar {out_filename}",
                    data=f.read(),
                    file_name=out_filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"Error durante la generación: {e}")