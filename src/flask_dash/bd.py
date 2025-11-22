import mysql.connector
import os
def insercao_dados(nome_produto, valor):
    con = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),  
        port=3306,
        database=os.getenv('MYSQL_DATABASE'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD')
    )

    cursor = con.cursor()
    inserir_dados = "INSERT INTO review (comentario, nota) VALUES (%s, %s)"
    
    cursor.execute(inserir_dados, (nome_produto, valor))
    con.commit()
    con.close()
    cursor.close()


