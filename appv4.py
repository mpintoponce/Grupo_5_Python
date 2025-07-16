import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from datetime import datetime

# === Generar FECHA PLAN actual ===
fecha_actual = datetime.today()
numero_semana = fecha_actual.isocalendar().week
anio_dos_digitos = fecha_actual.strftime('%y')
fecha_plan = f"MINS{numero_semana}{anio_dos_digitos}"

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Dashboard OTs",
    page_icon="🔹",
    layout="wide",
    initial_sidebar_state="expanded"
)
img_url = "https://raw.githubusercontent.com/Articjm/PROYECTO_G5/main/CAMION_TR.jpg"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{img_url}");
        background-attachment: fixed;
        background-size: cover;
        background-position: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔹 Dashboard de Cumplimiento de OTs")
st.markdown("Visualización de KPIs semanales y mensuales de mantenimiento mina")

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    archivo = "CUMPLIMIENTO_PLAN.xlsm"
    df_plan = pd.read_excel(archivo, sheet_name='IW38 PLAN SEMANAL')
    df_semana = pd.read_excel(archivo, sheet_name='IW38 SEMANA CAL')
    df_bl = pd.read_excel(archivo, sheet_name='BL MENSUALOT')
    df_cm = pd.read_excel(archivo, sheet_name='CMENSUAL')
    df_tendencia = pd.read_excel(archivo, sheet_name='RESUMEN ANUAL')
    return df_plan, df_semana, df_bl, df_cm, df_tendencia

df_plan, df_semana, df_bl, df_cm, df_tendencia = load_data()

# --- PARÁMETROS DE FECHA ---
fecha_actual = datetime.today()
numero_semana = fecha_actual.isocalendar().week
anio_dos_digitos = fecha_actual.strftime('%y')
fecha_plan = f"MINS{numero_semana}{anio_dos_digitos}"

# --- CLASIFICACIÓN DE ESTADOS ---
def clasificar_estado_plan(fila):
    if fila['Orden'] > 0:
        if str(fila['Status del sistema']).startswith(('CTE', 'CER')):
            return "CERRADO"
        elif str(fila['Status de usuario']).startswith("REPR"):
            return "REPROGRAMADO"
        elif fila['Reprogramación'] != fecha_plan:
            return "REPROGRAMADO"
        else:
            return "ABIERTO"
    return ""

df_plan['ESTADO OTS'] = df_plan.apply(clasificar_estado_plan, axis=1)
df_plan['FLOTA'] = df_plan['Emplazamiento']

ordenes_planificadas = df_plan['Orden'].dropna().astype(int).tolist()
df_semana['Orden'] = pd.to_numeric(df_semana['Orden'], errors='coerce')

def tipo_plan(orden):
    if pd.notnull(orden) and orden > 0:
        return "PROGRAMADO" if int(orden) in ordenes_planificadas else "CORRECTIVO"
    return ""

df_semana['TIPO PLAN'] = df_semana['Orden'].apply(tipo_plan)


def estado_semana(fila):
    status = str(fila.get('Status del sistema', ''))[:3]
    orden = fila.get('Orden')
    if pd.notnull(orden) and orden > 0:
        if status in ['CTE', 'CER']:
            return 'CERRADO'
        elif status == 'REP':
            return 'REPROGRAMADO'
        else:
            return 'ABIERTO'
    return ""

df_semana['ESTADO OTS'] = df_semana.apply(estado_semana, axis=1)
df_semana['FLOTA'] = df_semana['Emplazamiento']

# Mensual
def calcular_estado(status):
    status = str(status).strip().upper()
    if status.startswith('CTE'):
        return 'CERRADO'
    elif status.startswith('REP'):
        return 'REPROGRAMADO'
    else:
        return 'ABIERTO'
    
def estado_simple_flotas(fila):
    status = str(fila['Status del sistema']).strip().upper()
    if status.startswith('CTE') or status.startswith('CER'):
        return 'CERRADO'
    else:
        return 'ABIERTO'
    
