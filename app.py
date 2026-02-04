import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Crypto Rank Tracker", layout="wide")

st.title("📊 Ranking Histórico de Criptomonedas (Top 400)")
st.markdown("Visualiza cómo ha evolucionado la posición de tus criptos favoritas según el ranking de Coinmarketcap")

# 1. Cargar los datos
@st.cache_data # Esto hace que la web cargue rápido
def cargar_datos():
    df = pd.read_csv('historico_top400_ranking.csv')
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    return df

try:
    data = cargar_datos()

    # 2. Selectores
    col1, col2 = st.columns([0.5, 0.5])

    with col1:
        data['Display'] = data['Nombre'] + " (" + data['Ticker'] + ")"
        lista_monedas = sorted(data['Display'].unique())
        try:
            indice_defecto = lista_monedas.index("Polkadot (DOT)")
        except ValueError:
            indice_defecto = 0
        seleccion = st.selectbox("Criptomoneda:", lista_monedas, index=indice_defecto)
    
    with col2:
        frecuencia = st.radio("Frecuencia:", ["Día", "Semana", "Mes"], horizontal=False)

    # 3. Filtrado por moneda
    df_filtrado = data[data['Display'] == seleccion].sort_values('Fecha')

    # --- LÓGICA DE HITOS TEMPORALES ---
    if frecuencia == "Semana":
        # dt.dayofweek: 0 es Lunes, 1 Martes...
        df_final = df_filtrado[df_filtrado['Fecha'].dt.dayofweek == 0]
    elif frecuencia == "Mes":
        # dt.day: extrae el número del día del mes
        df_final = df_filtrado[df_filtrado['Fecha'].dt.day == 1]
    else:
        df_final = df_filtrado

    # 4. Crear el Gráfico con Plotly
    if df_final.empty:
        # Si el filtro vacía la tabla, avisamos al usuario
        st.warning(f"⚠️ No hay datos para la frecuencia: {frecuencia}")
    else:
        fig = px.line(
            df_final, 
            x='Fecha', 
            y='Ranking', 
            title=f"Evolución de Ranking: {seleccion}",
            markers=True,
            template="plotly_dark"
        )

        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>%{y}<extra></extra>"
        )

        # IMPORTANTE: Invertir el eje Y (para que el puesto 1 esté arriba)
        fig.update_yaxes(
            autorange="reversed",
            dtick=1,
            tickformat='d'
        )

        # 5. Mostrar el gráfico
        st.plotly_chart(fig, use_container_width=True)

        # 6. Mostrar tabla limpia
        st.subheader("Últimos registros")

        tabla_final = df_final.drop(columns=['Display']).tail(100) # preparamos los datos para la tabla
        st.dataframe(tabla_final, hide_index=True, use_container_width=True) # la mostramos sin índice y ajustada al ancho

except FileNotFoundError:
    st.error("No se encontró el archivo CSV. Ejecuta primero el script de recolección de datos.")