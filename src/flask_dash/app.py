from flask import Flask, render_template, url_for, request
import pandas as pd
import numpy as np
from grap import criando_grap, grap_censo_e, criando_map

titulo={
    'IN_INF':'ENSINO INFANTIL',
    'IN_FUND':'ENSINO FUNDAMENTAL',
    'IN_MED':'ENSINO MEDIO'
}


app=Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/indicadores")
def indicadores():
       print("Gerando gráficos...")
       graficos = criando_grap()
    
       if graficos:
        
         return render_template('principais_indicadores.html',
           grap_etario=graficos['barras'],
           grap_piramid=graficos['piramide'],
           grap_setor=graficos['setor'],
           grap_domi=graficos['domici']
        )
      
@app.route("/graficos",methods=['GET','POST'])
def graf():
    tipo='barras'
    regi='NORTE'
    esco='IN_INF'
    mapa=criando_map()
    mapa_no_site=mapa._repr_html_()
    
    censo=request.form.get('censo','Censo_d')
    grap=''
    if censo=='Censo_d' :
        
         tipo=request.form.get('grafico',tipo)
         grape=criando_grap()
         grap=grape.get(tipo)
         
       
    elif censo=='Censo_e':
      
     
    
      regi=request.form.get('regiao',regi)
      esco=request.form.get('escolas',esco)
      grap=grap_censo_e(regi,esco,titulo)
      

        
      
      
    return render_template('graficos.html',
                       grap=grap,
                       regi=regi,
                       esco=esco,
                       titulo=titulo,
                       m=mapa_no_site,
                      
                       
                   
                     censo=censo) 
    







if __name__=="__main__":
    app.run(debug=True)
