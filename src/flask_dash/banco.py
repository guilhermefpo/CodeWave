import mysql.connector
from mysql.connector import Error

# --- Configuração do Banco ---
# O app.py vai usar esta configuração para se conectar
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',       # Sua senha do MySQL (se houver)
    'database': 'codewave_db'
}

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    try:
        # Usa o **DB_CONFIG para "desempacotar" o dicionário
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        # Se falhar a conexão ao DB_CONFIG (ex: DB não existe),
        # tenta conectar sem o database para o init_db
        try:
            conn_no_db = mysql.connector.connect(
                host=DB_CONFIG['host'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password']
            )
            return conn_no_db
        except Error as e_no_db:
            print(f"Erro ao conectar ao MySQL (sem DB): {e_no_db}")
            return None

def init_db():
    """
    Função para criar o banco e a tabela.
    Execute isso como um script ANTES de rodar o app pela primeira vez:
    python banco.py
    """
    conn = None
    cursor = None
    try:
        # 1. Conecta ao MySQL (sem DB específico)
        conn = get_db_connection()
        if conn is None:
            print("Falha fatal: Não foi possível conectar ao MySQL.")
            return

        cursor = conn.cursor()
        
        # 2. Cria o banco de dados
        cursor.execute("CREATE DATABASE IF NOT EXISTS codewave_db")
        print("Banco de dados 'codewave_db' verificado/criado.")
        
        # 3. Seleciona o banco de dados para a conexão
        conn.database = 'codewave_db'
        
        # 4. Cria a tabela
        print("Criando Tabela 'avaliacao'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS avaliacao (
                id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                nota TINYINT NOT NULL CHECK(nota IN (1, 2, 3, 4, 5)),
                mensagem VARCHAR(250)
            )
        """)
        conn.commit()
        print("Tabela 'avaliacao' criada com sucesso!")
        
    except Error as e:
        print(f'Erro no init_db: {e}')
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def adicionar_avaliacao(nota, mensagem):
    """Adiciona um novo review ao banco de dados."""
    conn = None
    cursor = None
    try:
        # Pega uma conexão já com o database 'codewave_db'
        conn = mysql.connector.connect(**DB_CONFIG) 
        if conn is None or not conn.is_connected():
            print("Não foi possível conectar ao banco 'codewave_db'.")
            return False
            
        cursor = conn.cursor()
        query = "INSERT INTO avaliacao (nota, mensagem) VALUES (%s, %s)"
        cursor.execute(query, (nota, mensagem))
        conn.commit()
        print(f"Avaliação adicionada: {nota} estrelas, '{mensagem}'")
        return True
    except Error as e:
        print(f"Erro ao inserir avaliação: {e}")
        if conn:
            conn.rollback() # Desfaz a transação em caso de erro
        return False
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# --- Bloco de Execução Principal ---
if __name__ == '__main__':
    # Corrigido: 'if __name__ == '__main__':'
    print("Executando script de inicialização do banco...")
    init_db()
    print("Script de inicialização concluído.")
    input('Pressione Enter para fechar......')