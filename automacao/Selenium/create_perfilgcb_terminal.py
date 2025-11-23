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
from datetime import datetime


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
    logger.info("Login realizado com sucesso.")

    time.sleep(2)

    # Navegar para a página de perfil GCB
    driver.get("https://kronos.servicenet.dev.br/rede/perfil/gcb/terminal/listar/")
    novo = driver.find_element(By.ID, 'btn_novo_terminal_gcb')
    novo.click()

    # Preencher formulário
    nome_aleatorio = limpar_string(fake.company())
    logger.info(f"Nome para preencher na descrição: {nome_aleatorio}")
    descricao = driver.find_element(By.ID, 'id_descricao')
    descricao.send_keys(nome_aleatorio)

    numero_de_seis_digitos = gerar_numero_aleatorio_6_digitos()
    logger.info(f"Números para preencher no campo PDV: {numero_de_seis_digitos}")
    pdv = driver.find_element(By.ID, 'id_pdv')
    pdv.send_keys(numero_de_seis_digitos)

    numero_de_quatro_digitos = gerar_numero_aleatorio_4_digitos()
    logger.info(f"Números para preencher no campo agência: {numero_de_quatro_digitos}")
    agencia = driver.find_element(By.ID, 'id_agencia_estabelecida')
    agencia.send_keys(numero_de_quatro_digitos)

    numero_de_quatro_digitos_loja = gerar_numero_aleatorio_4_digitos()
    logger.info(f"Números para preencher no campo loja: {numero_de_quatro_digitos_loja}")
    loja = driver.find_element(By.ID, 'id_loja_sub_estabelecimento')
    loja.send_keys(numero_de_quatro_digitos_loja)

    perfil_estabelecimento = driver.find_element(By.ID, 'select2-id_id_perfil_estabelecimento_gcb-container')
    perfil_estabelecimento.click()
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

    queryPerfilTerminal = f"""
    select id_perfil_terminal_gcb, pdv, agencia_estabelecida, loja_sub_estabelecimento, nome, 
    id_perfil_estabelecimento_gcb from arrecada.perfil_terminal_gcb ptg where nome = '{nome_aleatorio}'
    """



    resultados = connect.select(queryPerfilTerminal, return_type='dict')
    
    connect.close()

    if resultados:
        for resultado in resultados:
            logger.info(f"ID Perfil Terminal GCB: {resultado['id_perfil_terminal_gcb']}, PDV: {resultado['pdv']}, "
                        f"Agência: {resultado['agencia_estabelecida']}, Loja: {resultado['loja_sub_estabelecimento']}, "
                        f"Descrição: {resultado['nome']}, ID Perfil Estabelecimento GCB: {resultado['id_perfil_estabelecimento_gcb']}. Cadastro realizado com sucesso!")
    else:
        logger.warning("Nenhum resultado encontrado.")

    # Iniciando pesquisa para exclusão
    descricao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'id_descricao')))
    descricao.send_keys(nome_aleatorio)
    pesquisar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'fat-btn')))
    pesquisar.click()
    remover = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr/td[1]/div/a[2]/i')))
    remover.click()
    confirmar_remocao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modal_confirmacao_exclusao_unico"]/div/div/div[2]/button[2]')))
    confirmar_remocao.click()


    time.sleep(2)

    connect = DBConnect(DB_CONFIG)


    queryPerfilTerminal2 = f"""
    select id_perfil_terminal_gcb, pdv, agencia_estabelecida, loja_sub_estabelecimento, nome, 
    id_perfil_estabelecimento_gcb from arrecada.perfil_terminal_gcb ptg where nome = '{nome_aleatorio}'
    """



    resultados2 = connect.select(queryPerfilTerminal2, return_type='dict')

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

    try:
        connect._connection.close()
    except Exception as e:
        logger.error(f"Erro ao fechar a conexão com o banco de dados: {str(e)}")
