import psycopg2
from psycopg2.extras import RealDictCursor
import logging
import time
import os
import re
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

# Verificação das variáveis de ambiente
login = os.environ.get('LOGIN')
senha = os.environ.get('SENHA')

if not login or not senha:
    raise EnvironmentError('As variáveis de ambiente LOGIN e SENHA devem estar definidas.')

# Função para gerar número aleatório de 4 dígitos
def gerar_numero_aleatorio_4_digitos():
    return random.randint(1000, 9999)

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

    driver.get('https://kronos.servicenet.dev.br/rede/perfil/gcb/subrede/listar/')

    novo = driver.find_element(By.ID, 'btn_novo_subrede_gcb')
    novo.click()

    # Iniciando preenchimento do form
    nome_aleatorio = faker.company()
    nome_aleatorio = re.sub(r'-', ' ', nome_aleatorio)
    nome_aleatorio = re.sub(r'[^\w\s]', '', nome_aleatorio)
    nome_descricao = nome_aleatorio.split()[0]

    logger.info(f"Nome para preencher na descrição: {nome_descricao}")
    descricao = driver.find_element(By.ID, 'id_descricao')
    descricao.send_keys(nome_descricao)

    numero_de_quatro_digitos = gerar_numero_aleatorio_4_digitos()
    logger.info(f"Números para preencher no campo loja: {numero_de_quatro_digitos}")
    loja = driver.find_element(By.ID, 'id_loja')
    loja.send_keys(numero_de_quatro_digitos)

    perfil_arrecadadora = driver.find_element(By.ID, 'select2-id_id_perfil_arrecadadora_gcb-container')
    perfil_arrecadadora.click()
    options = WebDriverWait(driver, 10).until(
        EC.visibility_of_any_elements_located((By.CLASS_NAME, "select2-results__option"))
    )

    if options:
        first_option = options[1]  # Pega a primeira opção
        first_option.click()

    time.sleep(2)

    salvar = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[5]/div[3]/form/div/button')
    salvar.click()

    # Iniciando conexão com o banco de dados para verificar se foi realizado o cadastro com sucesso
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

    # Exemplo de consulta para verificar resultados no banco
    queryPerfilSubrede = f"""
        SELECT loja, id_perfil_subrede_gcb, nome, id_perfil_arrecadadora_gcb 
        FROM arrecada.perfil_subrede_gcb 
        WHERE nome = '{nome_descricao}'
    """

    resultados = connect.select(queryPerfilSubrede, return_type='dict')

    connect.close()


    if resultados:
        for resultado in resultados:
            logger.info(f"Loja: {resultado['loja']}, ID Perfil GCB: {resultado['id_perfil_subrede_gcb']}, "
                        f"Descrição: {resultado['nome']}, ID Perfil Arrecadadora: {resultado['id_perfil_arrecadadora_gcb']}, Cadastro realizado com sucesso!")
    else:
        logger.warning("Nenhum resultado encontrado.")

    # Exemplo de exclusão de dados
    descricao = driver.find_element(By.ID, 'id_descricao')
    descricao.send_keys(nome_descricao)

    pesquisar = driver.find_element(By.ID, 'fat-btn')
    pesquisar.click()

    remover = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr/td[1]/div/a[2]/i')
    remover.click()

    confirma_remocao = driver.find_element(By.ID, 'btnRemoverPerfilGcbSubrede')
    confirma_remocao.click()

    time.sleep(2)

    connect = DBConnect(DB_CONFIG)


    queryPerfilSubrede2 = f"""
        SELECT loja, id_perfil_subrede_gcb, nome, id_perfil_arrecadadora_gcb 
        FROM arrecada.perfil_subrede_gcb 
        WHERE nome = '{nome_descricao}'
    """

    resultados2 = connect.select(queryPerfilSubrede2, return_type='dict')

    connect.close()

    if not resultados2:
        logger.info("Exclusão realizada com sucesso!")
    else:
        logger.error("Erro na exclusão.")

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
