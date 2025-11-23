import psycopg2
from psycopg2.extras import RealDictCursor
import logging
import os
import time

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

cnpj1 = '67.910.832/0001-16'

def cnpj_to_int(cnpj):
    # Remove caracteres não numéricos
    cnpj_numerico = ''.join(filter(str.isdigit, cnpj))
    
    # Converte para inteiro
    cnpj_int = int(cnpj_numerico)
    
    return cnpj_int

cnpj_inteiro = cnpj_to_int(cnpj1)
print(cnpj_inteiro)

time.sleep(2)

class DBConnect:
    def __init__(self, config):
        self.conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            dbname=config['dbname'],
            user=config['user'],
            password=config['password']
        )

    def select(self, query, return_type='tuple'):
        with self.conn.cursor(cursor_factory=RealDictCursor if return_type == 'dict' else None) as cur:
            cur.execute(query)
            return cur.fetchall()

DB_CONFIG = {
    'host': os.environ.get('DB_HOST'),
    'port': int(os.environ.get('DB_PORT')),
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD')
}
connect = DBConnect(DB_CONFIG)

# Geração do CNPJ para uso no cadastro e consulta
# cnpj = generate_valid_cnpj()
# Simulação do cadastro usando o CNPJ gerado
# Cadastro a ser feito na automação do Selenium
# ...

# Adiciona um atraso para garantir que o cadastro foi processado
time.sleep(10)  # Aguarda 10 segundos

# Consulta ao banco de dados para verificar se a loja foi criada
queryLoja = f"""
    SELECT nome_fantasia, numero_loja, momento_cadastro 
    FROM arrecada.loja_coban 
    WHERE cnpj = '{cnpj1}'
"""

try:
    resultados = connect.select(queryLoja, return_type='dict')
except Exception as e:
    logger.error(f"Erro ao executar a consulta: {e}")
    resultados = None

if resultados:
    for resultado in resultados:
        logger.info(f"Loja encontrada no banco de dados. Nome Fantasia: {resultado['nome_fantasia']}, Numero da loja: {resultado['numero_loja']}, Data de cadastro: {resultado['momento_cadastro']}")
else:
    logger.warning("A loja não foi encontrada no banco de dados.")