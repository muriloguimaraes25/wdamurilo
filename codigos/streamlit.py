import streamlit as st
import pandas as pd
import plotly.express as px

csv = "https://raw.githubusercontent.com/muriloguimaraes25/wdamurilo/refs/heads/main/bases_tratadas/base_tratada.csv"
df = pd.read_csv(csv, sep=';')

st.dataframe(df)

st.subheader('Análise de nulos')
aux = df.isnull().sum().reset_index()
aux.columns = ['Coluna', 'Quantidade de Nulos']
st.dataframe(aux)

st.subheader('Análises univariadas')
st.write('Medidas resumo')
st.dataframe(df.describe())

#SELECIONANDO AS COLUNAS AUTOMATICAMENTE
lista_de_colunas = df.columns
colunas_numericas = df.select_dtypes(include='number').columns.tolist()

if colunas_numericas:
    coluna_escolhida = st.selectbox('Escolha a coluna', colunas_numericas)

    media = round(df[coluna_escolhida].mean(), 2)
    desvio = round(df[coluna_escolhida].std(), 2)
    mediana = round(df[coluna_escolhida].quantile(0.5), 2)
    maximo = round(df[coluna_escolhida].max(), 2)
    minimo = round(df[coluna_escolhida].min(), 2)  # Corrigido

    st.write(f"**Média**: {media}")
    st.write(f"**Desvio padrão**: {desvio}")
    st.write(f"**Mediana**: {mediana}")
    st.write(f"**Máximo**: {maximo}")
    st.write(f"**Mínimo**: {minimo}")

    st.write(f'A coluna escolhida foi **{coluna_escolhida}**.')
    st.write(f'A sua média é **{media}**, o desvio padrão é **{desvio}**, a mediana é **{mediana}**, o máximo é **{maximo}**, e o mínimo é **{minimo}**.')

    st.subheader('Histograma')
    fig = px.histogram(df, x=coluna_escolhida)
    st.plotly_chart(fig)

    st.subheader('Boxplot')
    fig2 = px.box(df, x=coluna_escolhida)
    st.plotly_chart(fig2)
else:
    st.warning("Não contém coluna numérica.")

print('Média de valores descontados:', media)
print('Desvio padrão de valores descontados:', desvio)
print('Mediana dos valores descontados:', mediana)
print('Máximo dos valores descontados:' , maximo)
print('Menor valor dos descontados:', menor_desconto)

# Análises multivariadas
st.subheader('Análises multivariadas')
lista_de_escolhas = st.multiselect('Escolha mais de uma coluna para avaliar', lista_de_colunas)

if len(lista_de_escolhas) != 2:
    st.error('Escolha exatamente 2 colunas')
else:
    st.markdown('### Gráfico de Dispersão')
    fig3 = px.scatter(df, x=lista_de_escolhas[0], y=lista_de_escolhas[1])
    st.plotly_chart(fig3)

    st.markdown('### Boxplot')
    fig4 = px.box(df, x=lista_de_escolhas[0], y=lista_de_escolhas[1])
    st.plotly_chart(fig4)

    st.markdown('### Gráfico de Pizza')
    # Verificação para evitar erro em gráfico de pizza
    if df[lista_de_escolhas[0]].nunique() < 50:
        fig5 = px.pie(df, names=lista_de_escolhas[0], values=lista_de_escolhas[1])
        st.plotly_chart(fig5)
    else:
        st.warning("A coluna selecionada para o gráfico de pizza tem muitos valores únicos.")
