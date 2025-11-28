%%writefile app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
import numpy as np
import uuid
import datetime
import random

# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS (DISEÑO PITCH PRO - ULTIMATE)
# ==============================================================================
st.set_page_config(
    page_title="KUALI",
    page_icon="✈️",
    layout="wide"
)

# --- CSS MAESTRO: TARJETAS, FUENTES Y TOOLTIPS INTELIGENTES ---
st.markdown("""
    <style>
    /* 1. FONDO GENERAL */
    .stApp {
        background-color: #F4F6F7;
    }

    /* 2. TIPOGRAFÍA GLOBAL (NEGRO POR DEFECTO) */
    html, body, [class*="css"], .stMarkdown, .stText, p, li, span, div {
        font-size: 24px !important;
        color: #000000 !important;
        font-family: 'Arial', sans-serif !important;
    }

    /* 3. TÍTULO PRINCIPAL */
    .main-title {
        font-size: 140px !important;
        font-weight: 900 !important;
        color: #0A3069 !important;
        text-align: center;
        text-transform: uppercase;
        text-shadow: 5px 5px 0px #FFFFFF, 7px 7px 0px #BDC3C7;
        margin-bottom: 0px !important;
        line-height: 1 !important;
        padding-top: 20px;
    }

    /* 4. SLOGAN */
    .main-slogan {
        font-size: 48px !important;
        color: #154360 !important;
        text-align: center;
        font-weight: 700 !important;
        font-style: italic;
        margin-top: 10px !important;
        margin-bottom: 40px !important;
        border-bottom: 5px solid #E67E22;
    }

    /* 5. TÍTULOS DE SECCIONES */
    h1, h2, h3 {
        color: #154360 !important;
        font-weight: 800 !important;
        padding-top: 10px;
    }

    /* 6. TARJETAS BLANCAS */
    div.block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    /* 7. ESTILO DE TABLA */
    div[data-testid="stTable"] {
        background-color: #FFFFFF !important;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #BDC3C7;
    }
    table { width: 100% !important; border-collapse: collapse !important; }
    thead tr th {
        background-color: #FFFFFF !important;
        color: #0A3069 !important;
        font-size: 26px !important;
        font-weight: 900 !important;
        text-align: center !important;
        padding: 15px !important;
        border-bottom: 4px solid #0A3069 !important;
    }
    tbody tr td {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-size: 24px !important;
        border-bottom: 2px solid #D5D8DC !important;
        font-weight: 600 !important;
        padding: 15px !important;
    }

    /* 8. PESTAÑAS */
    button[data-baseweb="tab"] {
        font-size: 28px !important;
        background-color: #E5E8E8 !important;
        color: #555555 !important;
        margin-right: 5px;
        border-radius: 10px 10px 0 0;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #0A3069 !important;
        border-top: 6px solid #0A3069 !important;
    }

    /* 9. ALERTAS */
    .stAlert {
        background-color: #FFFFFF !important;
        border-left: 10px solid #E67E22 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* 10. MÉTRICAS */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF !important;
        border: 1px solid #BDC3C7 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 15px !important;
        border-radius: 8px;
    }
    [data-testid="stMetricValue"] { color: #0A3069 !important; }

    /* 11. TOOLTIPS DE PYDECK (SOLUCIÓN DEFINITIVA COLOR NARANJA) */
    .deck-tooltip {
        background-color: #0A3069 !important;
        color: #FFA500 !important;
        font-family: 'Arial', sans-serif !important;
        font-size: 18px !important;
        border-radius: 8px !important;
        padding: 12px !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3) !important;
        border: 2px solid #FFA500 !important;
        z-index: 9999 !important;
    }
    /* FUERZA BRUTA: CUALQUIER COSA DENTRO DEL TOOLTIP SERÁ NARANJA */
    .deck-tooltip * {
        color: #FFA500 !important;
    }

    /* 12. TARJETAS HTML DE PILARES */
    .pilar-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        border-bottom: 5px solid #0A3069;
        height: 100%;
        transition: transform 0.3s ease;
    }
    .pilar-card:hover {
        transform: scale(1.05);
        background-color: #FDFEFE;
    }
    .pilar-icon { font-size: 60px; margin-bottom: 10px; }
    .pilar-title { font-size: 28px; font-weight: bold; color: #154360; margin-bottom: 5px; }
    .pilar-value { font-size: 36px; font-weight: 900; color: #E67E22; }
    .pilar-desc { font-size: 20px; color: #555; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 2. CONFIGURACIÓN GLOBAL DE GRÁFICAS
# ==============================================================================

def hex_to_rgba(hex_code, opacity):
    hex_code = hex_code.lstrip('#')
    return f"rgba({int(hex_code[0:2], 16)}, {int(hex_code[2:4], 16)}, {int(hex_code[4:6], 16)}, {opacity})"

def update_fig_layout(fig, height=None):
    fig.update_layout(
        template='plotly_white',
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#FFFFFF',
        font=dict(color='#000000', size=20, family="Arial"),
        margin=dict(l=20, r=20, t=60, b=20),
        height=height if height else 450,
        legend=dict(
            font=dict(color="#000000", size=20),
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#BDC3C7",
            borderwidth=1
        ),
        # Tooltip Plotly Inteligente
        hoverlabel=dict(
            bgcolor="#0A3069",
            font=dict(color="#FFFFFF", size=24),
            bordercolor="#E67E22"
        )
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#EBEDEF', showline=True, linewidth=2, linecolor='black', tickfont=dict(color='black', size=18))
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#EBEDEF', showline=True, linewidth=2, linecolor='black', tickfont=dict(color='black', size=18))
    return fig

# --- DATOS GLOBALES ---
kpi_inversion_inicial = 1200000
pe_paquetes_mensuales_c12 = 22

# --- FUNCIONES GENERADORAS ---

def crear_grafica_plataforma(nombre_plataforma, color_linea, volatilidad, nivel_precio):
    fechas = []
    precio_bajo = []
    precio_alto = []
    precio_prom = []
    curr = datetime.date(2025, 10, 10)
    end = datetime.date(2025, 11, 5)
    while curr <= end:
        fechas.append(curr)
        base = 22000 * nivel_precio
        factor = 1.0
        if curr.weekday() >= 4: factor = 1.15
        if curr.month == 11 and curr.day <= 2: factor = 1.85
        p_prom = int(base * factor)
        gap = int(p_prom * volatilidad)
        noise = random.uniform(0.95, 1.05)
        p_min = int((p_prom - gap) * noise)
        p_max = int((p_prom + gap) * noise)
        p_final = int(p_prom * noise)
        precio_bajo.append(p_min)
        precio_alto.append(p_max)
        precio_prom.append(p_final)
        curr += datetime.timedelta(days=1)

    fill_color = hex_to_rgba(color_linea, 0.2)

    # --- TOOLTIP COMPETENCIA ---
    tooltip_template = (
        "<b>PLATAFORMA: " + nombre_plataforma + "</b><br>" +
        "📅 Fecha: %{x|%d %b}<br>" +
        "💸 Precio: %{y:$,.0f}<br>" +
        "<br>" +
        "⚠️ <b>RIESGO:</b> El precio cambia por hora.<br>" +
        "📉 <b>CAUSA:</b> Algoritmo de Especulación.<br>" +
        "❌ <b>EFECTO:</b> Pagas más si hay mucha demanda.<extra></extra>"
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fechas, y=precio_alto, mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'))
    fig.add_trace(go.Scatter(
        x=fechas, y=precio_bajo, mode='lines', line=dict(width=0), fill='tonexty', fillcolor=fill_color, name=f'Volatilidad',
        hoverinfo='skip'
    ))
    fig.add_trace(go.Scatter(
        x=fechas, y=precio_prom, mode='lines+markers', line=dict(color=color_linea, width=4), marker=dict(size=8), name=f'Precio',
        hovertemplate=tooltip_template
    ))

    fig.update_layout(
        title=dict(text=f'<b>{nombre_plataforma}</b>', font=dict(size=24, color="#000000")),
        yaxis=dict(tickformat="$,.0f"),
        xaxis=dict(tickformat="%d %b"),
        showlegend=False
    )
    return update_fig_layout(fig, height=350)

def crear_grafica_kuali():
    fechas = []
    precio_bajo = []
    precio_alto = []
    precio_prom = []
    curr = datetime.date(2025, 10, 10)
    end = datetime.date(2025, 11, 5)
    while curr <= end:
        fechas.append(curr)
        base = 21500
        factor = 1.0
        if curr.month == 11 and curr.day <= 2: factor = 1.10
        elif curr.weekday() >= 4: factor = 1.05
        p_prom = int(base * factor)
        gap = 1500
        noise = random.uniform(0.99, 1.01)
        p_min = int((p_prom - gap) * noise)
        p_max = int((p_prom + gap) * noise)
        precio_bajo.append(p_min)
        precio_alto.append(p_max)
        precio_prom.append(p_prom)
        curr += datetime.timedelta(days=1)

    color_kuali = "#0A3069"
    fill_kuali = hex_to_rgba(color_kuali, 0.15)

    # --- TOOLTIP KUALI ---
    tooltip_kuali = (
        "<b>KUALI (NOSOTROS)</b><br>" +
        "📅 Fecha: %{x|%d %b}<br>" +
        "💰 Precio: %{y:$,.0f}<br>" +
        "<br>" +
        "✅ <b>GARANTÍA:</b> Precio Protegido y Fijo.<br>" +
        "🤖 <b>TECNOLOGÍA:</b> IA Anti-Bias bloquea aumentos.<br>" +
        "❤️ <b>BENEFICIO:</b> Tu presupuesto está seguro.<extra></extra>"
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fechas, y=precio_alto, mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'))
    fig.add_trace(go.Scatter(
        x=fechas, y=precio_bajo, mode='lines', line=dict(width=0), fill='tonexty', fillcolor=fill_kuali, name='Volatilidad Mínima',
        hoverinfo='skip'
    ))
    fig.add_trace(go.Scatter(
        x=fechas, y=precio_prom, mode='lines+markers', line=dict(color=color_kuali, width=6), marker=dict(size=12, symbol='square'), name='Precio KUALI',
        hovertemplate=tooltip_kuali
    ))

    fig.update_layout(
        title=dict(text='<b>KUALI</b>: Estabilidad Garantizada', font=dict(size=28, color="#000000")),
        yaxis=dict(title='Precio (MXN)', tickformat="$,.0f"),
        xaxis=dict(title='Fechas', tickformat="%d %b"),
        annotations=[
            dict(
                x='2025-11-01', y=precio_prom[22], xref="x", yref="y",
                text="<b>Sin abusos en Día de Muertos</b>",
                showarrow=True, arrowhead=2, ax=0, ay=-50,
                font=dict(color="#E67E22", size=24)
            )
        ]
    )
    return update_fig_layout(fig, height=500)

# --- DATAFRAMES ---
df_inversion_inicial = pd.DataFrame({
    'Concepto': ['Activos Fijos', 'Activos Intangibles (IA)', 'Trámites', 'Capital Trabajo (Reserva)'],
    'Monto Total (MXN)': [140500, 695000, 56500, 308000],
    'Justificación': ['Equipo IA', 'Algoritmo KUALI-Δ', 'Legal/Marca', 'Fondo Reserva Leasing']
})
df_proyeccion_ingresos = pd.DataFrame({
    'Concepto': ['Margen Paquetes', 'Comisión Leasing', 'Servicios Tech'],
    'Año 1': [9500000, 950000, 480000],
    'Año 2': [12000000, 1200000, 720000],
    'Año 3': [16200000, 1620000, 950000]
})
data_competencia_mercado = {
    'Plataforma': ['KUALI', 'Despegar', 'PriceTravel', 'Booking.com', 'Expedia Group'],
    'Paquetes Ofrecidos': [
        'Vuelo + Hotel + Traslado + Leasing + Experiencias',
        'Vuelo + Hotel + MSI',
        'Vuelo + Hotel + Todo Incluido',
        'Alojamiento + Desayuno',
        'Vuelo + Hotel + Autos'
    ],
    'Comisión': ['Única (10-15%)', 'Markup', 'Margen + Comisión', '10-25%', '10-30%']
}
df_precios_competencia = pd.DataFrame(data_competencia_mercado)

# ==============================================================================
# 3. INTERFAZ PRINCIPAL
# ==============================================================================

st.markdown('<h1 class="main-title">KUALI</h1>', unsafe_allow_html=True)
st.markdown('<p class="main-slogan">Transparencia que viaja contigo</p>', unsafe_allow_html=True)

# PESTAÑAS
tab1, tab2, tab3 = st.tabs([
    "⚙️ Producto y Operación",
    "📈 Estudio Financiero",
    "🎯 Estudio de Mercado"
])

# ==============================================================================
# PESTAÑA 1: PRODUCTO
# ==============================================================================
with tab1:
    # --- 1. MAPA (TOOLTIPS TOTALMENTE NARANJAS) ---
    st.markdown("### 1. Cobertura Operativa: Conectando a México")
    st.caption("Pasa el mouse sobre las rutas para ver el perfil familiar por región.")

    rutas_data = [
        {"origen": "Monterrey", "source": [-100.3161, 25.6866], "target": [-99.1332, 19.4326], "color": [255, 0, 128],
         "alta": "+45% (Navidad/Verano)", "normal": "Compras & Ocio", "segmento": "20% Familias Norte (Ticket Alto)"},

        {"origen": "Guadalajara", "source": [-103.3496, 20.6597], "target": [-99.1332, 19.4326], "color": [255, 165, 0],
         "alta": "+40% (Semana Santa)", "normal": "Cultural", "segmento": "18% Familias Tradicionales"},

        {"origen": "Mérida", "source": [-89.5926, 20.9674], "target": [-99.1332, 19.4326], "color": [0, 255, 0],
         "alta": "+25% (Vacaciones)", "normal": "Visita Familiar", "segmento": "12% Familias Multigeneracionales"},

        {"origen": "Cancún", "source": [-86.8515, 21.1619], "target": [-99.1332, 19.4326], "color": [0, 255, 255],
         "alta": "+60% (Todo el año)", "normal": "Conexión", "segmento": "25% Familias en Retorno/Conexión"},

        {"origen": "Puebla", "source": [-98.2063, 19.0414], "target": [-99.1332, 19.4326], "color": [138, 43, 226],
         "alta": "+30% (Puentes)", "normal": "Fin de Semana", "segmento": "10% Escapada Familiar Express"},

        {"origen": "Querétaro", "source": [-100.3899, 20.5888], "target": [-99.1332, 19.4326], "color": [255, 215, 0],
         "alta": "+35% (Verano)", "normal": "Recreativo", "segmento": "15% Familias Jóvenes con Niños"},
    ]
    df_rutas = pd.DataFrame(rutas_data)

    layer_arc = pdk.Layer(
        "ArcLayer",
        data=df_rutas,
        get_source_position="source",
        get_target_position="target",
        get_source_color="color",
        get_target_color=[14, 102, 85],
        get_width=15,
        get_tilt=15,
        pickable=True,
        auto_highlight=True,
    )

    # --- TOOLTIP NARANJA FORZADO CON !IMPORTANT EN CSS ---
    deck_tooltip = {
        "html": """
        <div style='font-family: Arial; line-height: 1.4;'>
            <b style='font-size: 1.3em;'>Ruta: {origen} ➡ CDMX</b><br/>
            <div style='border-bottom: 2px solid #FFA500; margin: 5px 0;'></div>
            <span>📈 T. Alta:</span> <b>{alta}</b><br/>
            <span>📉 Motivo:</span> <b>{normal}</b><br/>
            <span>👨‍👩‍👧‍👦 Target:</span> <b>{segmento}</b>
        </div>
        """,
        "style": {
            "backgroundColor": "#0A3069",
            "color": "#FFA500", # ESTE COLOR ES REFORZADO POR EL CSS .deck-tooltip *
            "fontSize": "18px",
            "padding": "15px",
            "borderRadius": "10px",
            "border": "2px solid #E67E22",
            "zIndex": "1000",
            "boxShadow": "0px 4px 15px rgba(0,0,0,0.5)"
        }
    }

    layer_text = pdk.Layer(
        "TextLayer",
        data=df_rutas,
        get_position="source",
        get_text="origen",
        get_color=[0, 0, 0],
        get_size=26,
        get_alignment_baseline="'bottom'",
        background=True,
        get_background_color=[255, 255, 255, 240]
    )

    view_state = pdk.ViewState(latitude=23.5, longitude=-101.0, zoom=4.2, pitch=40)

    r = pdk.Deck(
        layers=[layer_arc, layer_text],
        initial_view_state=view_state,
        map_style=None,
        height=850,
        tooltip=deck_tooltip
    )
    st.pydeck_chart(r, use_container_width=True)

    st.divider()

    # --- RELLENO DE ESPACIO (TARJETAS HTML DE PILARES) ---
    st.markdown("### 💡 Pilares de Operación")

    col_html1, col_html2, col_html3 = st.columns(3)

    with col_html1:
        st.markdown("""
        <div class="pilar-card">
            <div class="pilar-icon">📍</div>
            <div class="pilar-title">Alcance</div>
            <div class="pilar-value">6 Estados</div>
            <div class="pilar-desc">Fase 1: Hubs Turísticos Clave</div>
        </div>
        """, unsafe_allow_html=True)

    with col_html2:
        st.markdown("""
        <div class="pilar-card">
            <div class="pilar-icon">🚗</div>
            <div class="pilar-title">Transporte</div>
            <div class="pilar-value">Privado</div>
            <div class="pilar-desc">Aeropuerto - Hotel Garantizado</div>
        </div>
        """, unsafe_allow_html=True)

    with col_html3:
        st.markdown("""
        <div class="pilar-card">
            <div class="pilar-icon">🛡️</div>
            <div class="pilar-title">Seguridad</div>
            <div class="pilar-value">100%</div>
            <div class="pilar-desc">Monitoreo Digital 24/7</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- 2. ECOSISTEMA ---
    st.markdown("### 2. El Ecosistema KUALI")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### 2.1. Valor al Cliente")
        fig_pie = go.Figure(data=[go.Pie(
            labels=["Logística", "Hospedaje", "Tecnología", "Experiencias"],
            values=[40, 30, 20, 10], hole=.4,
            textinfo='label+percent',
            textfont=dict(size=20, color="black"),
            marker=dict(colors=["#2874A6", "#E67E22", "#2ECC71", "#F1C40F"], line=dict(color='#000000', width=2)),
            hovertemplate='<b>%{label}</b><br>Aporte: %{percent}<extra></extra>'
        )])
        st.plotly_chart(update_fig_layout(fig_pie, 400), use_container_width=True)
        st.info("El 40% del valor es la **solución logística (Leasing)** integrada.")

    with c2:
        st.markdown("#### 2.2. Estructura Operativa")
        fig_sun = go.Figure(go.Sunburst(
            labels=["KUALI", "Logística", "Hospedaje", "Tecnología", "Leasing", "Traslado", "Hotel", "Ruta", "IA", "Precio"],
            parents=["", "KUALI", "KUALI", "KUALI", "Logística", "Logística", "Hospedaje", "Hospedaje", "Tecnología", "Tecnología"],
            values=[100, 40, 30, 30, 20, 20, 15, 15, 15, 15],
            branchvalues="total",
            textinfo='label+percent root',
            textfont=dict(size=18, color="black"),
            marker=dict(colors=["#2ECC71", "#3498DB", "#E67E22", "#9B59B6", "#AED6F1", "#AED6F1", "#F5CBA7", "#F5CBA7", "#D2B4DE", "#D2B4DE"], line=dict(color='#000000', width=1)),
            hovertemplate='<b>%{label}</b><br>Peso Total: %{percentRoot:.1%}<extra></extra>'
        ))
        st.plotly_chart(update_fig_layout(fig_sun, 400), use_container_width=True)
        st.info("Distribución porcentual del modelo de negocio total.")

    st.divider()

    # --- 3. RADAR ---
    st.markdown("### 3. Ventaja Competitiva")
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=[5, 5, 5, 5, 4], theta=['Transparencia', 'Precio', 'Logística', 'Ética', 'Servicio'], fill='toself', name='KUALI', line_color='#2ECC71', hovertemplate='<b>KUALI:</b> %{r}/5<extra></extra>'))
    fig_radar.add_trace(go.Scatterpolar(r=[2, 2, 1, 1, 2], theta=['Transparencia', 'Precio', 'Logística', 'Ética', 'Servicio'], fill='toself', name='OTAs', line_color='#E74C3C', hovertemplate='<b>OTAs:</b> %{r}/5<extra></extra>'))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 5], tickfont=dict(size=16, color='black')),
            angularaxis=dict(tickfont=dict(size=20, color='black'))
        )
    )
    st.plotly_chart(update_fig_layout(fig_radar, 550), use_container_width=True)

    st.divider()

    # --- 4. TECNOLOGÍA ---
    st.markdown("### 4. Motor Tecnológico")

    fig_tech = px.bar(
        x=[80, 100, 95, 100], y=['Automatización API', 'Algoritmo Antibias', 'Cloud', 'Seguridad'],
        orientation='h', text=[80, 100, 95, 100],
        title="Nivel de Madurez Tecnológica",
        color_discrete_sequence=['#0A3069']
    )
    fig_tech.update_layout(xaxis_title="%", yaxis_title="", showlegend=False)
    fig_tech.update_traces(
        texttemplate='%{text}%',
        textposition='outside',
        textfont_size=24,
        textfont_color="black",
        marker_line_color='black',
        marker_line_width=2,
        hovertemplate='<b>%{y}</b>: %{x}% Completado<extra></extra>'
    )
    st.plotly_chart(update_fig_layout(fig_tech, 450), use_container_width=True)