# === FUNCIONES DE CLASIFICACIÓN DE ESTADO ===
def calcular_estado_ots(fila):
    if fila['Orden'] > 0:
        if str(fila['Status del sistema']).startswith(("CTE", "CER")):
            return "CERRADO"
        elif str(fila['Status de usuario']).startswith("REPR"):
            return "REPROGRAMADO"
        elif fila['Reprogramación'] != fecha_plan:
            return "REPROGRAMADO"
        else:
            return "ABIERTO"
    return ""

# === CLASIFICACIÓN PARA ANÁLISIS DE FLOTAS ===
def clasificar_estado_flotas(fila):
    if fila['Orden'] > 0:
        if str(fila['Status del sistema']).startswith(("CTE", "CER")):
            return "CERRADO"
        elif str(fila['Status de usuario']).startswith("REPR"):
            return "REPROGRAMADO"
        elif fila['Reprogramación'] != fecha_plan:
            return "REPROGRAMADO"
        else:
            return "ABIERTO"
    return ""

df_bl['ESTADO'] = df_bl['Status del sistema'].apply(calcular_estado)
df_bl['FLOTA'] = df_bl['Emplazamiento']
df_cm['ESTADO'] = df_cm['Status del sistema'].apply(calcular_estado)
df_plan['ESTADO_FLOTA'] = df_plan.apply(clasificar_estado_flotas, axis=1)
df_cm['FLOTA'] = df_cm['Emplazamiento']
df_plan['ESTADO_FLOTA'] = df_plan.apply(estado_simple_flotas, axis=1)



# --- COLORES Y COLUMNAS ---
colores = {'ABIERTO': '#FF6666', 'CERRADO': '#6699FF', 'REPROGRAMADO': '#FFEB66'}
columnas = ['CERRADO', 'REPROGRAMADO', 'ABIERTO']

# --- MENÚ PRINCIPAL ---
submenu = st.sidebar.selectbox("Selecciona vista", [
    "Análisis Semanal",
    "Análisis Mensual",
    "Componentes y Backlogs Programados",
    "Análisis por Flota",
    "Tendencia Anual"
])

# === ANÁLISIS SEMANAL ===
if submenu == "Análisis Semanal":
    st.subheader("📅 Análisis del Plan Semanal")

    col1, col2 = st.columns(2)

    with col1:
        conteo_total = df_plan['ESTADO OTS'].value_counts().reindex(columnas, fill_value=0).reset_index()
        conteo_total.columns = ['ESTADO', 'CANTIDAD']
        fig = px.pie(conteo_total, values='CANTIDAD', names='ESTADO',
                     color='ESTADO', color_discrete_map=colores,
                     title="Cumplimiento del Plan Semanal")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df_correctivo = df_semana[df_semana['TIPO PLAN'] == 'CORRECTIVO']
        conteo_correctivo = df_correctivo['ESTADO OTS'].value_counts().reindex(columnas, fill_value=0).reset_index()
        conteo_correctivo.columns = ['ESTADO', 'CANTIDAD']
        fig = px.pie(conteo_correctivo, values='CANTIDAD', names='ESTADO',
                     color='ESTADO', color_discrete_map=colores,
                     title="OTs Correctivas - Semana")
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        conteo_flotas = df_plan.groupby(['FLOTA', 'ESTADO OTS']).size().reset_index(name='CANTIDAD')
        fig = px.bar(conteo_flotas, x='FLOTA', y='CANTIDAD', color='ESTADO OTS',
                     category_orders={"ESTADO OTS": columnas},
                     color_discrete_map=colores,
                     title="Plan Semanal por Flota")
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        conteo_correctivo_flotas = df_correctivo.groupby(['FLOTA', 'ESTADO OTS']).size().reset_index(name='CANTIDAD')
        fig = px.bar(conteo_correctivo_flotas, x='FLOTA', y='CANTIDAD', color='ESTADO OTS',
                     category_orders={"ESTADO OTS": columnas},
                     color_discrete_map=colores,
                     title="Correctivas por Flota")
        st.plotly_chart(fig, use_container_width=True)

