from flask import Flask, render_template, url_for
import pandas as pd
import numpy as np



import os
from grap import criando_grap



app=Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/indicadores")
def indicadores():
       print("Gerando gráficos...")
       graficos = criando_grap()
    
       if graficos:
         print("Gráficos gerados com sucesso!")
         return render_template('principais_indicadores.html',
           grap_etario=graficos['barras'],
           grap_piramid=graficos['piramide'],
           grap_setor=graficos['setor'],
           grap_domi=graficos['domici']
        )
      
@app.route("/sobre")
def sobre():
    return render_template("sobre.html")
    







if __name__=="__main__":
    app.run(debug=True)
