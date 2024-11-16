import streamlit as st
import pandas as pd
import plotly. express as px

#Configura a página para uzar toso o espaço
st.set_page_config(layout="wide",page_title="doacoesbonificacoes")
st.title("DASHBOARD DOAÇÕES & BONIFICAÇÕES")

#Define a organização das figuras na página
col1,col2, col3 = st.columns(3)
col4,col5 = st.columns(2)

with col1:
    st.image("logo.png", width=200,)
with col2:    
    st.image("c5.png", width=250)
with col3:
    st.image("polar.png",width=140)


#Busca os dados do arquivo em excel
dados = pd.read_excel("doacoes_bonificacoes.xlsx",decimal=",")

#Faz com que o pandas reconheça as datas na coluna da planila e ordena de A a Z
dados["DT NOTA"] = pd.to_datetime(dados["DT NOTA"])
dados = dados.sort_values("DT NOTA")

#Sepera os meses contidos na planilha
dados["Month"] = dados["DT NOTA"].apply(lambda x: str(x.month) + " - " + str(x.year))
month = st.sidebar.selectbox("SELECIONE O MÊS", dados["Month"].unique())
mod_filtro_data = st.sidebar.toggle("ATIVAR/DESATIVAR FILTRO")

#carrega os dados de acordo com filtro de datas
filtro_mes = dados[dados["Month"] == month]

if mod_filtro_data == False or month == "":
    #Agrupa os tipos de saida e faz a soma, para exibir no g´rafico de barras
    valor_t = dados.groupby("TIPO DE SAIDA")[["VLR FAT"]].sum().reset_index()
    grafico_tipo = px.bar(valor_t, x="TIPO DE SAIDA", y="VLR FAT",color="TIPO DE SAIDA",title="FATURAMENTO POR TIPO DE SAIDA")
    grafico_tipo.update_layout(xaxis_title="",yaxis_title="")
    col4.plotly_chart(grafico_tipo, use_container_width=True)

    #Cria o gráfico de pizza
    grafico_pizza = px.pie(dados, values="VLR FAT", names="TIPO DE SAIDA",color="TIPO DE SAIDA",title="PERCENTUAL POR TIPO DE SAIDA")
    col5.plotly_chart(grafico_pizza, use_container_width=True)

    #tabela com rank 5 vendedores
    with col1:
        df_vendedores = dados.groupby("VEND")[["VLR FAT"]].sum().reset_index()
        df_vendedores.rename(columns={"VEND":"VENDEDOR","VLR FAT": "VALOR"})
        rank5 = df_vendedores.sort_values(by="VLR FAT", ascending=False)
        df_r = st.dataframe(rank5.head(5).reset_index(drop=True))

    with col2:
        #tabela top 5 produtos
        df_produtos = dados.groupby("PRODUTOS")[["VLR FAT"]].sum().reset_index()
        rank5_prod = df_produtos.sort_values(by="VLR FAT", ascending=False)
        df_p = st.dataframe(rank5_prod.head(5).reset_index(drop=True))

    #Card com aturamento total
    with col3:
        valor_total = dados["VLR FAT"].sum()
        card_valor_total = st.metric(label="VALOR TOTAL",value=f"R${valor_total:.2f}")

        peso_total = dados["KG"].sum() / 100
        card_peso_total = st.metric(label="PESO",value=f"{peso_total:.2f} TON")
else:    
    #Agrupa os tipos de saida e faz a soma, para exibir no g´rafico de barras
    valor_t = filtro_mes.groupby("TIPO DE SAIDA")[["VLR FAT"]].sum().reset_index()
    grafico_tipo = px.bar(valor_t, x="TIPO DE SAIDA", y="VLR FAT",color="TIPO DE SAIDA",title="FATURAMENTO POR TIPO DE SAIDA")
    grafico_tipo.update_layout(xaxis_title="",yaxis_title="")
    col4.plotly_chart(grafico_tipo, use_container_width=True)

    #Cria o gráfico de pizza
    grafico_pizza = px.pie(filtro_mes, values="VLR FAT", names="TIPO DE SAIDA",color="TIPO DE SAIDA",title="PERCENTUAL POR TIPO DE SAIDA")
    col5.plotly_chart(grafico_pizza, use_container_width=True)

    #tabela com rank 5 vendedores
    with col1:
        df_vendedores = filtro_mes.groupby("VEND")[["VLR FAT"]].sum().reset_index()
        df_vendedores.rename(columns={"VEND":"VENDEDOR","VLR FAT": "VALOR"})
        rank5 = df_vendedores.sort_values(by="VLR FAT", ascending=False)
        df_r = st.dataframe(rank5.head(5).reset_index(drop=True))

    with col2:
        #tabela top 5 produtos
        df_produtos = filtro_mes.groupby("PRODUTOS")[["VLR FAT"]].sum().reset_index()
        rank5_prod = df_produtos.sort_values(by="VLR FAT", ascending=False)
        df_p = st.dataframe(rank5_prod.head(5).reset_index(drop=True))

    #Card com aturamento total
    with col3:
        valor_total = filtro_mes["VLR FAT"].sum()
        card_valor_total = st.metric(label="VALOR TOTAL",value=f"R${valor_total:.2f}")

        peso_total = filtro_mes["KG"].sum() / 100
        card_peso_total = st.metric(label="PESO",value=f"{peso_total:.2f} TON")


st.markdown("desenvolvido por: Diego Dias - Tec. logistica e Transporte")