# === ANÁLISIS MENSUAL ===
elif submenu == "Análisis Mensual":
    st.subheader("📆 Análisis del Cumplimiento Mensual")

    col1, col2 = st.columns(2)

    with col1:
        conteo_bl = df_bl['ESTADO'].value_counts().reindex(columnas, fill_value=0).reset_index()
        conteo_bl.columns = ['ESTADO', 'CANTIDAD']
        fig = px.pie(conteo_bl, values='CANTIDAD', names='ESTADO',
                     color='ESTADO', color_discrete_map=colores,
                     title="Backlog Mensual")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        conteo_cm = df_cm['ESTADO'].value_counts().reindex(columnas, fill_value=0).reset_index()
        conteo_cm.columns = ['ESTADO', 'CANTIDAD']
        fig = px.pie(conteo_cm, values='CANTIDAD', names='ESTADO',
                     color='ESTADO', color_discrete_map=colores,
                     title="Correctivos Componentes Mensual")
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        conteo_flotas_bl = df_bl.groupby(['FLOTA', 'ESTADO']).size().reset_index(name='CANTIDAD')
        fig = px.bar(conteo_flotas_bl, x='FLOTA', y='CANTIDAD', color='ESTADO',
                     category_orders={"ESTADO": columnas},
                     color_discrete_map=colores,
                     title="Backlog por Flota")
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        conteo_flotas_cm = df_cm.groupby(['FLOTA', 'ESTADO']).size().reset_index(name='CANTIDAD')
        fig = px.bar(conteo_flotas_cm, x='FLOTA', y='CANTIDAD', color='ESTADO',
                     category_orders={"ESTADO": columnas},
                     color_discrete_map=colores,
                     title="Correctivos por Flota")
        st.plotly_chart(fig, use_container_width=True)

elif submenu == "Componentes y Backlogs Programados":
    st.subheader("🧩 Análisis de Componentes y Backlogs Programados")

    # Clasificación por texto breve
    df_plan['ESTADO OTS'] = df_plan.apply(calcular_estado_ots, axis=1)

    def calcular_tipo_componente(fila):
        if fila['Orden'] > 0:
            if str(fila['Texto breve']).startswith(("CO_", "CC_")):
                return "COMPONENTE"
            elif str(fila['Texto breve']).startswith("BL"):
                return "BACKLOG"
        return ""

    df_plan['TIPO ELEMENTO'] = df_plan.apply(calcular_tipo_componente, axis=1)

    df_backlog = df_plan[df_plan['TIPO ELEMENTO'] == "BACKLOG"]
    df_comp = df_plan[df_plan['TIPO ELEMENTO'] == "COMPONENTE"]

    orden_flotas = ['AUXILIAR', 'ACARREO', 'PERFORACIO', 'CARGUIO', 'SOPORTE']
    columnas = ['CERRADO', 'REPROGRAMADO', 'ABIERTO']

    # Conteo
    comp_estado_total = df_comp['ESTADO OTS'].value_counts().reindex(columnas, fill_value=0).reset_index()
    comp_estado_total.columns = ['ESTADO', 'CANTIDAD']

    backlog_estado_total = df_backlog['ESTADO OTS'].value_counts().reindex(columnas, fill_value=0).reset_index()
    backlog_estado_total.columns = ['ESTADO', 'CANTIDAD']

    # Conteo por flota
    comp_flotas = df_comp.groupby(['FLOTA', 'ESTADO OTS']).size().unstack(fill_value=0).reindex(orden_flotas).fillna(0)
    backlog_flotas = df_backlog.groupby(['FLOTA', 'ESTADO OTS']).size().unstack(fill_value=0).reindex(orden_flotas).fillna(0)

    columnas_presentes_comp = [col for col in columnas if col in comp_flotas.columns]
    columnas_presentes_back = [col for col in columnas if col in backlog_flotas.columns]

    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(comp_estado_total, values='CANTIDAD', names='ESTADO',
                     color='ESTADO', color_discrete_map=colores,
                     title="Componentes Programados")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.pie(backlog_estado_total, values='CANTIDAD', names='ESTADO',
                     color='ESTADO', color_discrete_map=colores,
                     title="Backlogs Programados")
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        fig = px.bar(comp_flotas[columnas_presentes_comp].reset_index().melt(id_vars='FLOTA'),
                     x='FLOTA', y='value', color='ESTADO OTS',
                     category_orders={"ESTADO OTS": columnas},
                     color_discrete_map=colores,
                     title="Componentes por Flota")
        fig.update_layout(barmode='stack')
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        fig = px.bar(backlog_flotas[columnas_presentes_back].reset_index().melt(id_vars='FLOTA'),
                     x='FLOTA', y='value', color='ESTADO OTS',
                     category_orders={"ESTADO OTS": columnas},
                     color_discrete_map=colores,
                     title="Backlogs por Flota")
        fig.update_layout(barmode='stack')
        st.plotly_chart(fig, use_container_width=True)

