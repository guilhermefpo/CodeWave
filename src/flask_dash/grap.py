import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import sidrapy
import numpy as np
import os
def criando_grap():
 url='https://www.sjc.sp.gov.br/servicos/governanca/populacao/'
 df=pd.read_html(url,header=0)
#grafico etario
 df1=df[1].copy()

 df1 = df1[df1["Grupo etário"] != "Total"]


 df1["2010"] = pd.to_numeric(df1["2010"])
 df1["2022"] = pd.to_numeric(df1["2022"])

 fig = px.bar(
    df1, 
    x="Grupo etário", 
    y=["2010", "2022"], 
    barmode="group", 
    title="População por grupo etário - 2010 x 2022",
    labels={
        "value": "População", 
        "variable": "Ano",
        "Grupo etário": "Faixa Etária"
    }
)
#grafico piramide etaria
 grup_quinhental = df[2].copy()

# Consertando os números da coluna Homens
 lis_h = []
 for x in grup_quinhental['Homens (2022)']:
  if x < 100 and x != 12:
    x = x * 1000
    lis_h.append(x)
  else:
    lis_h.append(x)
 grup_quinhental['Homens (2022)'] = lis_h

# Consertando os números da coluna Mulheres
 lis_m = []
 for x in grup_quinhental['Mulheres (2022)']:
  if x < 100 and x != 73:
    x = x * 1000
    lis_m.append(x)
  else:
    lis_m.append(x)
 grup_quinhental['Mulheres (2022)'] = lis_m

# Criar pirâmide etária
 fig2 = go.Figure()

# Homens (lado esquerdo, valores negativos)
 fig2.add_trace(go.Bar(
    y=grup_quinhental['Grupo quinquenal'],
    x=-grup_quinhental['Homens (2022)'],
    name='Homens',
    orientation='h',
    marker=dict(color='lightblue')
))

# Mulheres (lado direito, valores positivos)
 fig2.add_trace(go.Bar(
    y=grup_quinhental['Grupo quinquenal'],
    x=grup_quinhental['Mulheres (2022)'],
    name='Mulheres',
    orientation='h',
    marker=dict(color='pink')
))

 fig2.update_layout(
    title='Pirâmide Etária - São José dos Campos (2022)',
    barmode='overlay',
    xaxis=dict(
        title='População',
        tickvals=[-30000, -20000, -10000, 0, 10000, 20000, 30000],
        ticktext=['30mil', '20mil', '10mil', '0', '10mil', '20mil', '30mil']
    ),
    yaxis=dict(title='Faixa Etária'),
    showlegend=True
)
 # grafico do setor socio
 p=df[4]
 l=[]
 for x in p['População (2022)']:
  if x < 100:
    x=x*1000
    l.append(x)
  else:
    l.append(x)
 p['População(2022)']=l




 popu_set = px.bar(p, x="Setor socioeconômico/área", y='População(2022)', title="População")
 

#grafico domiporregiao
 lista_coorec=[]


 domi_regi=df[3]
 domi_regi['Domicílios particulares (2022)']=domi_regi['Domicílios particulares (2022)'].astype ('float64')
 for x in domi_regi['Domicílios particulares (2022)']:
  if x!=754:
    lista_coorec.append(x*1000)
  else:
    lista_coorec.append(x)
 domi_regi['Domicílios particulares (2022)']=lista_coorec
 domi_regi=domi_regi.drop(8)
 domi_regi_grap=px.bar(domi_regi, x="Região", y="Domicílios particulares (2022)", title="Domicílios    particulares por Região")




 return {
            'barras': fig.to_html(full_html=False),
            'piramide':fig2.to_html(full_html=False),
            'setor':popu_set.to_html(full_html=False),
            'domici': domi_regi_grap.to_html(full_html=False)
            }


   
