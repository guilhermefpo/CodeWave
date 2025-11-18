from flask import Flask, render_template, url_for, request, redirect, flash
import pandas as pd
import numpy as np
from grap import criando_grap, grap_censo_e, criando_map

# Importa a função do seu script de banco
# (Certifique-se que o arquivo se chama banco.py e está na mesma pasta)
try:
    from banco import adicionar_avaliacao
except ImportError:
    print("="*50)
    print("AVISO: Não foi possível importar 'banco.py'.")
    print("Execute 'python banco.py' primeiro para criar o banco e a tabela.")
    print("="*50)
    # Define uma função placeholder para evitar que o app quebre
    def adicionar_avaliacao(nota, msg):
        print(f"Modo Falso: Avaliação ({nota}, '{msg}') não salva. 'banco.py' não encontrado.")
        return False

titulo = {
    'IN_INF': 'ENSINO INFANTIL',
    'IN_FUND': 'ENSINO FUNDAMENTAL',
    'IN_MED': 'ENSINO MEDIO'
}

app = Flask(__name__)

# Chave secreta é OBRIGATÓRIA para usar 'flash messages'
# Mude isso para uma string aleatória e segura
app.secret_key = 'sua-chave-secreta-muito-segura-aqui'

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
    return "Erro ao gerar gráficos", 500 # Adicionado um fallback

@app.route("/graficos", methods=['GET', 'POST'])
def graf():
    tipo = 'barras'
    regi = 'NORTE'
    esco = 'IN_INF'
    mapa = criando_map()
    mapa_no_site = mapa._repr_html_()

    censo = request.form.get('censo', 'Censo_d')
    grap = ''
    if censo == 'Censo_d':
        tipo = request.form.get('grafico', tipo)
        grape = criando_grap()
        grap = grape.get(tipo)
    elif censo == 'Censo_e':
        regi = request.form.get('regiao', regi)
        esco = request.form.get('escolas', esco)
        grap = grap_censo_e(regi, esco, titulo)

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

@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        # 1. Obter os dados do formulário
        nota = request.form.get('rating')
        comentario = request.form.get('comentario')
        
        # 2. Validar (verificar se a nota foi enviada)
        if not nota:
            # Informa o usuário se ele não selecionou uma nota
            # 'danger' é uma categoria do Bootstrap (vermelho)
            flash('Por favor, selecione uma avaliação de estrelas.', 'danger')
            return render_template('review.html') # Renderiza de novo com a msg de erro

        try:
            # Converte nota para inteiro
            nota_int = int(nota)
            
            # 3. Chamar a função do banco para salvar
            sucesso = adicionar_avaliacao(nota_int, comentario)
            
            if sucesso:
                # 4. Redirecionar para evitar reenvio do formulário (Padrão PRG)
                print("Avaliação salva com sucesso.")
                # 'success' é uma categoria do Bootstrap (verde)
                flash('Obrigado pelo seu feedback!', 'success')
                return redirect(url_for('review'))
            else:
                flash('Ocorreu um erro ao salvar seu feedback. Tente novamente.', 'danger')
        
        except ValueError:
            flash('Valor de avaliação inválido.', 'danger')
        except Exception as e:
            print(f"Erro na rota /review: {e}")
            flash('Um erro inesperado ocorreu. Tente novamente mais tarde.', 'danger')
        
        # Se algo falhar, apenas renderiza a página de review novamente
        return render_template('review.html')

    # 5. Se for GET, apenas mostra a página de review
    return render_template('review.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)