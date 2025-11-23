import psycopg2

def pega_conexao_bd():
    """Função para estabelecer conexão com o banco de dados PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host="",
            database="",
            user="",
            password="",
            port=""
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar no banco de dados: {e}")
        return None

        
