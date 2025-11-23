import psycopg2
from psycopg2.extras import RealDictCursor
import logging
import time
import os
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker
from faker.providers import company

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("selenium_actions")

# Configuração do WebDriver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Configuração do Faker para geração de dados fictícios
faker = Faker()
faker.add_provider(company)

# Função para transformar CNPJ em inteiro
def cnpj_to_int(cnpj):
    cnpj_numerico = ''.join(filter(str.isdigit, cnpj))
    return int(cnpj_numerico)

# Verificação das variáveis de ambiente
login = os.environ.get('LOGIN')
senha = os.environ.get('SENHA')

# Função gerar convenio
def gerar_numero_aleatorio_6_digitos():
    """
    Gera um número aleatório de 6 dígitos.
    
    :return: Um número inteiro de 6 dígitos.
    """
    return random.randint(100000, 999999)

convenio = gerar_numero_aleatorio_6_digitos()

if not login or not senha:
    raise EnvironmentError('As variáveis de ambiente LOGIN e SENHA devem estar definidas.')

# URL de acesso
url_login = "https://kronos.servicenet.dev.br/"

try:
    # Início da automação
    logger.info("Iniciando automação do Kronos...")

    # Acessar página de login
    driver.get(url_login)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'acceptCookiesButton')))
    aceite_cookie = driver.find_element(By.ID, 'acceptCookiesButton')
    aceite_cookie.click()

    # Preencher formulário de login
    search_bar_login = driver.find_element(By.ID, 'username')
    search_bar_login.send_keys(login)

    search_bar_password = driver.find_element(By.ID, "password")
    search_bar_password.send_keys(senha)

    search_button = driver.find_element(By.ID, 'login-btn')
    search_button.click()

    driver.implicitly_wait(10)
    logger.info("Login realizado com sucesso.")

    logger.info("Aguardando carregamento da página.")
    time.sleep(2)

    # Exemplo de operação no Kronos (substituir com suas ações específicas)
    driver.get("https://kronos.servicenet.dev.br/rede/perfil/gcb/arrecadadora/listar/")
    
    novo_perfil = driver.find_element(By.ID, 'btn_novo_arrecadadora_gcb')
    novo_perfil.click()

    # Operações específicas no formulário (substituir com suas ações específicas)
    

    descricao = driver.find_element(By.ID, 'id_descricao')
    descricao.send_keys('Teste perfil arrecadadora')

    num_convenio = driver.find_element(By.ID, 'id_convenio')
    num_convenio.send_keys(convenio)

    time.sleep(1)

    salvar = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[5]/div[3]/form/div/button')
    salvar.click()
    time.sleep(2)
    # Exemplo de consulta ao banco de dados (substituir com suas consultas)
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

    # Instância da conexão com o banco de dados
    

    # Exemplo de consulta para verificar resultados no banco (substituir com suas consultas)
    queryPerfilArrecadadora = f"""
        select nome, convenio from arrecada.perfil_arrecadadora_gcb pag where convenio = '{convenio}'

    """

    resultados = connect.select(queryPerfilArrecadadora, return_type='dict')

    connect.conn.close()


    if resultados:
        for resultado in resultados:
            logger.info(f"Perfil encontrado no banco de dados. Nome: {resultado['nome']}, Convenio: {resultado['convenio']}")
    else:
        logger.warning("Nenhum resultado encontrado.")


    # Exemplo de exclusão de dados (substituir com suas ações específicas)

    # Iniciando pesquisa para exclusão
    descricao = driver.find_element(By.ID, 'id_descricao')
    descricao.send_keys('Teste perfil arrecadadora')

    num_convenio = driver.find_element(By.ID, 'id_convenio')
    num_convenio.send_keys(convenio)

    pesquisar = driver.find_element(By.ID, 'fat-btn')
    pesquisar.click()

    exclusao = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr/td[1]/div/a[2]/i')
    exclusao.click()

    confirma_exclusao = driver.find_element(By.ID, 'btnRemoverPerfilGcbArrecadadora')
    confirma_exclusao.click()

    connect = DBConnect(DB_CONFIG)


    time.sleep(2)

    queryPerfilArrecadadora2 = f"""
    SELECT id_perfil_arrecadadora_gcb, nome, convenio
    FROM arrecada.perfil_arrecadadora_gcb 
    WHERE convenio = '{convenio}' AND nome = 'Teste perfil arrecadadora'
    """


    resultados = connect.select(queryPerfilArrecadadora2, return_type='dict')

    connect.conn.close()


    if not resultados:
        print('Exclusão realizada com sucesso !')
    else:
        print('Erro ao realizar exclusão.')
    

except Exception as e:
    logger.error(f"Ocorreu um erro durante a execução do script: {str(e)}")

finally:
    # Fechamento do WebDriver e conexão com o banco de dados
    try:
        driver.quit()
    except:
        pass

    try:
        connect.conn.close()
    except:
        pass
