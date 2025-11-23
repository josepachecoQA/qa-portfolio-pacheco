import psycopg2
import logging
import time
from psycopg2.extras import RealDictCursor
import os
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

login = os.environ.get('LOGIN')
senha = os.environ.get('SENHA')

# Verifica se as variáveis de ambiente estão definidas
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

    driver.get("https://kronos.servicenet.dev.br/rede/terminal/listar/")
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'btn_novo_terminal')))

    # Navegação até o formulário de novo terminal
    novo_terminal = driver.find_element(By.ID, 'btn_novo_terminal')
    novo_terminal.click()

    logger.info('Navegando até o módulo terminal')

    # Preenchimento do formulário principal
    input_element = driver.find_element(By.ID, "id_num_terminal")
    valor_preenchido = input_element.get_attribute("value")

    cep = driver.find_element(By.ID, "id_cep")
    cep.click()
    cep.send_keys('58408063')

    time.sleep(2)


    dropdown_estabelecimento = driver.find_element(By.ID, 'select2-id_id_estabelecimento-container')
    dropdown_estabelecimento.click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "select2-results__option")))
    options = driver.find_elements(By.CLASS_NAME, "select2-results__option")
    options[1].click()

    time.sleep(2)

    dropdown_loja = driver.find_element(By.ID, 'select2-id_id_loja-container')
    dropdown_loja.click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "select2-results__option")))
    options = driver.find_elements(By.CLASS_NAME, "select2-results__option")
    options[1].click()
    
    time.sleep(2)
    
    apresentacao = driver.find_element(By.ID, 'id_apresentacao')
    apresentacao.send_keys('Teste Bot')

    # Preenchimento do formulário de configuração
    configuracao = driver.find_element(By.ID, 'tab_configuracao_terminal')
    configuracao.click()

    ativo = driver.find_element(By.ID, 'id_ativo')
    ativo.click()

    comprovante_2_vias = driver.find_element(By.ID, 'id_re_imprimir_comprovante')
    comprovante_2_vias.click()

    solicitar_confirmacao_valor = driver.find_element(By.ID, 'id_confirmar_valor_conta')
    solicitar_confirmacao_valor.click()

    receber_contas_lote = driver.find_element(By.ID, 'id_processar_lote_contas')
    receber_contas_lote.click()

    faz_recarga = driver.find_element(By.ID, 'id_faz_recarga')
    faz_recarga.click()

    opera_online = driver.find_element(By.ID, 'id_operar_online')
    opera_online.click()

    validar_serial_pos = driver.find_element(By.ID, 'id_validar_serial_pos')
    validar_serial_pos.click()

    confirmar_impressao_recarga = driver.find_element(By.ID, 'id_confirmar_dados_recarga')
    confirmar_impressao_recarga.click()

    bloquear_impressao_comprovante = driver.find_element(By.ID, 'id_bloq_reimpressao_coban')
    bloquear_impressao_comprovante.click()

    forcar_inicializacao = driver.find_element(By.ID, 'id_inicializar')
    forcar_inicializacao.click()

    nao_exibir_boleto_avulso = driver.find_element(By.ID, 'id_nao_exibir_emissao_avulsa')
    nao_exibir_boleto_avulso.click()

    nao_exibir_lote_envelope = driver.find_element(By.ID, 'id_aliviar_ilimitado')
    nao_exibir_lote_envelope.click()

    forcar_fechamento = driver.find_element(By.ID, 'id_fechamento_terminal')
    forcar_fechamento.click()

    solicitar_troco_pos_pagamento = driver.find_element(By.ID, 'id_solicita_troco')
    solicitar_troco_pos_pagamento.click()

    senha_supersao = driver.find_element(By.ID, 'id_senha_supervisao')
    senha_supersao.send_keys('12345')

    confirma_senha_supervisao = driver.find_element(By.ID, 'id_confirma_senha')
    confirma_senha_supervisao.send_keys('12345')

    # Preenchimento do formulário Coban
    coban = driver.find_element(By.ID, 'tab_coban_terminal')
    coban.click()

    num_pdv = driver.find_element(By.ID, 'id_cc_pdv')
    num_pdv.send_keys('965')

    salvar = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[5]/div[4]/form/button')
    salvar.click()

    logger.info("Cadastro de novo terminal realizado com sucesso")

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
    db_connect = DBConnect(DB_CONFIG)

    # Aguarda 10 segundos para garantir que o cadastro seja processado
    time.sleep(10)

    # Consulta ao banco de dados para verificar se o terminal foi cadastrado
    query_terminal = f"""
        SELECT id_terminal, id_estabelecimento, num_terminal, momento_cadastro
        FROM arrecada.terminais WHERE num_terminal = '{valor_preenchido}'
    """

    resultados = db_connect.select(query_terminal, return_type='dict')

    connect.close()

    if resultados:
        for resultado in resultados:
            logger.info(f"Terminal encontrado no banco de dados. ID Terminal: {resultado['id_terminal']}, "
                        f"ID Estabelecimento: {resultado['id_estabelecimento']}, "
                        f"Número Terminal: {resultado['num_terminal']}, "
                        f"Momento do cadastro: {resultado['momento_cadastro']}")
    else:
        logger.warning("O terminal não foi encontrado no banco de dados.")

    # Início da pesquisa para exclusão
    num_terminal = driver.find_element(By.ID, 'id_num_terminal')
    num_terminal.send_keys(valor_preenchido)

    button_pesquisar = driver.find_element(By.ID, 'fat-btn')
    button_pesquisar.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr/td[1]/div/div[2]/a[1]')))
    remover = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr/td[1]/div/div[2]/a[1]')
    remover.click()

    confirmar_remocao = driver.find_element(By.ID, 'btnRemoverTerminal')
    confirmar_remocao.click()

    connect = DBConnect(DB_CONFIG)

    time.sleep(2)

    # Consulta ao banco de dados após exclusão para verificar se o terminal foi removido
    query_terminal_after_delete = f"""
        SELECT id_terminal, id_estabelecimento, num_terminal, momento_cadastro
        FROM arrecada.terminais WHERE num_terminal = '{valor_preenchido}'
    """

    resultados_after_delete = db_connect.select(query_terminal_after_delete, return_type='dict')

    connect.close()

    if not resultados_after_delete:
        logger.info("Exclusão do terminal realizada com sucesso!")
    else:
        logger.warning("Erro ao realizar exclusão do terminal.")

except Exception as e:
    logger.error(f"Ocorreu um erro durante a execução do script: {str(e)}")

finally:
    # Fechamento da conexão com o banco de dados e do WebDriver
    try:
        connect.conn.close()
    except:
        pass

    try:
        driver.quit()
    except:
        pass
