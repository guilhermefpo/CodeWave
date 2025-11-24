from flask import Flask, render_template, url_for, request, flash, redirect
from grap import criando_grap, grap_censo_e, criando_map
import os
from bd import insercao_dados






titulo = {
    'IN_INF': 'ENSINO INFANTIL',
    'IN_FUND': 'ENSINO FUNDAMENTAL',
    'IN_MED': 'ENSINO MEDIO'
}

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'chave_padrao_desenvolvimento')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/indicadores")
def indicadores():
    try:
        graficos = criando_grap()
        if graficos:
            return render_template('principais_indicadores.html',
                grap_etario=graficos['barras'],
                grap_piramid=graficos['piramide'],
                grap_setor=graficos['setor'],
                grap_domi=graficos['domici']
            )
    except Exception as e:
        print(f"Erro ao gerar indicadores: {e}")
    
    return "Erro ao carregar gráficos. Verifique os logs.", 500

@app.route("/graficos", methods=['GET', 'POST'])
def graf():
    # Valores padrão
    tipo = 'barras'
    regi = 'NORTE'
    esco = 'IN_INF'
    
    # Mapa
    try:
        mapa = criando_map()
        mapa_no_site = mapa._repr_html_()
    except Exception as e:
        print(f"Erro no mapa: {e}")
        mapa_no_site = "<h1>Erro ao carregar mapa</h1>"

    # Lógica do Filtro
    censo = request.form.get('censo', 'Censo_d')
    grap = ''
    
    if censo == 'Censo_d':
        # Recupera o tipo enviado pelo form, ou mantem o padrão 'barras'
        tipo = request.form.get('grafico', tipo)
        grape = criando_grap()
        grap = grape.get(tipo)
        
    elif censo == 'Censo_e':
        regi = request.form.get('regiao', regi)
        esco = request.form.get('escolas', esco)
        grap = grap_censo_e(regi, esco, titulo)

    # RETORNO CORRIGIDO: Adicionado 'tipo=tipo' para o HTML saber o que selecionar
    return render_template('graficos.html',
                           grap=grap,
                           regi=regi,
                           esco=esco,
                           titulo=titulo,
                           m=mapa_no_site,
                           censo=censo,
                           tipo=tipo) # <--- ISSO FALTAVA

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        nota = request.form.get('rating')
        comentario = request.form.get('comentario')

        if not nota:
            flash('Por favor, selecione uma estrela para avaliar.', 'warning')
             
            return redirect(url_for('review'))

    
        sucesso = insercao_dados(comentario,nota)
        if sucesso:
                flash('Obrigado! Seu feedback foi enviado com sucesso.', 'success')
                return redirect(url_for('review'))
        else:
                flash('Erro ao conectar ao banco de dados.', 'danger')
        

    return render_template('review.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)