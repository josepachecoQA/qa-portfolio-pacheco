import psycopg2
import logging
import time
import re
import os
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
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

# Verificação das variáveis de ambiente
login = os.getenv('LOGIN')
senha = os.getenv('SENHA')

def limpar_string(string):
    string = re.sub(r'-', ' ', string)
    string = re.sub(r'[^\w\s]', '', string)
    return string.split()[0]

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

    driver.get("https://kronos.servicenet.dev.br/rede/perfil_permissoes/listar/")

    # Preenchimento do formulário
    novo = driver.find_element(By.ID, 'btn_novo_perfil_permissoes')
    novo.click()

    nome_aleatorio = limpar_string(faker.company())
    nome_perfil = driver.find_element(By.ID, 'id_nome')
    nome_perfil.send_keys(nome_aleatorio)

    anotacao = driver.find_element(By.ID, 'id_anotacao')
    anotacao.send_keys('Teste de anotacao')

    time.sleep(1)

    salvar = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[5]/div[3]/form/button')
    salvar.click()

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
    SELECT id_perfil_permissao, nome, anotacao, data_cadastro, status, id_arrecadadora
    FROM arrecada.perfil_permissao
    WHERE nome = '{nome_aleatorio}'
    """

    resultados = connect.select(query_perfil, return_type='dict')

    connect.close()


    for resultado in resultados:
        logger.info(f"ID perfil permissao: {resultado['id_perfil_permissao']}, Nome: {resultado['nome']}, "
                    f"ID arrecadadora: {resultado['id_arrecadadora']}, Anotacao: {resultado['anotacao']}, "
                    f"Momento do cadastro: {resultado['data_cadastro']}, Ativo: {resultado['status']}, "
                    f"Cadastro realizado com sucesso!")

    # Iniciando pesquisa para marcar todas as permissões como true
    nome = driver.find_element(By.ID, 'id_nome')
    nome.send_keys(nome_aleatorio)

    pesquisar = driver.find_element(By.ID, 'fat-btn')
    pesquisar.click()

    alterar = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr/td[1]/div/a[2]/i')
    alterar.click()

    marca_todos = driver.find_element(By.ID, 'checkall')
    marca_todos.click()

    salvar = driver.find_element(By.ID, 'btnSubmit')
    salvar.click()

    # Validando se as flags foram todas marcadas
    time.sleep(5)

    checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
    checkboxes_nao_marcados = [checkbox.get_attribute('value') for checkbox in checkboxes if not checkbox.is_selected()]

    logger.info(f"Valores dos checkboxes não marcados: {checkboxes_nao_marcados}")

    if checkboxes_nao_marcados == ['']:
        logger.info("Todas as permissões foram marcadas com sucesso!")
    else:
        logger.warning("Verifique as flags, uma delas não foi marcada.")

    # Inicio da remoção
    voltar = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[5]/div[4]/a')
    voltar.click()

    time.sleep(2)

    nome = driver.find_element(By.ID, 'id_nome')
    nome.send_keys(nome_aleatorio)

    pesquisar = driver.find_element(By.ID, 'fat-btn')
    pesquisar.click()

    time.sleep(1)

    remover = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr/td[1]/div/a[3]')
    remover.click()
    
    time.sleep(1)

    confirma_remocao = driver.find_element(By.ID, 'btnRemoverPerfilPermissao')
    confirma_remocao.click()

    connect = DBConnect(DB_CONFIG)


    time.sleep(3)

    # Verificando exclusão no banco de dados
    query_perfil_excluido = f"""
    SELECT id_perfil_permissao, nome, anotacao, data_cadastro, status, id_arrecadadora
    FROM arrecada.perfil_permissao
    WHERE nome = '{nome_aleatorio}'
    """


    resultados_excluido = connect.select(query_perfil_excluido, return_type='dict')

    connect.close()


    if not resultados_excluido:
        logger.info("Remoção realizada com sucesso!")
    else:
        logger.warning("Algo de errado aconteceu com a exclusão do perfil.")

except Exception as e:
    logger.error(f"Ocorreu um erro durante a execução do script: {e}")

finally:
    driver.quit()
