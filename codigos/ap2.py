# IMPORTANDO AS BIBLIOTECAS selenium, time E pandas

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import plotly.express as px
#import streamlit as st

# ABRINDO O NAVEGADOR E MAXIMIZANDO A TELA
navegador = webdriver.Chrome()
navegador.maximize_window()


# ABRINDO O SITE
navegador.get('https://www.trocafone.com.br/smartphones/smartphones?initialMap=c&initialQuery=smartphones&map=category-1,category-2')


# ROLAR A TELA DA PÁGINA ATÉ O FINAL PARA CARREGAR TODOS OS PRODUTOS
def scroll_smoothly(driver, duration = 15):
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    step = scroll_height // (duration * 15)
    current_position = 0
    
    while current_position < scroll_height:
        current_position += step
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(0.1)


# GARANTINDO QUE A PÁGINA FOI ATÉ O FINAL
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# ROLAR A TELA LENTAMENTE PARA NÃO CORRER O RISCO DE DESCER MUITO RÁPIDO E NÃO CARREGAR OS PRODUTOS
scroll_smoothly(navegador, duration = 15)


# LISTA COM OS NOMES DAS MARCAS
lista_marcas = []
for marcas in range(1,40):
    try:
        #print(navegador.find_element(By.XPATH, f'//*[@id="gallery-layout-container"]/div[{marcas}]/section/a/article/div[4]/span').text)
        dados_marcas = navegador.find_element(By.XPATH, f'//*[@id="gallery-layout-container"]/div[{marcas}]/section/a/article/div[4]/span').text
        lista_marcas.append(dados_marcas)  #ITERANDO A LISTA VAZIA
    except:
        pass


# LISTA COM OS NOMES DOS PRODUTOS
lista_nomes = []
for nomes in range(1,40):
    try:
        #print(navegador.find_element(By.XPATH, f'//*[@id="gallery-layout-container"]/div[{nomes}]/section/a/article/div[5]/h2/span').text)
        dados_nomes = navegador.find_element(By.XPATH, f'//*[@id="gallery-layout-container"]/div[{nomes}]/section/a/article/div[5]/h2/span').text
        lista_nomes.append(dados_nomes)  #ITERANDO A LISTA VAZIA
    except:
        pass


# LISTA COM OS PREÇOS DESCONTADOS
lista_desconto = []
for desconto in range(1,40):
    try:
        #print(navegador.find_element(By.XPATH, f'//*[@id="gallery-layout-container"]/div[{desconto}]/section/a/article/div[6]/div/div/div/div[1]/div/div/div/div[2]/span[1]').text)
        dados_desconto = navegador.find_element(By.XPATH, f'//*[@id="gallery-layout-container"]/div[{desconto}]/section/a/article/div[6]/div/div/div/div[1]/div/div/div/div[2]/span[1]').text
        lista_desconto.append(dados_desconto)  #ITERANDO A LISTA VAZIA
    except:
        pass


# LISTA COM OS PREÇOS SEM DESCONTO
lista_preco = []
for preco in range(1,40):
    try:
        #print(navegador.find_element(By.XPATH, f'//*[@id="gallery-layout-container"]/div[{preco}]/section/a/article/div[6]/div/div/div/div[2]/div/div/div/div/span[1]/strong').text)
        dados_preco = navegador.find_element(By.XPATH, f'//*[@id="gallery-layout-container"]/div[{preco}]/section/a/article/div[6]/div/div/div/div[2]/div/div/div/div/span[1]/strong').text
        lista_preco.append(dados_preco)  #ITERANDO A LISTA VAZIA
    except:
        pass

# CRIANDO O DATAFRAME PARA A COLUNA MARCA
tb_marcas = pd.DataFrame(lista_marcas, columns=['marca'])
#tb_marcas


# CRIANDO O DATAFRAME PARA A COLUNA PRODUTO
tb_nomes = pd.DataFrame(lista_nomes, columns=['produto'])
#tb_nomes


# CRIANDO O DATAFRAME PARA A COLUNA DESCONTO
tb_desconto = pd.DataFrame(lista_desconto, columns=['desconto'])
#tb_desconto


# CRIANDO O DATAFRAME PARA A COLUNA PREÇO
tb_preco = pd.DataFrame(lista_preco, columns=['preco'])
#tb_preco


# CONCATENANDO OS DATAFRAME's DAS TABELAS CRIADAS ANTERIORMENTE
df = pd.concat([tb_marcas, tb_nomes, tb_desconto, tb_preco], axis=1)
#df

# EXPORTANDO PARA O CSV
df.to_csv("../bases_originais/base_bruta.csv", index=False, sep=';', encoding='utf-8')

# LIMPEZA DE PREÇO E DESCONTO
for troca in ['preco', 'desconto']:
    df[troca] = df[troca].str.replace('R$', '')

# LIMPEZA DE PREÇO E DESCONTO
for troca in ['preco', 'desconto']:
    df[troca] = df[troca].str.replace('.', '')

# LIMPEZA DE PREÇO E DESCONTO
for troca in ['preco', 'desconto']:
    df[troca] = df[troca].str.replace(',', '.')

# CONVERSÃO PARA NUMÉRICO
for col in ['preco', 'desconto']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# CALCULAR O VALOR DE DESCONTO
df['valor_desconto'] = (df['preco'] - df['desconto']).round(2)

# CALCULAR O PERCENTUAL DE DESCONTO
df['perc_desconto'] = (df['valor_desconto'] / df['preco']).round(2)

# NULOS
df.fillna({'preco': 0, 'desconto': 0, 'valor_desconto': 0, 'perc_desconto': 0}, inplace=True)

# DUPLICATAS
#df = df.drop_duplicates(subset=['marca', 'produto'])
df = df.drop_duplicates(subset=['marca', 'produto', 'preco', 'desconto', 'valor_desconto', 'perc_desconto'])


# OUTLIERS
for col in ['preco', 'desconto', 'valor_desconto', 'perc_desconto']:
    df.loc[df[col] >= 3200, col] = 3200
    df.loc[df[col] <= 0, col] = 20

# EXPORTAR
df.to_csv("../bases_tratadas/base_tratada.csv", index=False, sep=';', encoding='utf-8')