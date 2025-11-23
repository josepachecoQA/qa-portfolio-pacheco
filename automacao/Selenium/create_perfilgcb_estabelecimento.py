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



# Configurando o logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("selenium_actions")
service = webdriver.chrome.service.Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
fake = Faker()

# Função para gerar número aleatório de 4 dígitos
def gerar_numero_aleatorio_4_digitos():
    return random.randint(1000, 9999)

# Função para gerar número aleatório de 6 dígitos
def gerar_numero_aleatorio_6_digitos():
    return random.randint(100000, 999999)

# Função para limpar string
def limpar_string(string):
    string = re.sub(r'-', ' ', string)
    string = re.sub(r'[^\w\s]', '', string)
    return string.split()[0]

# Verificação das variáveis de ambiente
login = os.environ.get('LOGIN')
senha = os.environ.get('SENHA')

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

    driver.implicitly_wait(10)
    logger.info("Login realizado com sucesso.")
    time.sleep(2)
    # Navegar para a página de perfil GCB
    driver.get("https://kronos.servicenet.dev.br/rede/perfil/gcb/estabelecimento/listar/")

    novo = driver.find_element(By.ID, 'btn_novo_estabelecimento_gcb')
    novo.click()

    # Preencher formulário
    nome_aleatorio = limpar_string(fake.company())
    logger.info(f"Nome para preencher na descrição: {nome_aleatorio}")
    descricao = driver.find_element(By.ID, 'id_descricao')
    descricao.send_keys(nome_aleatorio)

    numero_de_seis_digitos = gerar_numero_aleatorio_6_digitos()
    logger.info(f"Números para preencher no campo coban: {numero_de_seis_digitos}")
    coban = driver.find_element(By.ID, 'id_coban')
    coban.send_keys(numero_de_seis_digitos)

    numero_de_quatro_digitos = gerar_numero_aleatorio_4_digitos()
    logger.info(f"Números para preencher no campo agência: {numero_de_quatro_digitos}")
    agencia = driver.find_element(By.ID, 'id_agencia')
    agencia.send_keys(numero_de_quatro_digitos)

    perfil_subrede = driver.find_element(By.ID, 'select2-id_id_perfil_subrede_gcb-container')
    perfil_subrede.click()
    options = WebDriverWait(driver, 10).until(
        EC.visibility_of_any_elements_located((By.CLASS_NAME, "select2-results__option"))
    )

    if options:
        first_option = options[2]  # Pega a segunda opção
        first_option.click()

    time.sleep(2)

    salvar = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[5]/div[3]/form/button')
    salvar.click()
    time.sleep(2)

    # Iniciando conexão com o banco de dados
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

    queryPerfilEstabelecimento = f"""
    select id_perfil_estabelecimento_gcb, coban, agencia, nome, id_perfil_subrede_gcb, substabelecido
    from arrecada.perfil_estabelecimento_gcb peg where nome = '{nome_aleatorio}'
    """


    resultados = connect.select(queryPerfilEstabelecimento, return_type='dict')

    connect.close()


    if resultados:
        for resultado in resultados:
            logger.info(f"ID Perfil Estabelecimento GCB: {resultado['id_perfil_estabelecimento_gcb']}, Numero do Coban: {resultado['coban']}, "
                        f"Numero da agencia: {resultado['agencia']}, Nome: {resultado['nome']}, ID Perfil Subrede GCB: {resultado['id_perfil_subrede_gcb']}, "
                        f"Substabelecido: {resultado['substabelecido']}. Cadastro realizado com sucesso!")
    else:
        logger.warning("Nenhum resultado encontrado.")

    # Excluir dados cadastrados
    descricao = driver.find_element(By.ID, 'id_descricao')
    descricao.send_keys(nome_aleatorio)
    pesquisar = driver.find_element(By.ID, 'fat-btn')
    pesquisar.click()
    remover = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr/td[1]/div/a[2]/i')
    remover.click()
    confirmar_remocao = driver.find_element(By.ID, 'btnRemoverPerfilGcbEstabelecimento')
    confirmar_remocao.click()
    time.sleep(2)


    connect = DBConnect(DB_CONFIG)

    queryPerfilEstabelecimento2 = f"""
    select id_perfil_estabelecimento_gcb, coban, agencia, nome, id_perfil_subrede_gcb, substabelecido
    from arrecada.perfil_estabelecimento_gcb peg where nome = '{nome_aleatorio}'
    """


    resultados2 = connect.select(queryPerfilEstabelecimento2, return_type='dict')

    connect.close()


    if not resultados2:
        logger.info("Exclusão realizada com sucesso!")
    else:
        logger.error("Erro na exclusão.")

except Exception as e:
    logger.error(f"Ocorreu um erro durante a execução do script: {str(e)}")

finally:
    try:
        driver.quit()
    except Exception as e:
        logger.error(f"Erro ao fechar o WebDriver: {str(e)}")

    # Verificar se connect foi definido antes de fechar a conexão
    if 'connect' in locals():
        try:
            connect.conn.close()
        except Exception as e:
            logger.error(f"Erro ao fechar a conexão com o banco de dados: {str(e)}")