# ==============================================================================
# PESTAÑA 2: FINANCIERO
# ==============================================================================
with tab2:
    st.header("📈 Análisis Financiero")

    # 1. INVERSION
    st.subheader("1. Inversión Inicial: $1.2 M")
    c_inv1, c_inv2 = st.columns(2)
    with c_inv1:
        fig_pie_inv = px.pie(
            df_inversion_inicial,
            values='Monto Total (MXN)',
            names='Concepto',
            hole=0.4,
            color_discrete_sequence=['#E74C3C', '#3498DB', '#F1C40F', '#2ECC71']
        )
        fig_pie_inv.update_traces(
            textinfo='percent+label',
            textfont_size=24,
            textfont_color="black",
            marker=dict(line=dict(color='#000000', width=2)),
            hovertemplate='<b>%{label}</b><br>Monto: %{value:$,.0f}<extra></extra>'
        )
        st.plotly_chart(update_fig_layout(fig_pie_inv, height=700), use_container_width=True)

    with c_inv2:
        st.markdown("#### Fuentes de Financiamiento")
        labels_source = ['Capital Propio (Socios)', 'Financiamiento (Deuda)']
        values_source = [900000, 300000]
        colors_source = ['#FF6F61', '#48C9B0']

        fig_source = go.Figure(data=[go.Pie(
            labels=labels_source, values=values_source, hole=.6,
            textinfo='label+percent',
            textfont=dict(size=22, color="black"),
            marker=dict(colors=colors_source, line=dict(color='#000000', width=2)),
            hovertemplate='<b>%{label}</b>: %{value:$,.0f}<extra></extra>'
        )])
        fig_source.update_layout(
            annotations=[dict(text='<b>$1.2M</b>', x=0.5, y=0.5, font_size=50, showarrow=False, font_color="black")],
            showlegend=True,
            legend=dict(font=dict(size=20))
        )
        st.plotly_chart(update_fig_layout(fig_source, height=550), use_container_width=True)

    st.divider()

    # 2. PROYECCIÓN
    st.subheader("2. Proyección de Ingresos")
    df_melt = df_proyeccion_ingresos.melt(id_vars=['Concepto'], var_name='Año', value_name='Monto')
    fig_bar = px.bar(df_melt, x='Año', y='Monto', color='Concepto', text_auto='.2s', color_discrete_sequence=['#2ECC71', '#F39C12', '#3498DB'])
    fig_bar.update_traces(textfont_size=20, textfont_color="black", marker_line_color='black', marker_line_width=1.5, hovertemplate='<b>%{x}</b><br>Monto: %{y:$,.0f}<extra></extra>')
    st.plotly_chart(update_fig_layout(fig_bar, 500), use_container_width=True)

    # --- REEMPLAZO: GRÁFICA COMBINADA DE ESCALABILIDAD ---
    st.markdown("#### Evolución de la Eficiencia Operativa")

    anios = ['Año 1', 'Año 2', 'Año 3']
    ingresos = [10930000, 13920000, 18770000]
    costos_operativos_pct = [68, 62, 55] # Eficiencia mejora

    fig_combo = go.Figure()
    fig_combo.add_trace(go.Bar(
        x=anios, y=ingresos, name='Ingresos Totales',
        marker_color='#3498DB', text=ingresos, texttemplate='%{text:.2s}', textposition='inside',
        hovertemplate='<b>Ingreso:</b> %{y:$,.0f}<extra></extra>'
    ))
    fig_combo.add_trace(go.Scatter(
        x=anios, y=costos_operativos_pct, name='Costo Operativo (%)',
        yaxis='y2', mode='lines+markers+text', text=[f"{v}%" for v in costos_operativos_pct], textposition='top center',
        line=dict(color='#E74C3C', width=5), marker=dict(size=12, color='red'),
        hovertemplate='<b>Costo:</b> %{y}%<extra></extra>'
    ))

    fig_combo.update_layout(
        template='plotly_white',
        paper_bgcolor='#FFFFFF', plot_bgcolor='#FFFFFF',
        font=dict(color='black', size=18),
        height=500,
        yaxis=dict(title='Ingresos (MXN)', showgrid=True, gridcolor='#EAEDED'),
        yaxis2=dict(title='Costo Operativo (%)', overlaying='y', side='right', range=[0, 100], showgrid=False),
        legend=dict(x=0.1, y=1.1, orientation='h'),
        hovermode='x unified',
        hoverlabel=dict(bgcolor="#0A3069", font=dict(color="#FFFFFF", size=24), bordercolor="#E67E22")
    )
    st.plotly_chart(fig_combo, use_container_width=True)
    st.success("📉 **Eficiencia:** Al escalar, nuestros costos operativos bajan del 68% al 55%, aumentando el margen neto.")

    st.divider()

    # 3. INDICADORES DINÁMICOS
    st.subheader("3. Salud Financiera (KPIs Dinámicos)")
    c_k1, c_k2, c_k3 = st.columns(3)

    with c_k1:
        fig_g1 = go.Figure(go.Indicator(
            mode="gauge+number+delta", value=2.4,
            title={'text': "Liquidez", 'font': {'color': 'black'}},
            delta={'reference': 1.5, 'increasing': {'color': "green"}, 'position': "top"},
            gauge={
                'axis': {'range': [0, 5], 'tickfont': {'color': 'black', 'size': 18}},
                'bar': {'color': "#2ECC71"},
                'bordercolor': "black", 'borderwidth': 2,
                'threshold': {'value': 1, 'line': {'color': "red", 'width': 4}}
            },
            number={'font': {'color': 'black'}}
        ))
        st.plotly_chart(update_fig_layout(fig_g1, 350), use_container_width=True)
        st.caption("Capacidad de Pago vs Ind. (1.5)")
        st.progress(2.4/5)

    with c_k2:
        fig_g2 = go.Figure(go.Indicator(
            mode="gauge+number+delta", value=34,
            title={'text': "Endeudamiento (%)", 'font': {'color': 'black'}},
            delta={'reference': 50, 'decreasing': {'color': "green"}, 'increasing': {'color': "red"}},
            gauge={
                'axis': {'range': [0, 100], 'tickfont': {'color': 'black', 'size': 18}},
                'bar': {'color': "#3498DB"},
                'bordercolor': "black", 'borderwidth': 2
            },
            number={'font': {'color': 'black'}}
        ))
        st.plotly_chart(update_fig_layout(fig_g2, 350), use_container_width=True)
        st.caption("Autonomía vs Límite (50%)")
        st.progress(34/100)

    with c_k3:
        fig_mar = go.Figure(go.Indicator(
            mode="gauge+number+delta", value=14,
            title={'text': "Margen Neto (%)", 'font': {'color': 'black'}},
            delta={'reference': 10, 'increasing': {'color': "green"}},
            gauge={
                'axis': {'range': [0, 25], 'tickfont': {'color': 'black', 'size': 18}},
                'bar': {'color': "#F39C12"},
                'threshold': {'value': 10, 'line': {'color': "gray", 'width': 4}}
            },
            number={'font': {'color': 'black'}}
        ))
        st.plotly_chart(update_fig_layout(fig_mar, 350), use_container_width=True)
        st.caption("Rentabilidad vs Sector (10%)")
        st.progress(14/25)

