import streamlit as st
import pandas as pd

st.title("Dashboard de Vendas")


@st.cache_data
def carregar_dados():
    return pd.read_csv("vendas.csv", sep=";")


df = carregar_dados()

st.sidebar.title("Filtros")

lista_de_categorias = df["categoria"].unique()

categorias_selecionadas = st.sidebar.multiselect(
    "Selecione as Categorias",
    options=lista_de_categorias,
    default=lista_de_categorias
)

df_filtrado = df[
    df["categoria"].isin(categorias_selecionadas)
]

receita_calculada = df_filtrado["valor_venda"].sum()

total_pedidos = len(df_filtrado)

col1, col2 = st.columns([1, 1])

with col1:
    st.metric(
        label="Receita Total",
        value=f"R$ {receita_calculada:,.2f}"
    )

with col2:
    st.metric(
        label="Total de Pedidos",
        value=total_pedidos
    )


aba1, aba2 = st.tabs([
    "Evolução Mensal",
    "Tabela de Dados"
])


with aba1:

    df_filtrado["data_hora"] = pd.to_datetime(
        df_filtrado["data_hora"]
    )

    dados_agrupados = (
        df_filtrado
        .groupby(
            df_filtrado["data_hora"].dt.to_period("M")
        )["valor_venda"]
        .sum()
    )

    dados_agrupados.index = dados_agrupados.index.astype(str)

    st.area_chart(dados_agrupados)


with aba2:

    st.dataframe(df_filtrado)

    csv = df_filtrado.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Baixar dados filtrados",
        data=csv,
        file_name="vendas_filtradas.csv",
        mime="text/csv"
    )