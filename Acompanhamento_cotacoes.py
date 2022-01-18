
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
from PIL import Image
import xlrd



st.set_page_config(page_title='Acompanhamento de cotações')
st.header('Acompanhamento Cotações 2022')

image = Image.open('Engeman logo.png')
st.image(image, width=300)




# LOAD DATA

excel_file = '2022. ACOMPANHAMENTO DE COTAÇÕES ACs.xlsx'

df = pd.read_excel(excel_file)

df_cotacoes_respondidas = pd.read_excel(excel_file, 
                                        usecols='B,J')

pie_chart = px.pie(df_cotacoes_respondidas, 
                   title = '***Monitoramento***',
                   values='AC',
                   names= 'STATUS')

st.plotly_chart(pie_chart)

#Bar Chart
df_cotacoes = pd.read_excel(excel_file, usecols='B,E,I')


bar_chart = px.bar(df_cotacoes,
                    x = "AC",
                    y = ["COTAÇÕES SOLICITADAS AO MERCADO", "COTAÇÕES NÃO RECEBIDAS DO MERCADO"],
                    title = 'Comparação',
                    barmode='group',
                    color_discrete_map={
                   "COTAÇÕES SOLICITADAS AO MERCADO": 'blue',
                   "COTAÇÕES NÃO RECEBIDAS DO MERCADO": 'red'},
                    # color_discrete_sequence= ['#F63366']*len(df_cotacoes),
                    template= 'plotly_white',
                    height = 400)

st.plotly_chart(bar_chart)

st.dataframe(df)



#Filter dataframe
st.sidebar.header("Nº de cotações não recebidas")
info = st.sidebar.empty()

AC = df['AC'].unique().tolist()

nome_da_planilha= df['NOME PLANILHA'].unique().tolist()

Cotacoes_n = df['COTAÇÕES NÃO RECEBIDAS DO MERCADO'].unique().tolist()


ac_selection = st.sidebar.slider('AC:',
                          min_value= min(AC),
                          max_value= max(AC),
                          value=(min(AC), max(AC)))

Cotacoes_n_selection = st.sidebar.multiselect('Nome da planilha:',
                                      nome_da_planilha, 
                                      default= nome_da_planilha)



# print(df.columns)

cotacoes_nao_receidas = df['COTAÇÕES NÃO RECEBIDAS DO MERCADO']

# mask = df[(df['AC'] == ac_selection) & (cotacoes_nao_receidas.isin(Cotacoes_n_selection))]

mask = (df['AC'].between(*ac_selection)) & (df['NOME PLANILHA'].isin(Cotacoes_n_selection))
number_of_result = df[mask].shape[0]
# st.sidebar.markdown(f'N de cotações não recebidas: {number_of_result}')
info.info("{} Planilhas".format(number_of_result))