elif submenu == "Análisis por Flota":
    st.subheader("📊 Distribución del Cumplimiento por Flota")

    conteo_flotas = df_plan.groupby(['FLOTA', 'ESTADO_FLOTA']).size().unstack(fill_value=0)
    flotas_existentes = conteo_flotas.index[conteo_flotas.sum(axis=1) > 0]

    cols = 3
    rows = (len(flotas_existentes) + cols - 1) // cols

    for row in range(rows):
        cols_stream = st.columns(cols)
        for i in range(cols):
            idx = row * cols + i
            if idx < len(flotas_existentes):
                flota = flotas_existentes[idx]
                data = conteo_flotas.loc[flota]
                data = data[data > 0]
                df_flota = data.reset_index()
                df_flota.columns = ['ESTADO OTS', 'CANTIDAD']

                fig = px.pie(
                    df_flota,
                    values='CANTIDAD',
                    names='ESTADO OTS',
                    color='ESTADO OTS',
                    color_discrete_map=colores,
                    title=f'FLOTA: {flota}'
                )
                fig.update_traces(textinfo='percent+label', textfont_size=10)
                fig.update_layout(
                    margin=dict(t=40, b=20, l=20, r=20),
                    showlegend=True
                )
                cols_stream[i].plotly_chart(fig, use_container_width=True)

elif submenu == "Tendencia Anual":
    st.subheader("📈 Tendencia Anual de Cumplimiento")

    df_tendencia['Cumplimiento (%)'] = df_tendencia['Promedio Cumplimiento'] * 100

    fig_bar = px.bar(
        df_tendencia,
        x='Semana',
        y='Cumplimiento (%)',
        title='Tendencia Anual de Cumplimiento',
        text='Cumplimiento (%)',
        labels={'Semana': 'Periodo', 'Cumplimiento (%)': '% Cumplimiento'},
        color_discrete_sequence=['#6699FF']
    )

    fig_bar.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside',
        name='Cumplimiento Semanal'
    )

    fig_bar.add_shape(
        type='line',
        x0=-0.5,
        x1=len(df_tendencia['Semana']) - 0.5,
        y0=80,
        y1=80,
        line=dict(color='red', width=2, dash='dash'),
        xref='x',
        yref='y'
    )

    fig_bar.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='red', width=2, dash='dash'),
        name='Meta del 80%'
    ))

    fig_bar.update_layout(
        font=dict(color='white'),
        title_font=dict(size=20),
        xaxis=dict(tickangle=-45),
        yaxis=dict(title='% Cumplimiento', range=[0, 110]),
        legend=dict(
            font=dict(size=12),
            bgcolor='black',
            bordercolor='gray',
            borderwidth=1
        ),
        paper_bgcolor='black',
        plot_bgcolor='black',
        margin=dict(t=80)
    )

    st.plotly_chart(fig_bar, use_container_width=True)