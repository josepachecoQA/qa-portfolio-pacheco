import psycopg2
import logging
import time
import re
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from faker import Faker
from faker.providers import company


# Configurando o logging
logging.basicConfig(level=logging.INFO)  # Define o nível de registro
logger = logging.getLogger("selenium_actions")
service = webdriver.chrome.service.Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
faker = Faker()
faker.add_provider(company)

#driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get("https://kronos.redeflex.dev.br/")
time.sleep(3) 
search_bar_login = driver.find_element(By.XPATH,'//*[@id="username"]')
search_bar_login.send_keys("jose.pacheco")
search_bar_password = driver.find_element(By.ID, "password")
search_bar_password.send_keys("Pacheco159.")
search_button = driver.find_element(By.ID, 'login-btn')
search_button.click()

time.sleep(2) 


driver.get("https://kronos.redeflex.dev.br/rede/prospeccao/cadastrar/")

fake = Faker()
nome_empresa = fake.company()
# Substitui hífens por espaços
nome_empresa = re.sub(r'-', ' ', nome_empresa)

# Limpeza para remover outros caracteres especiais indesejados
nome_empresa_limpo = re.sub(r'[^\w\s]', '', nome_empresa)

print("Nome da empresa aleatória gerado:", nome_empresa)

fake = Faker()
nome = fake.name()
print("Nome aleatório gerado:", nome)


fake = Faker('pt_BR')
cpf_ficticio = fake.cpf()

print("CPF fictício gerado:", cpf_ficticio)


razao_social = driver.find_element(By.ID, 'id_nome')
razao_social.send_keys(nome_empresa)

nome_fantasia = driver.find_element(By.ID, 'id_nome_fantasia')
nome_fantasia.send_keys(nome_empresa)

cpf_cnpj = driver.find_element(By.ID, 'id_cpf_cnpj')
cpf_cnpj.send_keys(cpf_ficticio)

dropdown_segmento = driver.find_element(By.XPATH, '//span[@id="select2-id_id_segmento-container" and contains(@title, "Selecione")]')
dropdown_segmento.click()
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "select2-results__option")))

options = driver.find_elements(By.CLASS_NAME, "select2-results__option")
for option in options:
    if option.text != "Selecione":
        option.click()
        break

time.sleep(1)



dropdown_prospector = driver.find_element(By.XPATH, '//span[@id="select2-id_id_prospector-container" and contains(@title, "Selecione")]')
dropdown_prospector.click()
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "select2-results__option")))

options = driver.find_elements(By.CLASS_NAME, "select2-results__option")
for option in options:
    if option.text != "Selecione":
        option.click()
        break

time.sleep(1)


email = driver.find_element(By.ID, 'id_email')
email.send_keys('tested5@gmail.com')

## Aba endereço

endereco = driver.find_element(By.XPATH, '//*[@id="tab_identificacao"]/ul/li[2]/a')
endereco.click()

time.sleep(2)

cep = driver.find_element(By.ID, 'id_cep')
cep.click()
cep.send_keys('58408063')

numero = driver.find_element(By.ID, 'id_numero')
numero.send_keys('14')

time.sleep(1)

# Form aba representante

representante = driver.find_element(By.XPATH, '//*[@id="aba_representante"]/a')
representante.click()

time.sleep(1)

nome_representante1 = driver.find_element(By.ID, 'id_nome_socio')
nome_representante1.send_keys(nome)

cpf_cnpj = driver.find_element(By.ID, 'id_cpf_socio')
cpf_cnpj.send_keys(cpf_ficticio)

num_doc = driver.find_element(By.ID, 'id_rg_socio')
num_doc.send_keys('8020651')

time.sleep(2)

dropdown_uf = driver.find_element(By.ID, 'select2-id_id_estado_orgao_emissor-container')
dropdown_uf.click()
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "select2-results__option")))
options = driver.find_elements(By.CLASS_NAME, "select2-results__option")

for option in options:
    if option.text != "Selecione":
        option.click()
        break

time.sleep(1)


data_nascimento = driver.find_element(By.ID, 'id_data_nasc_representante')
data_nascimento.send_keys('14011998')


dropdown_status_civil = driver.find_element(By.XPATH, '//*[@id="content_tab_representante2"]/div[4]/div[3]/span/span[1]/span')
dropdown_status_civil.click()
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "select2-results__option")))
options = driver.find_elements(By.CLASS_NAME, "select2-results__option")

for option in options:
    if option.text != "Selecione":
        option.click()
        break

time.sleep(1)

nascionalidade = driver.find_element(By.ID, 'id_nacionalidade_socio')
nascionalidade.send_keys('Brasileiro')

profissao = driver.find_element(By.ID, 'id_profissao_socio')
profissao.send_keys('Tested5')

endereco_socio1 = driver.find_element(By.ID, 'id_cep_socio')
endereco_socio1.click()
endereco_socio1.send_keys('58053022')

