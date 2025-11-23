import psycopg2
from psycopg2.extras import RealDictCursor
import logging
import time
import random
import re
import os
from faker import Faker
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

login = os.environ.get('LOGIN')
senha = os.environ.get('SENHA')

# Verifica se as variáveis de ambiente estão definidas
if not login or not senha:
    raise EnvironmentError('As variáveis de ambiente LOGIN e SENHA devem estar definidas.')

# Configuração do webdriver
service = webdriver.chrome.service.Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Funções auxiliares
def generate_valid_cnpj():
    faker = Faker('pt_BR')
    return faker.cnpj()

def generate_valid_cpf():
    faker = Faker('pt_BR')
    return faker.cpf()

def generate_company_name():
    fake = Faker()
    company_name = fake.company()
    return re.sub(r'[^\w\s]', '', company_name)

def generate_random_digits(num_digits):
    return random.randint(10**(num_digits-1), 10**num_digits-1)

# Início do processo de automação
try:
    logger.info("Iniciando automação do Kronos...")

    driver.get("https://kronos.servicenet.dev.br/")
    time.sleep(3)

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

    logger.info("Aguardando carregamento da página.")
    time.sleep(2)

    # Navegação até a página de novo estabelecimento
    driver.get("https://kronos.servicenet.dev.br/rede/loja/listar/")
    nova_loja = driver.find_element(By.ID, 'btn_nova_loja')
    nova_loja.click()
    logger.info("Criando nova loja...")

    cnpj = generate_valid_cnpj()
    nome_empresa = generate_company_name()
    cpf_ficticio = generate_valid_cpf()
    numero_loja = generate_random_digits(6)
    print('CNPJ GERADO: ', cnpj)
    # Preenchimento do formulário
    dropdown_segmento = driver.find_element(By.ID, 'select2-id_id_segmento-container')
    dropdown_segmento.click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "select2-results__option")))
    options = driver.find_elements(By.CLASS_NAME, "select2-results__option")
    options[1].click()

    time.sleep(2)

    dropdown_estabelecimento = driver.find_element(By.ID, 'select2-id_id_estabelecimento-container')
    dropdown_estabelecimento.click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "select2-results__option")))
    options = driver.find_elements(By.CLASS_NAME, "select2-results__option")
    options[1].click()

    razao_social = driver.find_element(By.ID, 'id_descricao')
    razao_social.send_keys(nome_empresa)

    nome_fantasia = driver.find_element(By.ID, 'id_nome_fantasia')
    nome_fantasia.send_keys(nome_empresa)

    cpf_cnpj = driver.find_element(By.ID, 'id_cnpj')
    cpf_cnpj.send_keys(cnpj)

    numero_loja_field = driver.find_element(By.ID, 'id_numero_loja')
    numero_loja_field.send_keys(numero_loja)

    # Preenchimento do formulário de endereço
    aba_endereco = driver.find_element(By.ID, 'tab_endereco_loja')
    aba_endereco.click()

    cep = driver.find_element(By.ID, 'id_cep')
    cep.send_keys('58408063')

    numero = driver.find_element(By.ID, 'id_numero')
    numero.send_keys('100')

    complemento = driver.find_element(By.ID, 'id_complemento')
    complemento.send_keys('Empresa')

    ddd1 = driver.find_element(By.ID, 'id_ddd')
    ddd1.send_keys('081')

    telefone_1 = driver.find_element(By.ID, 'id_telefone')
    telefone_1.send_keys('991737145')

    nome_contato = driver.find_element(By.ID, 'id_nome_contato')
    nome_contato.send_keys('Pacheco Qa')
    time.sleep(1)

    # Preenchimento do formulário Coban
    clica_coban_aba = driver.find_element(By.ID, 'tab_coban_loja')
    clica_coban_aba.click()

    time.sleep(1)

    agencia = driver.find_element(By.ID, 'id_cc_agencia')
    agencia.send_keys('5551')

    # Submissão do formulário
    salvar = driver.find_element(By.XPATH, '//*[@id="form_cadastro_loja"]/button')
    salvar.click()
    logger.info("Cadastro de nova loja enviado.")

    # Aumenta o tempo de espera após enviar o formulário
    time.sleep(5)

    # Consulta no banco de dados para verificar se a loja foi criada
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

    queryLoja = f"""
    SELECT nome_fantasia, numero_loja, momento_cadastro 
    FROM arrecada.loja_coban 
    WHERE cnpj = '{cnpj.replace(".", "").replace("/", "").replace("-", "")}'
    """


    resultados = connect.select(queryLoja, return_type='dict')

    connect.close()


    if resultados:
        for resultado in resultados:
            logger.info(f"Loja encontrada no banco de dados. Nome Fantasia: {resultado['nome_fantasia']}, Numero da loja: {resultado['numero_loja']}, Data de cadastro: {resultado['momento_cadastro']}")
    else:
        logger.warning("A loja não foi encontrada no banco de dados.")

except Exception as e:
    logger.error(f"Ocorreu um erro durante a execução: {str(e)}")

finally:
    # Fechando a conexão e o navegador
    if 'connect' in locals():
        connect.conn.close()

    if 'driver' in locals():
        driver.quit()

    logger.info("Fim da automação do Kronos.")
