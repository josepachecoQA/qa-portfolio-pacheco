import psycopg2
import logging
import time
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime
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

nome_arquivo_relatorio = "relatorio.txt"


# Função para transformar CNPJ em inteiro
def cnpj_to_int(cnpj):
    cnpj_numerico = ''.join(filter(str.isdigit, cnpj))
    return int(cnpj_numerico)

# Configurações do banco de dados
DB_CONFIG = {
    'host': os.environ.get('DB_HOST'),
    'port': int(os.environ.get('DB_PORT')),
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD')
}

# Classe para conexão com o banco de dados
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

    def close(self):
        self.conn.close()

# Configurações de login
login = os.environ.get('LOGIN')
senha = os.environ.get('SENHA')

# Verifica se as variáveis de ambiente estão definidas
if not login or not senha:
    raise EnvironmentError('As variáveis de ambiente LOGIN e SENHA devem estar definidas.')

# URL de acesso
url_login = "https://kronos.servicenet.dev.br/"

db_connect = None

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

    driver.get("https://kronos.servicenet.dev.br/rede/configterminal/listar/")
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'btn_nova_config_padrao')))

    # Navegação até o formulário de novo terminal
    novo_terminal = driver.find_element(By.ID, 'btn_nova_config_padrao')
    novo_terminal.click()

    logger.info('Iniciando preenchimento...')

    ativo = driver.find_element(By.ID, 'id_ativo')
    ativo.click()

    bloqueado = driver.find_element(By.ID, 'id_bloqueado')
    bloqueado.click()

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

    salvar = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[5]/div[3]/form/button')
    salvar.click()

    logger.info("Cadastro de configuracao padrao realizado com sucesso")

    # Instância da conexão com o banco de dados
    db_connect = DBConnect(DB_CONFIG)

    time.sleep(10)

    queryConfig2 = f"""
    select id_config_terminal, nome from arrecada.config_terminal where nome = 'Teste Create Conf' """



    resultados = db_connect.select(queryConfig2, return_type='dict')

    db_connect.close()
    logger.info("Conexão com o banco de dados fechada.")    

    if resultados:
        for resultado in resultados:
            logger.info(f"Configuracao encontrada no banco de dados. ID Config: {resultado['id_terminal']}, "
                        f"ID Estabelecimento: {resultado['id_estabelecimento']}, "
                        f"Número Terminal: {resultado['num_terminal']}, "
                        f"Momento do cadastro: {resultado['momento_cadastro']}")
    else:
        logger.warning("A configuracao padrao não foi encontrada no banco de dados.")

    # Início da pesquisa para exclusão

    button_pesquisar = driver.find_element(By.ID, 'fat-btn')
    button_pesquisar.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr/td[1]/div/div[2]/a[1]')))
    remover = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr/td[1]/div/div[2]/a[1]')
    remover.click()

    now = datetime.now()
    data_hora_atual = now.strftime("%d/%m/%Y %H:%M:%S")
    with open(nome_arquivo_relatorio, 'a') as file:
        file.write(f"{data_hora_atual} - Execução do script Criação Recolhedor concluída com sucesso.\n")

except Exception as e:
    logger.error(f"Ocorreu um erro durante a automação: {str(e)}")
    driver.quit()
    
    now = datetime.now()
    data_hora_atual = now.strftime("%d/%m/%Y %H:%M:%S")
    with open(nome_arquivo_relatorio, 'a') as file:
        file.write(f"{data_hora_atual} - Erro durante a execução do script Criação Configuração Padrão: {e}\n")

finally:
    if db_connect:
        db_connect.close()
        logger.info("Conexão com o banco de dados fechada.")
