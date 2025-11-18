from flask import Flask, render_template, url_for, request
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
    
@app.route('/sobre')
def sobre():
  return render_template('sobre.html')

@app.route('/review',methods=['GET','POST'])
def review():
  return render_template('review.html')

    






if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)