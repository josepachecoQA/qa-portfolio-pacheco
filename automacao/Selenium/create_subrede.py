import psycopg2
import logging
import time
import re
import os
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from datetime import datetime
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


service = Service('/usr/local/bin/chromedriver')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
login = os.environ.get('LOGIN')
senha = os.environ.get('SENHA')

# Verifica se as variáveis de ambiente estão definidas
if not login or not senha:
    raise EnvironmentError('As variáveis de ambiente LOGIN e SENHA devem estar definidas.')

driver.get("https://kronos.servicenet.dev.br/")
fake = Faker()

nome_arquivo_relatorio = "relatorio.txt"

# Gera um nome completo aleatório
nome_completo = fake.name()

# Extrai o primeiro nome
primeiro_nome = nome_completo.split()[0]
primeiro_nome = re.sub(r'-', ' ', primeiro_nome)
primeiro_nome_limpo = re.sub(r'[^\w\s]', '', primeiro_nome)

time.sleep(3)
aceite_cookie = driver.find_element(By.ID, 'acceptCookiesButton')
aceite_cookie.click()
search_bar_login = driver.find_element(By.XPATH, '//*[@id="username"]')
search_bar_login.send_keys(login)
search_bar_password = driver.find_element(By.ID, "password")
search_bar_password.send_keys(senha)
search_button = driver.find_element(By.ID, 'login-btn')
search_button.click()
driver.implicitly_wait(10)

print("Aguardando carregamento da pagina")
time.sleep(10)

driver.get("https://kronos.servicenet.dev.br/rede/subrede/listar/")

nova_sub = driver.find_element(By.ID, 'btn_nova_subrede')
nova_sub.click()

nome_sub = driver.find_element(By.ID, 'id_nome')
nome_sub.send_keys(primeiro_nome_limpo)

nome_pos = driver.find_element(By.ID, 'id_nome_pos')
nome_pos.send_keys(primeiro_nome_limpo)
print('Inserindo dados de cadastro: ', primeiro_nome_limpo)

salvar = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[5]/div[3]/form/div/div[3]/div/button')
salvar.click()

class Conexao(object):

    def __init__(self, host, port, db_name, db_user, db_pass):
        try:
            self._db = psycopg2.connect(host=host, port=port, database=db_name, user=db_user, password=db_pass)
            self.cursor = self._db.cursor()
            self._db.autocommit = True
            print("Conectado: {host}:{port}/{db}. User: {usuario}.".format(host=host, db=db_name, port=port, usuario=db_user))
            logging.info("Conectado: {host}:{port}/{db}. User: {usuario}.".format(host=host, db=db_name, port=port, usuario=db_user))
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
            db_name=DB_CONFIG['dbname'],
            db_user=DB_CONFIG['user'],
            db_pass=DB_CONFIG['password']
        )
        self._cursor = self._connection.cursor

    def select(self, sql, type=None):
        _data = None
        try:
            self._cursor.execute(sql)
            data = self._cursor
        except ValueError as e:
            return e

        if type == dict:
            _data = self._dictfetchall(self._cursor)
        else:
            _data = self._cursor.fetchall()

        return _data

    def _dictfetchall(self, cursor):
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

# Verifica se todas as variáveis de ambiente estão definidas
required_env_vars = ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
for var in required_env_vars:
    if not os.environ.get(var):
        # raise EnvironmentError(f'A variável de ambiente {var} não está definida.')
        print(f'A variável de ambiente {var} não está definida.')
        exit()

# Cria o dicionário de configuração do banco de dados
DB_CONFIG = {
    'host': os.environ.get('DB_HOST'),
    'port': int(os.environ.get('DB_PORT')),
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD')
}
print(DB_CONFIG)

connect = DBConnect(DB_CONFIG)

# Usando a variável nome_sub para a consulta
querySub = f"""
             SELECT 
             nome 
             FROM arrecada.sub_redes where id_arrecadadora = 9 and nome = '{primeiro_nome_limpo}'
            """


sub = connect.select(querySub, dict)

print(str(sub[0]['nome']))

validacao = str(sub[0]['nome'])

with open(nome_arquivo_relatorio, "a") as arquivo:
    # Escreve a data e hora atual no arquivo
    data_hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    arquivo.write(f"Data e hora da operação: {data_hora_atual}\n")
    if validacao != 'NULL':  
        if validacao == primeiro_nome_limpo:
            print('Cadastro realizado com sucesso!')
            arquivo.write('Cadastro realizado com sucesso!\n')
        else:
            print('Erro no cadastro Sub rede')
            arquivo.write('Erro no cadastro Sub rede\n')
    else:
        print('Erro no cadastro Sub rede')           

time.sleep(2)  

buscar = driver.find_element(By.ID, 'id_nome')
buscar.send_keys(primeiro_nome_limpo)
pesquisar = driver.find_element(By.ID, 'fat-btn')
pesquisar.click()
wait = WebDriverWait(driver, 10)
elemento_para_apagar = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[5]/div[5]/div[1]/div[2]/div/table/tbody/tr/td[1]/div/a[2]')
elemento_para_apagar.click()
botao_remove = driver.find_element(By.ID, 'btnRemoverSubrede')
botao_remove.click()
# removendo = driver.find_element(By.CSS_SELECTOR, '#btnRemoverSubrede')
# removendo.click()

time.sleep(5)  

connect = DBConnect(DB_CONFIG)


# Usando a variável nome_sub para a consulta de exclusão
queryDeleteSub = f"""
                 SELECT 
                 nome 
                 FROM arrecada.sub_redes where id_arrecadadora = 9 and nome = '{primeiro_nome_limpo}'
                """ 



subdelete = connect.select(queryDeleteSub, dict)
connect.close()

with open(nome_arquivo_relatorio, "a") as arquivo:
    if subdelete == []:
        print('Sub rede excluida com sucesso')
        arquivo.write('Sub rede excluida com sucesso\n')
    elif subdelete != []:
        print('Sub rede nao foi excluida')
        arquivo.write('Sub rede nao foi excluida\n')
    else:
        print('Ocorreu um erro durante a validacao')
        arquivo.write('Ocorreu um erro durante a validacao\n')