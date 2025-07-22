import streamlit as st
import pandas as pd
import sqlite3

#conectando com o banco
conn = sqlite3.connect('data/amazonbrasil.sql')
df = pd.read_sql_query('SELECT * FROM tenis', conn)
conn.close()

#titulo
st.title('📈 Pesquisa de Mercado - Tênis na Amazon Brasil')
st.subheader('KPIs principais')

col1, col2, col3 = st.columns(3)

total_itens = df.shape[0]
col1.metric(label='Total de Tenis', value=total_itens)

unique_brands = df['brand'].nunique()
col2.metric(label='Total de Marcas', value=unique_brands)

# Converter e arredondar os preços
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['price'] = df['price'].round(2)
average_price = df['price'].mean()
col3.metric(label='Preço Médio', value=f'R$ {average_price:,.2f}'.replace('.', ','))


#Marcas mais frequentes
st.subheader('Marcas mais encontradas até a 7º página')
col1, col2 = st.columns([4, 2])
top_brands = df['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_brands)
col2.dataframe(top_brands)

#Preço medio por marca
st.subheader('Preço médio por marca')
col1, col2 = st.columns([4, 2])
df_nom_zero_prices = df[df['price']> 0]
average_price_by_brand = (
    df_nom_zero_prices.groupby('brand')['price']
    .mean()
    .round(2)
    .sort_values(ascending=False)
)
col1.bar_chart(average_price_by_brand)
formatted_prices = average_price_by_brand.apply(lambda x: f'R$ {x:,.2f}'.replace('.', ','))
col2.dataframe(formatted_prices)

#Satistação por marca
st.subheader('Satistação por marca')
col1, col2 = st.columns([4, 2])
df['reviews_rating_number'] = pd.to_numeric(df['reviews_rating_number'], errors='coerce')
df['reviews_rating_number'] = df['reviews_rating_number'].round(2)
df_nom_zero_reviews = df[df['reviews_rating_number'] > 0]
saturation_by_brand = (
    df_nom_zero_reviews.groupby('brand')['reviews_rating_number']
    .mean()
    .round(2)
    .sort_values(ascending=False))
col1.bar_chart(saturation_by_brand)
col2.write(saturation_by_brand)
