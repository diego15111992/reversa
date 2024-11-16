import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.header("DASHBOAR DE DOAÇÕES E BONIFICAÇÕES 2024")


df = pd.read_excel("doacoes_bonificacoes.xlsx", decimal=",")
df["DT NOTA"] = pd.to_datetime(df["DT NOTA"])
df=df.sort_values("DT NOTA")

df["Month"] = df["DT NOTA"].apply(lambda x: str(x.year) + "-" + str(x.month))
month = st.sidebar.selectbox("Mês", df["Month"].unique())

df_filtered = df[df["Month"] == month]

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

#Gráfico de barras com valores por dia
fig_date = px.bar(df_filtered, x="DT NOTA", y="VLR FAT", title="FATURAMENTO POR DIA")
col1.plotly_chart(fig_date, use_container_width=True)

fig_prod = px.bar(df_filtered, x="DT NOTA", y="TIPO DE SAIDA", 
                  color="TIPO DE SAIDA", title="TIPOS DE SAIDA",
                  orientation="h")
col2.plotly_chart(fig_prod, use_container_width=True)


valor_total = df_filtered.groupby("TIPO DE SAIDA")[["VLR FAT"]].sum().reset_index()
fig_city = px.bar(valor_total, x="TIPO DE SAIDA", y="VLR FAT",color="TIPO DE SAIDA",title="FATURAMENTO POR TIPO DE SAIDA")
col3.plotly_chart(fig_city, use_container_width=True)


fig_kind = px.pie(df_filtered, values="VLR FAT", names="TIPO DE SAIDA",
                   title="PERCENTUAL POR TIPO DE SAIDA")
col4.plotly_chart(fig_kind, use_container_width=True)


