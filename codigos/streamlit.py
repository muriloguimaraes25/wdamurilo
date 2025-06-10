# IMPORTANDO AS BIBLIOTECAS selenium, time E pandas

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import plotly.express as px
import streamlit as st

df = pd.read_csv('../bases_tratadas/base_tratada.csv', sep=';')
st.dataframe(df)

st.subheader('Análise de nulos')
aux = df.isnull().sum().reset_index()
aux.columns = ['variavel', 'qtd_miss']
st.dataframe(aux)

st.subheader('Análises univariadas')
st.write('Medidas resumo')
st.dataframe(df.describe())

#SELECIONANDO AS COLUNAS AUTOMATICAMENTE
lista_de_colunas = df.columns

colunas_numericas = df.select_dtypes(include='number').columns.tolist()

# Verifica se há colunas numéricas
if colunas_numericas:

    # MENU DE SELEÇÃO
    coluna_escolhida = st.selectbox('Escolha a coluna', colunas_numericas)
    
    # ESTATÍSTICAS
    media = round(df[coluna_escolhida].mean(), 2)
    desvio = round(df[coluna_escolhida].std(), 2)
    mediana = round(df[coluna_escolhida].median(), 2)
    maximo = round(df[coluna_escolhida].max(), 2)
    menor_desconto = df['desconto'].min()

    st.write(f"**Média**: {media}")
    st.write(f"**Desvio padrão**: {desvio}")
    st.write(f"**Mediana**: {mediana}")
    st.write(f"**Máximo**: {maximo}")
else:
    st.warning("O DataFrame não contém colunas numéricas.")

print('Média de valores descontados:', media)
print('Desvio padrão de valores descontados:', desvio)
print('Mediana dos valores descontados:', mediana)
print('Máximo dos valores descontados:' , maximo)
print('Menor valor dos descontados:', menor_desconto)

st.write(f'A coluna escolhida foi {coluna_escolhida}. A sua média é {media}. Seu desvio padrão indica que, quando há desvio, desvia em média {desvio}. E 50% dos dados vão até o valor {mediana}. E seu máximo é de {maximo}.')
st.write(f'Produto com menor valor {menor_desconto} litros')
st.write('Histograma')
fig = px.histogram(df,x=[coluna_escolhida])
st.plotly_chart(fig)
st.write('Boxplot')
fig2 = px.box(df, x=[coluna_escolhida])
st.plotly_chart(fig2)

st.subheader('Análises multivariadas')
lista_de_escolhas = st.multiselect('Escolha mais de uma coluna para avaliar', lista_de_colunas)
st.markdown('Gráfico de dispersão')
if len(lista_de_escolhas)>2 or len(lista_de_escolhas)<2:
    st.error('Escolha somente 2 colunas')
else:
    fig3 = px.scatter(df, x=lista_de_escolhas[0], y=lista_de_escolhas[1])
    st.plotly_chart(fig3)
    st.markdown('Gráfico de caixa')
    fig4 = px.box(df, x=lista_de_escolhas[0], y=lista_de_escolhas[1])
    st.plotly_chart(fig4)