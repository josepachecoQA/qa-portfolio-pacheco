import psycopg2
import logging
import time
import re
import random
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker
from faker.providers import company
from datetime import datetime

# Configurando o logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("selenium_actions")

# Configurando o Selenium WebDriver
service = webdriver.chrome.service.Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
faker = Faker()
faker.add_provider(company)

# Verificação das variáveis de ambiente
login = os.getenv('LOGIN')
senha = os.getenv('SENHA')

def limpar_string(string):
    string = re.sub(r'-', ' ', string)
    string = re.sub(r'[^\w\s]', '', string)
    return string.split()[0]

def gerar_numero_aleatorio_4_digitos():
    return random.randint(1000, 9999)


nome_arquivo_relatorio = "relatorio.txt"

if not login or not senha:
    raise EnvironmentError('As variáveis de ambiente LOGIN e SENHA devem estar definidas.')

# URL de acesso
url_login = "https://kronos.servicenet.dev.br/"

try:
    logger.info("Iniciando automação do Kronos...")

    # Acessar página de login
    driver.get(url_login)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'acceptCookiesButton')))
    aceite_cookie = driver.find_element(By.ID, 'acceptCookiesButton')
    aceite_cookie.click()
    search_bar_login = driver.find_element(By.ID, 'username')
    search_bar_login.send_keys(login)

    search_bar_password = driver.find_element(By.ID, "password")
    search_bar_password.send_keys(senha)

    search_button = driver.find_element(By.ID, 'login-btn')
    search_button.click()
    logger.info("Login realizado com sucesso.")
    time.sleep(2)

    # Navegando até o formulário de recolhedor
    driver.get("https://kronos.servicenet.dev.br/rede/recolhedor/listar/")

    novo = driver.find_element(By.ID, 'btn_novo_recolherdor')
    novo.click()

    # Preenchendo o formulário de recolhedor
    nome_aleatorio = limpar_string(faker.company())
    nome = driver.find_element(By.ID, 'id_nome')
    nome.send_keys(nome_aleatorio)
    
    login1 = gerar_numero_aleatorio_4_digitos()
    login = driver.find_element(By.ID, 'id_login')
    login.send_keys(login1)
    
    nome_impressao = driver.find_element(By.ID, 'id_nome_impressao')
    nome_impressao.send_keys('Teste impressao')
    
    senha = driver.find_element(By.ID, 'id_senha')
    senha.send_keys(login1)
    
    confirmar_senha = driver.find_element(By.ID, 'id_confirma_senha')
    confirmar_senha.send_keys(login1)
    
    time.sleep(1)

    salvar = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[5]/div[3]/form/button')
    salvar.click()

    logger.info("Formulário de recolhedor preenchido e enviado")
    time.sleep(2)

    # Iniciando conexão com banco de dados
    class Conexao(object):
        def __init__(self, host, port, db_name, db_user, db_pass):
            try:
                self._db = psycopg2.connect(host=host, port=port, database=db_name, user=db_user, password=db_pass)
                self.cursor = self._db.cursor()
                self._db.autocommit = True
                logger.info(f"Conectado: {host}:{port}/{db_name}. User: {db_user}.")
            except psycopg2.Error as e:
                logger.error(f"Erro ao conectar ao banco de dados: {e}")

        def close(self):
            self.cursor.close()
            logger.info("Conexão fechada.")

    class DBConnect(object):
        def __init__(self, DB_CONFIG):
            self._connection = Conexao(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                db_name=DB_CONFIG['db_name'],
                db_user=DB_CONFIG['user'],
                db_pass=DB_CONFIG['pass']
            )
            self._cursor = self._connection.cursor

        def select(self, sql, return_type=None):
            try:
                self._cursor.execute(sql)
                if return_type == 'dict':
                    return self._dictfetchall()
                else:
                    return self._cursor.fetchall()
            except psycopg2.Error as e:
                logger.error(f"Erro ao executar consulta SQL: {e}")
                return []

        def _dictfetchall(self):
            desc = self._cursor.description
            return [dict(zip([col[0] for col in desc], row)) for row in self._cursor.fetchall()]

    DB_CONFIG = {
        'host': os.environ.get('DB_HOST'),
        'port': int(os.environ.get('DB_PORT')),
        'db_name': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'pass': os.environ.get('DB_PASSWORD')
    }

    connect = DBConnect(DB_CONFIG)

    # Consulta no banco de dados
    query_perfil = f"""
    SELECT id_recolhedor, nome, login, id_arrecadadora
    FROM arrecada.recolhedores
    WHERE nome = '{nome_aleatorio}'
    """

    connect.close()

    resultados = connect.select(query_perfil, return_type='dict')

    for resultado in resultados:
        logger.info(f"ID Recolhedor: {resultado['id_recolhedor']}, Nome: {resultado['nome']}, "
                    f"Login: {resultado['login']}, ID Arrecadadora: {resultado['id_arrecadadora']}, "
                    f"Cadastro realizado com sucesso!")

    # Pesquisa para exclusão
    nome_pesquisa = driver.find_element(By.ID, 'id_nome')
    nome_pesquisa.send_keys(nome_aleatorio)
    pesquisar = driver.find_element(By.ID, 'fat-btn')
    pesquisar.click()
    time.sleep(1)
    excluir = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr/td[1]/div/a[2]')
    excluir.click()
    time.sleep(1)
    confirmar_exclusao = driver.find_element(By.ID, 'btnRemoverRecolhedor')
    confirmar_exclusao.click()
    logger.info("Recolhedor excluído com sucesso")
    time.sleep(2)

    connect = DBConnect(DB_CONFIG)


    query_perfil_excluido = f"""
    SELECT id_recolhedor, nome, login, id_arrecadadora
    FROM arrecada.recolhedores
    WHERE nome = '{nome_aleatorio}'
    """



    resultados_excluido = connect.select(query_perfil_excluido, return_type='dict')

    connect._connection.close()

    if not resultados_excluido:
        logger.info("Remoção realizada com sucesso!")
    else:
        logger.warning("Algo de errado aconteceu com a exclusão do recolhedor.")


    now = datetime.now()
    data_hora_atual = now.strftime("%d/%m/%Y %H:%M:%S")
    with open(nome_arquivo_relatorio, 'a') as file:
        file.write(f"{data_hora_atual} - Execução do script Criação Recolhedor concluída com sucesso.\n")

except Exception as e:
    logger.error(f"Ocorreu um erro durante a execução do script Criação Recolhedor: {e}")

    now = datetime.now()
    data_hora_atual = now.strftime("%d/%m/%Y %H:%M:%S")
    with open(nome_arquivo_relatorio, 'a') as file:
        file.write(f"{data_hora_atual} - Erro durante a execução do script: {e}\n")


finally:
    driver.quit()
    logger.info("Finalizando execução do script")
