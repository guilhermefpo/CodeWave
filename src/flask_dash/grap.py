import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
import geopandas as gpd
import folium
import glob
from geopandas.io.file import fiona
import json
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

# grafico de população por região 
 lista_popu_certa=[]
 popu_regi=df[3]
 popu_regi['População (2022)']=popu_regi['População (2022)'].astype('float64')

 for x in popu_regi['População (2022)']:
 
    lista_popu_certa.append(x*1000)
  
 popu_regi['População (2022)']=lista_popu_certa
 popu_regi=popu_regi.drop(8)
 popu_regi_grap=px.bar(popu_regi, x="Região", y="População (2022)", title="População por Região")

 



 return {
            'barras': fig.to_html(full_html=False),
            'piramide':fig2.to_html(full_html=False),
            'setor':popu_set.to_html(full_html=False),
            'domici': domi_regi_grap.to_html(full_html=False),
            'popu_regi':popu_regi_grap.to_html(full_html=False)
            }


   
def grap_censo_e(regiao,escolas,titulo):
           df = pd.read_csv('dados_municipio.csv',

                 sep=";", on_bad_lines = 'skip', encoding='Latin 1')
           bairros_sjc_certos = [
    "JARDIM AMÉRICA",
    "VILA BETÂNIA",
    "RESIDENCIAL PINHEIRINHO DOS PALMARES II",
    "JARDIM ALVORADA",
    "CAMPO DOS ALEMÃES",
    "JARDIM AMÉRICA",
    "JARDIM SÃO DIMAS",
    "ALTO DA PONTE",
    "VILA MONTERREY",
    "LOTEAMENTO SANTA EDWIGES",
    "CONJUNTO RESIDENCIAL GALO BRANCO",
    "RESIDENCIAL PINHEIRINHO DOS PALMARES II",
    "JARDIM ESPLANADA II",
    "JARDIM ORIENTE",
    "BAIRRINHO",
    "SETVILLE ALTOS DE SÃO JOSÉ",
    "VILA BETÂNIA",
    "JARDIM SUL",
    "JARDIM SATÉLITE",
    "JARDIM NOVA AMÉRICA",
    "JARDIM ORIENTE",
    "JARDIM DAS INDÚSTRIAS",
    "PARQUE NOVO HORIZONTE",
    "JARDIM VENEZA",
    "MONTE CASTELO",
    "PARQUE INDUSTRIAL",
    "JARDIM LIMOEIRO",
    "JARDIM PARAÍSO",
    "JARDIM ESPLANADA II",
    "RESIDENCIAL UNIÃO",
    "JARDIM ISMÊNIA",
    "JARDIM DAS INDÚSTRIAS",
    "JARDIM MARGARETH",
    "PUTIM",
    "SÃO JOSÉ DOS CAMPOS",
    "URBANOVA",
    "JARDIM PAULISTA",
    "CONJUNTO RESIDENCIAL VALE DOS PINHEIROS",
    "CIDADE MORUMBI",
    "JARDIM NOVA AMÉRICA",
    "BOSQUE DOS EUCALIPTOS",
    "JARDIM DAS PAINEIRAS II",
    "JARDIM MESQUITA",
    "VILA IRACEMA",
    "CONDOMÍNIO RESIDENCIAL MÔNACO",
    "JARDIM SANTA HERMÍNIA",
    "JARDIM SÃO DIMAS",
    "JARDIM ESPLANADA II",
    "PORTAL DOS PÁSSAROS",
    "JARDIM DAS COLINAS",
    "JARDIM ESPLANADA",
    "JARDIM IMPERIAL",
    "JARDIM SANTA HERMÍNIA",
    "SETVILLE ALTOS DE SÃO JOSÉ",
    "CENTRO",
    "CONJUNTO RESIDENCIAL TRINTA E UM DE MARÇO",
    "PARQUE NOVO HORIZONTE",
    "JARDIM ORIENTE",
    "JARDIM VALPARAÍBA",
    "CIDADE MORUMBI",
    "CHÁCARAS POUSADA DO VALE",
    "ALTO DA PONTE",
    "RESIDENCIAL ARMANDO MOREIRA RIGHI",
    "CONJUNTO PAPA JOÃO PAULO II",
    "VILA DO TESOURO",
    "CAMPO DOS ALEMÃES",
    "JARDIM SATÉLITE",
    "VILA TATETUBA",
    "MONTE CASTELO",
    "CENTRO",
    "JARDIM SÃO JOSÉ II",
    "BOSQUE DOS EUCALIPTOS",
    "JARDIM MOTORAMA",
    "JARDIM AMÉRICA",
    "BOA VISTA",
    "VILA SÃO GERALDO",
    "VILA SINHA",
    "MONTE CASTELO",
    "VILA CÂNDIDA",
    "JARDIM SATÉLITE",
    "VILA INDUSTRIAL",
    "JARDIM DA GRANJA",
    "EUGÊNIO DE MELO",
    "VILA NAIR",
    "CENTRO",
    "ALTO DA PONTE",
    "VILA PAIVA",
    "SANTANA",
    "CENTRO DISTRITO DE SÃO FRANCISCO XAVIER",
    "SANTANA",
    "PARQUE INDUSTRIAL",
    "JARDIM SÃO DIMAS",
    "VILA DAS ACÁCIAS",
    "CENTRO",
    "MONTE CASTELO",
    "VILA ALEXANDRINA",
    "VILA TATETUBA",
    "JARDIM SÃO DIMAS",
    "CAMPOS DE SÃO JOSÉ",
    "MONTE CASTELO",
    "JARDIM ANHEMBÍ",
    "JARDIM SATÉLITE",
    "CHÁCARAS REUNIDAS",
    "VILA DO TESOURO",
    "JARDIM IMPERIAL",
    "BUQUIRINHA",
    "JARDIM SATÉLITE",
    "JARDIM AMERICANO",
    "PARQUE NOVO HORIZONTE",
    "JARDIM ORIENTE",
    "CONJUNTO RESIDENCIAL TRINTA E UM DE MARÇO",
    "VILA SÃO BENTO",
    "CIDADE MORUMBI",
    "VALE DOS PINHEIROS",
    "VILA INDUSTRIAL",
    "CONJUNTO RESIDENCIAL ELMANO FERREIRA VELOSO",
    "PARQUE INDUSTRIAL",
    "BOSQUE DOS EUCALIPTOS",
    "VILA IRACEMA",
    "JARDIM SATÉLITE",
    "VILA ADYANA",
    "CIDADE VISTA VERDE",
    "VILA INDUSTRIAL",
    "VILA NOVA CONCEIÇÃO",
    "ALTO DA PONTE",
    "JARDIM DA GRANJA",
    "JARDIM DAS INDÚSTRIAS",
    "JARDIM OSWALDO CRUZ",
    "JARDIM SATÉLITE",
    "PARQUE INDUSTRIAL",
    "JARDIM PARAÍSO DO SOL",
    "JARDIM DAS INDÚSTRIAS",
    "JARDIM ALTOS DE SANTANA",
    "BUQUIRINHA",
    "JARDIM ANHEMBÍ",
    "JARDIM LIMOEIRO",
    "CONJUNTO RESIDENCIAL DOM PEDRO I",
    "JARDIM SÃO JUDAS TADEU",
    "JARDIM POR DO SOL",
    "BOSQUE DOS EUCALIPTOS",
    "JARDIM SOUTO",
    "JARDIM SÃO LEOPOLDO",
    "JARDIM ALTOS DE SANTANA",
    "VILA INDUSTRIAL",
    "CONJUNTO RESIDENCIAL GALO BRANCO",
    "CONJUNTO RESIDENCIAL DOM PEDRO I",
    "CAMPOS DE SÃO JOSÉ",
    "CHÁCARAS POUSADA DO VALE",
    "VILA MARIA",
    "CAMPOS DE SÃO JOSÉ",
    "RIO COMPRIDO",
    "CONJUNTO RESIDENCIAL VALE DOS PINHEIROS",
    "JARDIM COLONIAL",
    "CENTRO",
    "PARQUE NOVA ESPERANÇA",
    "JARDIM DAS CEREJEIRAS",
    "PARQUE INTERLAGOS",
    "BOSQUE DOS EUCALIPTOS",
    "VILA ICARAÍ",
    "VILA ADYANA",
    "JARDIM SANTA MATILDE",
    "JARDIM TORRÃO DE OURO",
    "JARDIM ESPLANADA",
    "FREITAS",
    "JARDIM SÃO JOSÉ II",
    "JARDIM SATÉLITE",
    "PARQUE INDUSTRIAL",
    "JARDIM ORIENTE",
    "JARDIM VALE DO SOL",
    "SANTANA",
    "JARDIM SÃO DIMAS",
    "JARDIM MOTORAMA",
    "JARDIM DAS INDÚSTRIAS",
    "SANTANA",
    "VILA MARIA",
    "JARDIM AEROPORTO",
    "CONJUNTO RESIDENCIAL TRINTA E UM DE MARÇO",
    "VILA TATETUBA",
    "VILA NOVA CRISTINA",
    "JARDIM SATÉLITE",
    "PARQUE NOVO HORIZONTE",
    "JARDIM ESTORIL",
    "VILA INDUSTRIAL",
    "CIDADE MORUMBI",
    "SANTANA",
    "BOSQUE DOS EUCALIPTOS",
    "JARDIM SANTA MADALENA",
    "CHÁCARAS REUNIDAS",
    "JARDIM VENEZA",
    "JARDIM SANTA INÊS I",
    "JARDIM DAS FLORES",
    "JARDIM SATÉLITE",
    "JARDIM DA GRANJA",
    "EUGÊNIO DE MELO",
    "JARDIM UIRÁ",
    "SANTANA",
    "JARDIM SÃO VICENTE",
    "VILA SÃO GERALDO",
    "VILA SÃO BENTO",
    "ALTO DA PONTE",
    "CAMPO DOS ALEMÃES",
    "JARDIM SANTO ONOFRE",
    "JARDIM SANTA FÉ",
    "JARDIM TELESPARK",
    "JARDIM AMERICANO",
    "JARDIM SANTA INÊS II",
    "JARDIM SÃO DIMAS",
    "VILA PAIVA",
    "VILA DO TESOURO",
    "MONTE CASTELO",
    "VILA VENEZIANI",
    "JARDIM COPACABANA",
    "JARDIM LIMOEIRO",
    "VILA SÃO PEDRO",
    "JARDIM VALPARAÍBA",
    "BOSQUE DOS EUCALIPTOS",
    "JARDIM APOLO I",
    "VILA ADYANA",
    "BOSQUE DOS EUCALIPTOS",
    "CENTRO",
    "JARDIM DAS COLINAS",
    "CENTRO",
    "CENTRO",
    "CENTRO",
    "JARDIM ESPLANADA",
    "SANTANA",
    "JARDIM ESPLANADA",
    "CIDADE VISTA VERDE",
    "URBANOVA",
    "TAMOIOS",
    "PERNAMBUCANA",
    "JARDIM SÃO DIMAS",
    "JARDIM SÃO DIMAS",
    "JARDIM NOVA AMÉRICA",
    "JARDIM ESPLANADA",
    "JARDIM SERIMBURA",
    "JARDIM ESPLANADA",
    "VILA EMA",
    "URBANOVA",
    "JARDIM ESPLANADA",
    "BOSQUE DOS EUCALIPTOS",
    "BOSQUE DOS EUCALIPTOS",
    "JARDIM DAS INDÚSTRIAS",
    "VILA ADYANA",
    "URBANOVA",
    "CIDADE VISTA VERDE",
    "VILA BETÂNIA",
    "FLORADAS DE SÃO JOSÉ",
    "RESIDENCIAL SOL NASCENTE",
    "BOSQUE DOS EUCALIPTOS",
    "SANTANA",
    "VILA INDUSTRIAL",
    "PARQUE INDUSTRIAL",
    "JARDIM ORIENTE",
    "JARDIM PORTUGAL",
    "FLORADAS DE SÃO JOSÉ",
    "VILA UNIDOS",
    "VILA BELA VISTA",
    "JARDIM AQUARIUS",
    "JARDIM SATÉLITE",
    "JARDIM ORIENTE",
    "VILA ALEXANDRINA",
    "JARDIM ESPLANADA",
    "VISTA VERDE",
    "JARDIM ESPLANADA",
    "JARDIM SATÉLITE",
    "JARDIM ISMÊNIA",
    "MONTE CASTELO",
    "JARDIM AMÉRICA",
    "VILA RUBI",
    "JARDIM SATÉLITE",
    "JARDIM DAS INDÚSTRIAS",
    "CHÁCARAS SÃO JOSÉ",
    "JARDIM NOVA AMÉRICA",
    "JARDIM AMÉRICA",
    "VILA EMA",
    "CONJUNTO RESIDENCIAL TRINTA E UM DE MARÇO",
    "JARDIM ISMÊNIA",
    "JARDIM OSWALDO CRUZ",
    "JARDIM SÃO DIMAS",
    "MONTE CASTELO",
    "CONJUNTO RESIDENCIAL GALO BRANCO",
    "JARDIM SATÉLITE",
    "JARDIM SERIMBURA",
    "CAMPOS DE SÃO JOSÉ",
    "URBANOVA",
    "MONTE CASTELO",
    "PARQUE INTERLAGOS",
    "VILA DO TESOURO",
    "VILA MARIA",
    "VILA TATETUBA",
    "CONJUNTO RESIDENCIAL GALO BRANCO",
    "PARQUE NOVO HORIZONTE",
    "ALTO DA PONTE",
    "JARDIM VALPARAÍBA",
    "CIDADE MORUMBI",
    "CAMPO DOS ALEMÃES",
    "VILA SÃO BENTO",
    "CONJUNTO RESIDENCIAL TRINTA E UM DE MARÇO",
    "JARDIM ORIENTE",
    "CONJUNTO HABITACIONAL PAPA JOÃO PAULO II",
    "JARDIM ALTOS DE SANTANA",
    "CHÁCARAS POUSADA DO VALE",
    "JARDIM SÃO JUDAS TADEU",
    "CAMPO DOS ALEMÃES",
    "RESIDENCIAL UNIÃO",
    "JARDIM CRUZEIRO DO SUL",
    "VILA ADYANA",
    "VILA BETÂNIA",
    "FLORADAS DE SÃO JOSÉ",
    "JARDIM DAS INDÚSTRIAS",
    "CENTRO",
    "JARDIM NOVA AMÉRICA",
    "CONJUNTO RESIDENCIAL GALO BRANCO",
    "BOSQUE DOS EUCALIPTOS",
    "CONJUNTO RESIDENCIAL GALO BRANCO",
    "JARDIM TORRÃO DE OURO",
    "PARQUE NOVO HORIZONTE",
    "JARDIM TELESPARK",
    "JARDIM MARIANA I",
    "JARDIM DAS CEREJEIRAS",
    "RESIDENCIAL BOSQUE DOS IPÊS",
    "SÃO FRANCISCO XAVIER",
    "CENTRO",
    "BOSQUE DOS EUCALIPTOS",
    "JARDIM DAS INDÚSTRIAS",
    "PARQUE INDUSTRIAL",
    "JARDIM DAS INDÚSTRIAS",
    "JARDIM SÃO JOSÉ II",
    "RESIDENCIAL TATETUBA",
    "JARDIM DA GRANJA",
    "VILA SÃO GERALDO",
    "JARDIM SATÉLITE",
    "RESIDENCIAL UNIÃO",
    "VILA MARIA",
    "CAMPO DOS ALEMÃES",
    "JARDIM MARIANA II",
    "BOSQUE DOS EUCALIPTOS",
    "VILA INDUSTRIAL",
    "VILA INDUSTRIAL",
    "CAPUAVA",
    "VILA INDUSTRIAL",
    "CONJUNTO RESIDENCIAL DOM PEDRO I",
    "JARDIM PARAÍSO DO SOL",
    "RESIDENCIAL BOSQUE DOS IPÊS",
    "VILA EMA",
    "VILA EMA",
    "JARDIM TORRÃO DE OURO",
    "CIDADE MORUMBI",
    "RESIDENCIAL JATOBÁ",
    "JARDIM ESPLANADA",
    "CONJUNTO RESIDENCIAL VALE DOS PINHEIROS",
    "JARDIM ESPLANADA",
    "JARDIM DAS INDÚSTRIAS",
    "URBANOVA",
    "PARQUE RESIDENCIAL AQUARIUS",
    "JARDIM PARARANGABA",
    "JARDIM ESPLANADA",
    "JARDIM TELESPARK",
    "EUGÊNIO DE MELO",
    "PARQUE RESIDENCIAL FLAMBOYANT",
    "MONTE CASTELO",
    "JARDIM ISMÊNIA",
    "JARDIM AMÉRICA",
    "JARDIM SATÉLITE",
    "JARDIM SATÉLITE",
    "JARDIM PORTUGAL",
    "JARDIM CASTANHEIRA",
    "JARDIM UIRÁ",
    "RIO COMPRIDO",
    "JARDIM AMÉRICA",
    "CENTRO",
    "FREITAS",
    "CONJUNTO RESIDENCIAL TRINTA E UM DE MARÇO",
    "BOSQUE DOS EUCALIPTOS",
    "JARDIM SATÉLITE",
    "JARDIM SATÉLITE",
    "JARDIM AMERICANO",
    "URBANOVA",
    "JARDIM ORIENTE",
    "JARDIM SANTA INÊS III",
    "JARDIM DAS INDÚSTRIAS",
    "JARDIM DAS INDÚSTRIAS",
    "CONJUNTO RESIDENCIAL TRINTA E UM DE MARÇO",
    "RESIDENCIAL GAZZO",
    "SANTANA",
    "VILA DAS ACÁCIAS",
    "BOSQUE DOS EUCALIPTOS",
    "ALTO DA PONTE",
    "CAMPO DOS ALEMÃES",
    "PARQUE INDUSTRIAL",
    "JARDIM RODOLFO",
    "PUTIM",
    "CENTRO",
    "CAMPO DOS ALEMÃES",
    "CONJUNTO RESIDENCIAL DOM PEDRO I",
    "CAMPOS DE SÃO JOSÉ",
    "PORTAL DE MINAS",
    "PARQUE INDUSTRIAL",
    "PARQUE INDUSTRIAL",
    "EUGÊNIO DE MELO",
    "EUGÊNIO DE MELO",
    "JARDIM SATÉLITE",
    "JARDIM DIAMANTE",
    "JARDIM REPÚBLICA",
    "JARDIM REPÚBLICA",
    "JARDIM SANTA LUZIA",
    "ALTOS DA VILA PAIVA",
    "JARDIM SATÉLITE",
    "CIDADE MORUMBI",
    "VILA TATETUBA",
    "JARDIM ESPLANADA",
    "VILA INDUSTRIAL",
    "PARQUE INDUSTRIAL",
    "JARDIM PAULISTA",
    "JARDIM ESPLANADA II",
    "URBANOVA",
    "JARDIM ESPLANADA II",
    "JARDIM ESPLANADA",
    "JARDIM SÃO JOSÉ II",
    "JARDIM SÃO DIMAS",
    "JARDIM DAS INDÚSTRIAS",
    "VILA INDUSTRIAL",
    "MONTE CASTELO",
    "BOSQUE DOS EUCALIPTOS",
    "JARDIM DAS CEREJEIRAS",
    "RESIDENCIAL FREI GALVÃO",
    "RESIDENCIAL ARMANDO MOREIRA RIGHI",
    "CIDADE MORUMBI",
    "JARDIM SATÉLITE",
    "SANTANA",
    "PARQUE INTERLAGOS",
    "EUGÊNIO DE MELO",
    "JARDIM SÃO VICENTE",
    "JARDIM SERIMBURA",
    "JARDIM DAS INDÚSTRIAS",
    "JARDIM ESPLANADA",
    "CENTRO",
    "CENTRO",
    "BOSQUE DOS EUCALIPTOS",
    "JARDIM SATÉLITE",
    "MONTE CASTELO",
    "EUGÊNIO DE MELO",
    "JARDIM IMPERIAL",
    "PARQUE RESIDENCIAL AQUARIUS",
    "CENTRO",
    "JARDIM SANTA HERMÍNIA",
    "CONJUNTO RESIDENCIAL GALO BRANCO",
    "CIDADE MORUMBI",
    "CASTANHEIROS",
    "CENTRO",
    "JARDIM DAS INDÚSTRIAS",
    "PUTIM",
    "BOSQUE DOS EUCALIPTOS",
    "JARDIM SÃO JUDAS TADEU",
    "JARDIM DAS FLORES",
    "JARDIM NOVA MICHIGAN",
    "JARDIM SANTA INÊS II",
    "JARDIM UIRÁ",
    "JARDIM DAS INDÚSTRIAS",
    "JARDIM NOVA DETROIT",
    "FREITAS",
    "CIDADE MORUMBI",
    "CIDADE MORUMBI",
    "JARDIM SANTA HERMÍNIA",
    "BOM RETIRO",
    "JARDIM DAS CEREJEIRAS",
    "CAMPO DOS ALEMÃES",
    "JARDIM SANTA INÊS I",
    "CIDADE VISTA VERDE",
    "JARDIM CASTANHEIRA",
    "JARDIM VALE DO SOL",
    "BOSQUE DOS EUCALIPTOS",
    "CIDADE MORUMBI",
    "CAMPO DOS ALEMÃES",
    "CONJUNTO RESIDENCIAL GALO BRANCO",
    "CONJUNTO RESIDENCIAL DOM PEDRO I",
    "CAMPO DOS ALEMÃES",
    "JARDIM SÃO LEOPOLDO",
    "JARDIM SÃO JUDAS TADEU",
    "VILA NOVA CRISTINA",
    "MONTE CASTELO"
]
           bairros_por_regiao = {
    "SUL": [
        "JARDIM AMÉRICA", "CAMPO DOS ALEMÃES", "JARDIM VENEZA", "LOTEAMENTO SANTA EDWIGES",
        "JARDIM ORIENTE", "JARDIM SUL", "JARDIM SATÉLITE", "PARQUE INDUSTRIAL",
        "JARDIM PARAÍSO", "RESIDENCIAL UNIÃO", "CIDADE MORUMBI", "BOSQUE DOS EUCALIPTOS",
        "JARDIM MESQUITA", "JARDIM IMPERIAL", "CONJUNTO RESIDENCIAL TRINTA E UM DE MARÇO",
        "CONJUNTO PAPA JOÃO PAULO II", "VILA NAIR", "VILA DAS ACÁCIAS", "JARDIM ANHEMBI",
        "CHÁCARAS REUNIDAS", "VILA SÃO BENTO", "CONJUNTO RESIDENCIAL ELMANO VELOSO",
        "VILA NOVA CONCEIÇÃO", "CONJUNTO RESIDENCIAL DOM PEDRO I", "RIO COMPRIDO",
        "JARDIM COLONIAL", "PARQUE INTERLAGOS", "TORRÃO DE OURO", "JARDIM AEROPORTO",
        "JARDIM ESTORIL", "FLORADAS DE SÃO JOSÉ", "RESIDENCIAL SOL NASCENTE",
        "PARQUE INDUSTRIAL", "JARDIM PORTUGAL", "JARDIM CRUZEIRO DO SUL",
        "RESIDENCIAL GAZZO", "JARDIM REPÚBLICA","RESIDENCIAL BOSQUE DOS IPÊS","CAPUAVA","CONJUNTO RESIDENCIAL ELMANO FERREIRA VELOSO","JARDIM VALE DO SOL"
    ],

    "CENTRO": [
        "VILA BETÂNIA", "JARDIM SÃO DIMAS", "JARDIM ESPLANADA II", "JARDIM NOVA AMÉRICA",
        "MONTE CASTELO", "JARDIM MARGARETH", "CENTRO", "VILA MARIA", "JARDIM PAULISTA",
        "CONJUNTO RESIDENCIAL VALE DOS PINHEIROS", "JARDIM ESPLANADA", "JARDIM SÃO JOSÉ II",
        "VALE DOS PINHEIROS", "VILA ADYANA", "JARDIM OSWALDO CRUZ", "VILA ICARAÍ",
        "JARDIM SANTA MADALENA", "VILA SÃO PEDRO", "JARDIM APOLO I", "JARDIM SERIMBURA",
        "VILA EMA", "VILA BELA VISTA","VILA RUBI"
    ],

    "SUDESTE": [
        "RESIDENCIAL PINHEIRINHO DOS PALMARES II", "SETVILLE ALTOS DE SÃO JOSÉ", "PUTIM",
        "PORTAL DOS PÁSSAROS", "JARDIM DA GRANJA", "JARDIM SÃO JUDAS TADEU", "JARDIM SOUTO",
        "JARDIM SÃO LEOPOLDO", "JARDIM UIRÁ", "JARDIM SANTO ONOFRE", "JARDIM SANTA FÉ",
        "TAMOIOS", "CHÁCARAS SÃO JOSÉ", "RESIDENCIAL JATOBÁ", "PARQUE RESIDENCIAL FLAMBOYANT",
        "JARDIM SANTA LUZIA","VILA IRACEMA","PERNAMBUCANA"
    ],

    "OESTE": [
        "JARDIM ALVORADA", "JARDIM DAS INDÚSTRIAS", "JARDIM LIMOEIRO", "URBANOVA",
        "CONDOMÍNIO RESIDENCIAL MÔNACO", "JARDIM DAS COLINAS", "JARDIM POR DO SOL",
        "JARDIM AQUÁRIUS", "PARQUE RESIDENCIAL AQUÁRIUS"
    ],

    "NORTE": [
        "ALTO DA PONTE", "BOA VISTA", "VILA SÃO GERALDO", "VILA SINHÁ", "VILA CÂNDIDA",
        "VILA PAIVA", "SANTANA", "CENTRO DISTRITO DE SÃO FRANCISCO XAVIER", "VILA ALEXANDRINA",
        "BUQUIRINHA", "JARDIM ALTOS DE SANTANA", "JARDIM SANTA MATILDE", "FREITAS",
        "VILA NOVA CRISTINA", "JARDIM TELESPARK", "VILA VENEZIANI", "VILA UNIDOS",
        "PORTAL DE MINAS", "ALTOS DA VILA PAIVA",""
    ],

    "LESTE": [
        "VILA MONTERREY", "CONJUNTO RESIDENCIAL GALO BRANCO", "BAIRRINHO",
        "PARQUE NOVO HORIZONTE", "JARDIM ISMÊNIA", "JARDIM DAS PAINEIRAS II",
        "JARDIM SANTA HERMÍNIA", "JARDIM VALPARAÍBA", "CHÁCARAS POUSADA DO VALE",
        "RESIDENCIAL ARMANDO MOREIRA RIGHI", "VILA TESOURO", "VILA TATETUBA",
        "JARDIM MOTORAMA", "VILA INDUSTRIAL", "EUGÊNIO DE MELO", "CAMPOS DE SÃO JOSÉ",
        "JARDIM AMERICANO", "CIDADE VISTA VERDE", "JARDIM PARAÍSO DO SOL",
        "PARQUE NOVA ESPERANÇA", "JARDIM DAS CEREJEIRAS", "JARDIM SANTA INÊS I",
        "JARDIM DAS FLORES", "JARDIM SÃO VICENTE", "JARDIM SANTA INÊS II",
        "JARDIM COPACABANA", "VISTA VERDE", "JARDIM NOVA DETROIT", "JARDIM MARIANA I",
        "JARDIM MARIANA II", "JARDIM PARARANGABA", "JARDIM CASTANHEIRA",
        "JARDIM SANTA INÊS III", "JARDIM RODOLFO", "JARDIM DIAMANTE",
        "RESIDENCIAL FREI GALVÃO", "CASTANHEIROS", "JARDIM NOVA MICHIGAN", "BOM RETIRO","RESIDENCIAL TATETUBA","VILA DO TESOURO"
    ]
}
           df['NO_BAIRRO']=bairros_sjc_certos
           if escolas:
              filtro=df[df[escolas]==1]
              filtro_centro=filtro[filtro['NO_BAIRRO'].isin(bairros_por_regiao[regiao])]
              filtro_centro.rename(columns={'NO_MUNICIPIO': 'MUNICIPIO', 'NO_BAIRRO': 'BAIRRO'}, inplace=True)
              bairros_quant=filtro_centro['BAIRRO'].value_counts().reset_index()
              bairros_quant.collumns=['BAIRRO','ESCOLAS']

              grap = px.bar(bairros_quant, x="BAIRRO", y="count", title=f"Quantidade de escolas com {titulo[escolas]} na região {regiao}")
           return grap.to_html(full_html=False)


