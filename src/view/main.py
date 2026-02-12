import streamlit as st
import pandas as pd
import os
class View: 

    def execute(self):
        st.title("Monitoramento de preço de notebooks")

        # verificar se o arquivo existe
        if(not os.path.exists('/home/vinicyos/python_projetos/monitoramento_preco/data/products.csv')):
            st.write("Clique no botão para iniciar a coleta de dados")
            st.stop()

        df = pd.read_csv('/home/vinicyos/python_projetos/monitoramento_preco/data/products.csv')

        st.subheader("KPIs")
        col1, col2, col3 = st.columns(3)

        total_itens = df.shape[0]
        col1.metric(label="Total de itens", value=total_itens)

        unique_stores = df['store'].nunique()
        col2.metric(label="Total de lojas", value=unique_stores)

        average_price = df['currentPrice'].mean()
        col3.metric(label="Preço médio", value=f"R${average_price:.2f}")

        # Quais sao as lojas mais encontradas
        st.subheader("Lojas mais encontradas no sistema até a página 10")
        col1, col2 = st.columns([4, 2])
        top_10_stores = df['store'].value_counts().sort_values(ascending=False).head(15)
        col1.bar_chart(top_10_stores)
        col2.write(top_10_stores)

        # Preço médio por loja
        st.subheader("Preço médio por loja")
        col1, col2 = st.columns([4, 2])
        average_price_by_store = df.groupby('store')['currentPrice'].mean().sort_values(ascending=False).head(15)
        col1.bar_chart(average_price_by_store)
        col2.write(average_price_by_store)

        st.subheader("Lojas com melhores taxas de desconto")
        col1, col2 = st.columns([4, 3])
        df['discout_rate'] = (1 - (df['currentPrice'] / df['oldPrice'])) * 100
        rating_discount = df.groupby('store')['discout_rate'].mean().sort_values(ascending=False).head(15)
        col1.line_chart(rating_discount)
        col2.write(rating_discount)

            
