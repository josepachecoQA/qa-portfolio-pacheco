import psycopg2
import logging
import time
import os
import re
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker
from faker.providers import company

# Configurando o logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("selenium_actions")
service = webdriver.chrome.service.Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
fake = Faker()
fake.add_provider(company)

# Função para limpar string
def limpar_string(string):
    string = re.sub(r'-', ' ', string)
    string = re.sub(r'[^\w\s]', '', string)
    return string.split()[0]

# Verificação das variáveis de ambiente
login = os.environ.get('LOGIN')
senha = os.environ.get('SENHA')

def gerar_numero_aleatorio_6_digitos():
    return random.randint(100000, 999999)


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
   

    # Navegar para a página de consultor
    driver.get("https://kronos.servicenet.dev.br/rede/consultor/listar/")
    time.sleep(2)

    # Preencher formulário
    nome_aleatorio = limpar_string(fake.company())
    logger.info(f"Nome para preencher no campo nome: {nome_aleatorio}")
    novo = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'btn_novo_consultor')))
    novo.click()

    nome = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'id_nome')))
    nome.send_keys('TesteQA')

    matricula_all = gerar_numero_aleatorio_6_digitos()
    matricula = driver.find_element(By.ID, 'id_matricula')
    matricula.send_keys(matricula_all)

    time.sleep(2)
    salvar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div[5]/div[3]/form/div[3]/button')))
    salvar.click()

    # Iniciando conexão com o banco de dados
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

    queryConsultor = f"""
    select id_consultor, nome, id_arrecadadora, matricula, momento_cadastro
    from arrecada.consultores c where matricula = '{matricula_all}';
    """

    resultados = connect.select(queryConsultor, return_type='dict')

    connect._connection.close()


    if resultados:
        for resultado in resultados:
            logger.info(f"ID consultor: {resultado['id_consultor']}, Nome: {resultado['nome']}, "
                        f"ID arrecadadora: {resultado['id_arrecadadora']}, "
                        f"Momento do cadastro: {resultado['momento_cadastro']}, Cadastro realizado com sucesso!")
    else:
        logger.warning("Nenhum resultado encontrado.")

    # Iniciando pesquisa para exclusão
    matricula = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'id_matricula')))
    matricula.send_keys(matricula_all)
    pesquisar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'fat-btn')))
    pesquisar.click()
    remover = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr/td[1]/div/a[2]/i')))
    remover.click()
    confirma_remocao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'btnRemoverConsultor')))
    confirma_remocao.click()

    connect = DBConnect(DB_CONFIG)

    time.sleep(2)

    queryConsultor2 = f"""
    select id_consultor, nome, id_arrecadadora, matricula, momento_cadastro
    from arrecada.consultores c where matricula = '{matricula_all}';
    """


    resultados2 = connect.select(queryConsultor2, return_type='dict')
    connect._connection.close()



    if not resultados2:
        logger.info('Exclusão realizada com sucesso!')
    else:
        logger.error('Erro ao realizar exclusão do terminal!')


except Exception as e:
    logger.error(f"Ocorreu um erro durante a execução do script: {e}")
finally:
    driver.quit()
