import os

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine


@st.cache_resource
def get_engine():
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL não encontrada no arquivo .env")
    return create_engine(database_url)


def load_data(view_name: str) -> pd.DataFrame:
    engine = get_engine()
    return pd.read_sql(f"SELECT * FROM {view_name}", engine)


st.set_page_config(page_title="Dashboard de Temperaturas IoT", layout="wide")

st.title("Dashboard de Temperaturas IoT")
st.write("Análise de leituras de temperatura por ambiente, horário e localização.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Média de Temperatura por Ambiente")
    df_avg_room = load_data("avg_temp_por_ambiente")
    fig1 = px.bar(
        df_avg_room,
        x="room_id",
        y="avg_temp",
        title="Média de temperatura por ambiente"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Leituras por Hora")
    df_hour = load_data("leituras_por_hora")
    fig2 = px.line(
        df_hour,
        x="hora",
        y="contagem",
        markers=True,
        title="Quantidade de leituras por hora do dia"
    )
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Temperaturas Máximas e Mínimas por Dia")
    df_day = load_data("temp_max_min_por_dia")
    fig3 = px.line(
        df_day,
        x="data",
        y=["temp_max", "temp_min"],
        markers=True,
        title="Máximas e mínimas por dia"
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Média de Temperatura: In x Out")
    df_inout = load_data("media_temp_in_out")
    fig4 = px.bar(
        df_inout,
        x="location_type",
        y="avg_temp",
        title="Comparação entre ambiente interno e externo"
    )
    st.plotly_chart(fig4, use_container_width=True)

st.subheader("Prévia dos dados")
engine = get_engine()
df_raw = pd.read_sql("SELECT * FROM temperature_readings LIMIT 20", engine)
st.dataframe(df_raw, use_container_width=True)
