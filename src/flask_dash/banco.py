import mysql.connector
from mysql.connector import Error
import os # Importe a biblioteca 'os' para ler variáveis de ambiente
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env (ótimo para teste local)
load_dotenv()

# --- Configuração do Banco Lendo das Variáveis de Ambiente ---
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASS', ''), # Senha pode ser vazia localmente
    'database': os.getenv('DB_NAME', 'codewave_db')
}

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    config = DB_CONFIG.copy() # Copia para não alterar o original
    db_name = config.pop('database', None) # Tira o DB da config inicial
    
    try:
        # 1. Tenta conectar ao MySQL sem DB específico
        conn_no_db = mysql.connector.connect(**config)
        
        if db_name:
            # 2. Tenta conectar ao DB específico
            config['database'] = db_name
            conn_with_db = mysql.connector.connect(**config)
            return conn_with_db
            
        return conn_no_db
        
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        # Retorna a conexão sem DB (para o init_db poder criar o banco)
        if 'conn_no_db' in locals:
            return conn_no_db
        return None

def init_db():
    """
    Função para criar o banco e a tabela.
    """
    conn = None
    cursor = None
    try:
        # 1. Conecta ao MySQL (sem DB específico)
        conn_config_no_db = DB_CONFIG.copy()
        db_name = conn_config_no_db.pop('database') # Pega o nome do DB
        
        conn = mysql.connector.connect(**conn_config_no_db)
        if conn is None:
            print("Falha fatal: Não foi possível conectar ao MySQL.")
            return

        cursor = conn.cursor()
        
        # 2. Cria o banco de dados
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Banco de dados '{db_name}' verificado/criado.")
        
        # 3. Seleciona o banco de dados para a conexão
        conn.database = db_name
        
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
        # Pega uma conexão já com o database
        conn = mysql.connector.connect(**DB_CONFIG) 
        if conn is None or not conn.is_connected():
            print("Não foi possível conectar ao banco.")
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
            conn.rollback() 
        return False
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# --- Bloco de Execução Principal ---
if __name__ == '__main__':
    print("Executando script de inicialização do banco...")
    print(f"Conectando ao host: {DB_CONFIG['host']}...")
    init_db()
    print("Script de inicialização concluído.")
    input('Pressione Enter para fechar......')