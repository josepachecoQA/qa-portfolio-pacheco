import configparser
import psycopg2

def get_db_connection(config_file='db_config.ini'):
    # Carrega as configurações do arquivo de configuração
    config = configparser.ConfigParser()
    config.read(config_file)

    # Extrai as configurações da seção 'database'
    db_config = {
        'host': config.get('database', 'host'),
        'port': config.getint('database', 'port'),
        'dbname': config.get('database', 'dbname'),
        'user': config.get('database', 'user'),
        'password': config.get('database', 'password')
    }

    # Retorna a conexão ao banco de dados
    return psycopg2.connect(**db_config)
