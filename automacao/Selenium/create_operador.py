import psycopg2
import logging
import time
import random
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from faker import Faker
from faker.providers import company

# Configurando o logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("selenium_actions")

# Configurando o Selenium WebDriver
service = webdriver.chrome.service.Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
faker = Faker()
faker.add_provider(company)
gera_email = faker.email()

def gerar_numero_aleatorio_4_digitos():
    return random.randint(1000, 9999)

def gerar_numero_aleatorio_10_digitos():
    return random.randint(1000000000, 9999999999)

# Funções úteis
def limpar_string(string):
    return string.split()[0]

# Verificação das variáveis de ambiente
login = os.getenv('LOGIN')
senha = os.getenv('SENHA')

email_gerado = faker.email(domain='servicenet.com.br')
email_sem_dominio = email_gerado.split('@')[0]

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

    # Navegação no menu
    driver.get("https://kronos.servicenet.dev.br/rede/operador/listar/")
    time.sleep(2)

    # Preenchimento do formulário
    novo = driver.find_element(By.ID, 'btn_novo_operador')
    novo.click()

    # Formulário principal
    nome = driver.find_element(By.ID, 'id_nome')
    nome.send_keys(email_sem_dominio)

    gera_matricula = gerar_numero_aleatorio_10_digitos()
    matricula = driver.find_element(By.ID, 'id_matricula')
    matricula.send_keys(gera_matricula)

    gera_login = gerar_numero_aleatorio_4_digitos()
    login = driver.find_element(By.ID, 'id_login')
    login.send_keys(gera_login)

    gera_senha = gerar_numero_aleatorio_4_digitos()
    senha = driver.find_element(By.ID, 'id_senha')
    senha.send_keys(gera_senha)
    confirma_senha = driver.find_element(By.ID, 'id_confirma_senha')
    confirma_senha.send_keys(gera_senha)

    # Formulário Smarth POS
    smarthpos = driver.find_element(By.ID, 'tab_smartpos_operador')
    smarthpos.click()

    email = driver.find_element(By.ID, 'id_email')
    email.send_keys(email_gerado)

    login_smartpos = driver.find_element(By.ID, 'id_login_smartpos')
    login_smartpos.send_keys(email_sem_dominio)

    senha_smartpos = driver.find_element(By.ID, 'id_senha_email')
    senha_smartpos.send_keys(gera_senha)

    confirma_senha_smartpos = driver.find_element(By.ID, 'id_confirma_senha_email')
    confirma_senha_smartpos.send_keys(gera_senha)

    time.sleep(2)

    # Formulário de vínculo
    vincular = driver.find_element(By.ID, 'tab_vincular_operador')
    vincular.click()

    flag_comum = driver.find_element(By.ID, 'id_tipo_0')
    flag_comum.click()

    dropdown_estabelecimento = driver.find_element(By.ID, "select2-id_id_estabelecimento-container")
    dropdown_estabelecimento.click()

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "select2-results__options")))

    option_text_estabelecimento = "000000000000001 - Testando monitor"

    option_locator_estabelecimento = f'//li[contains(text(), "{option_text_estabelecimento}")]'

    option_element_estabelecimento = driver.find_element(By.XPATH, option_locator_estabelecimento)
    option_element_estabelecimento.click()

    time.sleep(2)

    dropdown_loja = driver.find_element(By.ID, "select2-id_id_loja-container")
    dropdown_loja.click()

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "select2-results__option")))

    option_text_loja = "1 - TESTE MONITOR"
    option_locator_loja = f'//li[contains(text(), "{option_text_loja}")]'
    option_element_loja = driver.find_element(By.XPATH, option_locator_loja)
    option_element_loja.click()

    time.sleep(2)

    dropdown_terminal = driver.find_element(By.ID, "select2-id_id_terminal-container")
    dropdown_terminal.click()

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "select2-results__option")))

    option_text_terminal = "29046"
    option_locator_terminal = f'//li[contains(text(), "{option_text_terminal}")]'
    option_element_terminal = driver.find_element(By.XPATH, option_locator_terminal)
    option_element_terminal.click()

    time.sleep(2)

    salvar = driver.find_element(By.XPATH, '//*[@id="formoperador"]/button')
    salvar.click()

    time.sleep(2)

    # Conexão com banco de dados
    class Conexao:
        def __init__(self, host, port, db_name, db_user, db_pass):
            try:
                self._db = psycopg2.connect(
                    host=host, port=port, database=db_name, user=db_user, password=db_pass
                )
                self.cursor = self._db.cursor()
                self._db.autocommit = True
                logger.info(f"Conectado: {host}:{port}/{db_name}. User: {db_user}.")
            except Exception as e:
                logger.error(f"Erro ao conectar ao banco de dados: {e}")

        def close(self):
            self.cursor.close()
            logger.info("Conexão fechada.")

    class DBConnect:
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
                return self._cursor.fetchall()
            except Exception as e:
                logger.error(f"Erro ao executar query: {e}")
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
    query_operador = f"""
    SELECT id_operador, nome, login, ativo 
    FROM arrecada.operadores 
    WHERE nome = '{email_sem_dominio}'
    """


    resultados = connect.select(query_operador, return_type='dict')

    connect.close()


    for resultado in resultados:
        logger.info(f"ID operador: {resultado['id_operador']}, Nome: {resultado['nome']}, "
                    f"Login: {resultado['login']}, Ativo: {resultado['ativo']}, Cadastro realizado com sucesso!")


    # Exclusão de operador
    nome_excluir = driver.find_element(By.ID, 'id_nome')
    nome_excluir.send_keys(email_sem_dominio)

    pesquisar = driver.find_element(By.ID, 'fat-btn')
    pesquisar.click()

    time.sleep(2)


except Exception as e:
    logger.error(f"Ocorreu um erro durante a execução do script: {e}")

finally:
    logger.info(f"Cadastro realizado com sucesso")
    driver.quit()
