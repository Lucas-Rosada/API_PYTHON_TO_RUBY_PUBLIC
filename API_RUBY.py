from flask import Flask, jsonify
import pymysql
import threading
import time
from pymysql.err import OperationalError
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SQL_HOST = 'localhost'
SQL_DATABASE = 'database_name'
SQL_USER = 'user_name'
SQL_PASSWORD = 'password'

cached_data = []
last_updated = 0

def get_db_connection():
    """Estabelece uma conexão com o banco de dados."""
    try:
        conn = pymysql.connect(
            host=SQL_HOST,
            user=SQL_USER,
            password=SQL_PASSWORD,
            database=SQL_DATABASE
        )
        return conn
    except OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def update_cache():
    """Atualiza o cache com os dados do banco a cada 3 minutos."""
    global cached_data, last_updated
    while True:
        conn = get_db_connection()
        if conn is None:
            continue
        
        cursor = conn.cursor()
        try:
            # Executa a consulta SQL para buscar os dados
            cursor.execute('SELECT * FROM coloca_sua_tabela_aq') 
            rows = cursor.fetchall()

            # Limpa e preenche o cache com os dados mais recentes
            cached_data = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
            last_updated = time.time() 
            
        except Exception as e:
            print(f"Erro ao executar a consulta: {e}")
        
        finally:
            cursor.close()
            conn.close()
        
        time.sleep(180)  

@app.route('/data', methods=['GET'])
def get_data():
    """Retorna os dados em cache ou uma mensagem de erro se o cache estiver vazio."""
    if not cached_data:
        return jsonify({"error": "Nenhum dado disponível."}), 500
    return jsonify(cached_data)

if __name__ == '__main__':

    threading.Thread(target=update_cache, daemon=True).start()
    
    app.run(host='0.0.0.0', port=5000, debug=True)