# ==============================================================================
# PESTAÑA 3: MERCADO
# ==============================================================================
with tab3:
    st.header("🎯 Estudio de Mercado")

    # 1. OPORTUNIDAD (GIGANTE)
    st.subheader("1. Oportunidad: 82% Demanda Insatisfecha")
    col_m1, col_m2 = st.columns([1, 1])
    with col_m1:
        fig_don = go.Figure(data=[go.Pie(
            labels=['Migraría a KUALI', 'Otros'],
            values=[82, 18], hole=.6,
            marker_colors=['#27AE60', '#D5D8DC'],
            textinfo='none',
            marker=dict(line=dict(color='#000000', width=3)),
            hovertemplate='<b>%{label}:</b> %{percent}<extra></extra>'
        )])
        fig_don.update_layout(
            annotations=[dict(text='<b>82%</b>', x=0.5, y=0.5, font_size=90, showarrow=False, font_color="#000000")]
        )
        st.plotly_chart(update_fig_layout(fig_don, 700), use_container_width=True)
    with col_m2:
        st.markdown("#### ¿Por qué KUALI?")
        df_razones = pd.DataFrame({
            'Motivo': ['Desconfianza Cargos Ocultos', 'Odio a Precios Dinámicos', 'Busca Transparencia'],
            'Porcentaje': [87, 75, 82]
        })
        fig_raz = px.bar(
            df_razones, x='Porcentaje', y='Motivo', orientation='h', text='Porcentaje',
            color='Porcentaje', color_continuous_scale='Reds'
        )
        fig_raz.update_layout(yaxis=dict(autorange="reversed"), showlegend=False)
        fig_raz.update_traces(texttemplate='%{text}%', textposition='inside', textfont_size=24, textfont_color="white", marker_line_color='black', marker_line_width=1.5, hovertemplate='<b>%{y}:</b> %{x}%<extra></extra>')
        st.plotly_chart(update_fig_layout(fig_raz, 500), use_container_width=True)
        st.info("El mercado actual está roto por la desconfianza.")

    st.divider()

    # 2. POSICIONAMIENTO
    st.subheader("2. Posicionamiento Competitivo")
    st.table(df_precios_competencia)

    st.divider()

    # 3. Volatilidad
    st.subheader("3. Estabilidad vs Volatilidad")
    st.markdown("Comparativa en temporada alta (Día de Muertos).")

    st.plotly_chart(crear_grafica_kuali(), use_container_width=True)

    st.markdown("#### Competencia (Precios Inestables)")
    cg1, cg2 = st.columns(2)
    with cg1:
        st.plotly_chart(crear_grafica_plataforma("DESPEGAR", "#8E44AD", 0.25, 1.0), use_container_width=True)
        st.plotly_chart(crear_grafica_plataforma("BOOKING", "#2E86C1", 0.40, 1.02), use_container_width=True)
    with cg2:
        st.plotly_chart(crear_grafica_plataforma("EXPEDIA", "#F39C12", 0.20, 1.05), use_container_width=True)
        st.plotly_chart(crear_grafica_plataforma("PRICETRAVEL", "#3498DB", 0.30, 0.92), use_container_width=True)

    # --- CIERRE ESTRATÉGICO ---
    st.success("✅ **Conclusión:** KUALI entra en un Océano Azul donde la confianza es la moneda de cambio.")