numero_socio1 = driver.find_element(By.ID, 'id_numero_socio')
numero_socio1.send_keys('666')

ddd_socio1 = driver.find_element(By.ID, 'id_ddd_representante')
ddd_socio1.send_keys('081')

contato_socio1 = driver.find_element(By.ID, 'id_telefone_representante')
contato_socio1.send_keys('991737145')

time.sleep(2)

# Form dados bancários conta jurídica

dados_bancarios = driver.find_element(By.XPATH, '//*[@id="aba_dados_bancario"]/a')
dados_bancarios.click()

time.sleep(1)

dropdown_banco_cj = driver.find_element(By.ID, 'select2-id_id_banco-container')
dropdown_banco_cj.click()
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "select2-results__option")))
options = driver.find_elements(By.CLASS_NAME, "select2-results__option")

for option in options:
    if option.text != "---------":
        option.click()
        break

time.sleep(2)


agencia_cj = driver.find_element(By.ID, 'id_num_agencia_banco')
agencia_cj.send_keys('1122')

conta_cj = driver.find_element(By.ID, 'id_conta_corrente_banco')
conta_cj.send_keys('102300')

cpf_cnpj_cj = driver.find_element(By.ID, 'id_cpf_cnpj_conta_juridica')
cpf_cnpj_cj.send_keys(cpf_ficticio)

gerente_cj = driver.find_element(By.ID, 'id_nome_gerente')
gerente_cj.send_keys(nome)

ddd_gerente_cj = driver.find_element(By.ID, 'id_ddd_contato_gerente')
ddd_gerente_cj.send_keys('083')

telefone_gerente_cj = driver.find_element(By.ID, 'id_contato_gerente')
telefone_gerente_cj.send_keys('991737145')

# Form dados bancários conta Comissão

conta_comissao = driver.find_element(By.XPATH, '//*[@id="aba_dados_bancarios_beneficiario"]/a')
conta_comissao.click()

time.sleep(2)

dropdown_banco_cc = driver.find_element(By.ID, 'select2-id_id_banco_beneficiario-container')
dropdown_banco_cc.click()
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "select2-results__option")))
options = driver.find_elements(By.CLASS_NAME, "select2-results__option")

for option in options:
    if option.text != "---------":
        option.click()
        break

time.sleep(2)

agencia_cc = driver.find_element(By.ID, 'id_num_agencia_banco_beneficiario')
agencia_cc.send_keys('3366')

conta_cc = driver.find_element(By.ID, 'id_conta_corrente_banco_beneficiario')
conta_cc.send_keys('963369')

cpf_cnpj_cc = driver.find_element(By.ID, 'id_cpf_beneficiario')
cpf_cnpj_cc.send_keys(cpf_ficticio)


# Finalizando registro da prospecção

registrar_prospec = driver.find_element(By.XPATH, '//*[@id="form_prospeccao_cadastro"]/a[2]')
registrar_prospec.click()


time.sleep(2)#Iniciando conexão com bd para verificar se foi realizado o cadastro com sucesso 

class Conexao(object):

    def __init__(self, host, port, db_name, db_user, db_pass):
        try:
            self._db = psycopg2.connect(host=host, port=port, database=db_name, user=db_user, password=db_pass)
            self.cursor = self._db.cursor()
            self._db.autocommit = True
            print("Conectado: {host}:{port}/{db}. User: {usuario}.".format(host=host, db=db_name, port=port,
                                                                              usuario=db_user))
            logging.info(
                "Conectado: {host}:{port}/{db}. User: {usuario}.".format(host=host, db=db_name, port=port,
                                                                          usuario=db_user))
        except ValueError as e:
            print(e)

    def close(self):
        self.cursor.close()
        print("Conexao fechada!")

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

    def select(self, sql, type=None):
        _data = None
        try:
            self._cursor.execute(sql)
        except ValueError as e:
            return e

        if type == 'dict':
            _data = self._dictfetchall(self._cursor)
        else:
            _data = self._cursor.fetchall()

        return _data

    def _dictfetchall(self, cursor):
        desc = cursor.description
        return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
    

DB_CONFIG = {
    'host': "db1.ec2.servicenet.dev.br",
    'port': 7432,
    'db_name': "snetdb",
    'user': "jose_neto",
    'pass': "78cd01dc-5693-477e-8be7-ae3817fcfbe8"
}

connect = DBConnect(DB_CONFIG)

time.sleep(2)

queryProspeccao = f"""
select id_prospeccao, nome from gestao.prospeccao where cnpj = '{cpf_ficticio}'
"""

resultados = connect.select(queryProspeccao, type='dict')

connect.close()

for resultado in resultados:
    # print(resultado)
    print(f"ID Prospeccao: {resultado['id_prospeccao']}, Nome: {resultado['nome']}, Prospecção cadastrada com sucesso!")


driver.quit()