def criando_map():
  ZonaLeste='ZonaLeste.kml'
  ZL = gpd.read_file(ZonaLeste)
   
  ZonaCentral='ZonaCentral.kml'
  ZC = gpd.read_file(ZonaCentral)
   
  ZonaSul='ZonaSul.kml'
  ZS = gpd.read_file(ZonaSul)
   
  ZonaSudeste='ZonaSudeste.kml'
  ZSD = gpd.read_file(ZonaSudeste)
   
  ZonaNorte='ZonaNorte.kml'
  ZN = gpd.read_file(ZonaNorte)
   
  ZonaOeste='ZonaOeste.kml'
  ZO = gpd.read_file(ZonaOeste)
   
  limite_municipal='LimiteMunicipal.kml'
  LM = gpd.read_file(limite_municipal)
  
  
  
  
  
  
  
  
  m=folium.Map(location=[-23.216318439443732, -45.893426564928276], zoom_start=12, tiles="cartodb positron")
  folium.GeoJson(ZN).add_to(m)
  folium.GeoJson(LM).add_to(m)
  folium.GeoJson(ZO).add_to(m)
  folium.GeoJson(ZS).add_to(m)
  folium.GeoJson(ZC).add_to(m)
  folium.GeoJson(ZSD).add_to(m)
  folium.GeoJson(ZL).add_to(m)
  folium.GeoJson(
      ZN,
      style_function=lambda feature:{
          'fillColor': 'green',
          'color': 'black',
          'weight': 2,
          'fillOpacity': 0.5
      }
  ).add_to(m)
  folium.GeoJson(
      ZO,
      style_function=lambda feature: {
          'fillColor': 'blue',
          'color': 'black',
          'weight': 2,
          'fillOpacity': 0.5
      }).add_to(m)
  folium.GeoJson(
      ZS,
      style_function=lambda feature: {
          'fillColor': 'yellow',
          'color': 'black',
          'weight': 2,
          'fillOpacity': 0.5
      }).add_to(m)
  folium.GeoJson(
      ZC,
      style_function=lambda feature: {
          'fillColor': 'OrangeRed',
          'color': 'black',
          'weight': 2,
          'fillOpacity': 0.5
      }).add_to(m)
  folium.GeoJson(
      ZSD,
      style_function=lambda feature: {
          'fillColor': 'purple',
          'color': 'black',
          'weight': 2,
          'fillOpacity': 0.5
      }).add_to(m)
  folium.GeoJson(
      ZL,
      style_function=lambda feature: {
          'fillColor': 'red',
          'color': 'black',
          'weight': 2,
          'fillOpacity': 0.5
      }).add_to(m)
  
  return m

