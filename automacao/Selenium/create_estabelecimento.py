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
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


login = os.environ.get('LOGIN')
senha = os.environ.get('SENHA')

# Verifica se as variáveis de ambiente estão definidas
if not login or not senha:
    raise EnvironmentError('As variáveis de ambiente LOGIN e SENHA devem estar definidas.')
# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

service = webdriver.chrome.service.Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

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
    time.sleep(10)

    # Funções para gerar números aleatórios
    def gerar_numero_aleatorio_6_digitos():
        return random.randint(100000, 999999)

    def gerar_numero_aleatorio_9_digitos():
        return random.randint(100000000, 999999999)

    numeros_mci = gerar_numero_aleatorio_9_digitos()
    numeros_coban = gerar_numero_aleatorio_6_digitos()

    # Navegação até a página de novo estabelecimento
    driver.get("https://kronos.servicenet.dev.br/rede/estabelecimento/listar/")

    novo_estab = driver.find_element(By.ID, 'btn_novo_estabelecimento')
    novo_estab.click()
    logger.info("Criando novo estabelecimento...")

    # Preenchimento do formulário
    dropdown_segmento = driver.find_element(By.ID, "select2-id_id_segmento-container")
    dropdown_segmento.click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "select2-results__option")))
    options = driver.find_elements(By.CLASS_NAME, "select2-results__option")
    options[1].click()

    razao_soc = driver.find_element(By.ID, 'id_razao_social')
    razao_soc.send_keys('TESTE CREATE')

    nome_fantas = driver.find_element(By.ID, 'id_nome_fantasia')
    nome_fantas.send_keys('TESTE CREATE LTDA')

    dropdown_sub_rede = driver.find_element(By.ID, "select2-id_id_sub_rede-container")
    dropdown_sub_rede.click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "select2-results__option")))

    options = driver.find_elements(By.CLASS_NAME, "select2-results__option")


    desired_option_text = "API Teste"
    for option in options:
        if option.text == desired_option_text:
            option.click()
            break


    cnpj = driver.find_element(By.ID, 'id_cnpj')
    cnpj.send_keys('54.341.686/0001-03')

    insc_estadual = driver.find_element(By.ID, 'id_insc_estadual')
    insc_estadual.send_keys('Keys.END')

    numero_contrato = driver.find_element(By.ID, 'id_num_contrato')
    numero_contrato.send_keys('1547')

    controle_interno = driver.find_element(By.ID, 'id_codigo_controle')
    controle_interno.send_keys('21')

    observacao = driver.find_element(By.ID, 'id_observacao')
    observacao.send_keys('Teste campo obs')

    #formulario endereço e contato

    aba_endereco = driver.find_element(By.ID, 'tab_endereco_contato_estabelecimento')
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

    nome_contato = driver.find_element(By.ID, 'id_nome_contato_2')
    nome_contato.send_keys('Pacheco Qa')

    email = driver.find_element(By.ID, 'id_email')
    email.send_keys('jose.neto@servicenet.com.br')

    dropdown_consultor = driver.find_element(By.ID, 'select2-id_id_consultor-container')
    dropdown_consultor.click()

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "select2-results__option")))

    options = driver.find_elements(By.CLASS_NAME, "select2-results__option")

    desired_option_text = "Consultor Teste"
    for option in options:
        if option.text == desired_option_text:
            option.click()
            break


    metodo_contato = driver.find_element(By.ID, 'id_metodo_contato')
    metodo_contato.send_keys('Teste contato')

    time.sleep(2)

    # form socios

    socios = driver.find_element(By.ID, 'tab_socios_estabelecimento')
    socios.click()

    nome_socio1 = driver.find_element(By.ID, 'id_socio_nome1')
    nome_socio1.send_keys('José Pacheco da Silva Neto')

    cpf_socio1 = driver.find_element(By.ID, 'id_socio_cpf1')
    cpf_socio1.send_keys('090.082.134-51')

    rg_socio1 = driver.find_element(By.ID, 'id_socio_rg1')
    rg_socio1.send_keys('8020651')

    orgao_expd_sc1 = driver.find_element(By.ID, 'id_socio_org_expedidor1')
    orgao_expd_sc1.send_keys('SDS')

    campo_data1 = driver.find_element(By.ID, 'id_socio_nascimento1')
    campo_data1.send_keys('14011998')

    driver.execute_script("window.scrollTo(0, 0);")

    #Form coban

    clica_coban_aba = driver.find_element(By.ID, 'tab_coban_estabelecimento')
    clica_coban_aba.click()

    time.sleep(2)

    coban = driver.find_element(By.ID, 'id_convenioSE')
    coban.click()
    coban.send_keys(numeros_coban)

    mci = driver.find_element(By.ID, 'id_mci')
    mci.send_keys(numeros_mci)

    agencia = driver.find_element(By.ID, 'id_num_agencia')
    agencia.send_keys('0551')

    #salvando

    # Submissão do formulário
    salvar = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[5]/div[3]/form/button')
    salvar.click()
    logger.info("Finalizando cadastro.")

    time.sleep(10)

    # Consulta no banco de dados para verificar se o estabelecimento foi criado
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

    queryEstab = f"""
        SELECT razao_social, id_estabelecimento 
        FROM arrecada.estabelecimentos 
        WHERE mci = '{numeros_mci}'
    """
    
    resultados = connect.select(queryEstab, return_type='dict')

    connect.close()


    for resultado in resultados:
        logger.info(f"Estabelecimento encontrado no banco de dados. Razão Social: {resultado['razao_social']}, ID Estabelecimento: {resultado['id_estabelecimento']}")

    # Início da pesquisa para exclusão
    pesquisa_razao_soc = driver.find_element(By.ID, 'id_razao_social')
    pesquisa_razao_soc.send_keys('TESTE CREATE')

    button_pesquisar = driver.find_element(By.ID, 'fat-btn')
    button_pesquisar.click()

    button_excluir = driver.find_element(By.CSS_SELECTOR, 'a.btn-danger:nth-child(2)')
    button_excluir.click()

    button_remover = driver.find_element(By.CSS_SELECTOR, '#btnRemoverEstabelecimento')
    button_remover.click()

    connect = DBConnect(DB_CONFIG)
    time.sleep(3)

    queryEstab2 = f"""
        SELECT razao_social, id_estabelecimento 
        FROM arrecada.estabelecimentos 
        WHERE mci = '{numeros_coban}'
    """


    resultados2 = connect.select(queryEstab2, return_type='dict')

    connect.close()


    if not resultados2:
        logger.info("Exclusão realizada com sucesso.")
    else:
        logger.warning("Exclusão não foi realizada com sucesso.")

except Exception as e:
    logger.error(f"Ocorreu um erro durante a execução: {str(e)}")

finally:
    # Fechando a conexão e o navegador
    if 'connect' in locals():
        connect.conn.close()

    if 'driver' in locals():
        driver.quit()

    logger.info("Fim da automação do Kronos.")
