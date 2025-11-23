import psycopg2
import pandas as pd
import os
import datetime
from db import pega_conexao_bd

'''
#
#====== CONFIGS
#
'''

##### HOMOLOGACAO LOGCRED
# db_params_homologacao_logcred = {
#     'dbname': 'snetdb',
#     'user': 'jose_neto',
#     'password': '99392b7e-461d-4564-8fdd-10d8cffe4a65',
#     'host': 'db1.ec2.servicenet.dev.br',
#     'port': '7432'
# }


'''
#
#===== LOGGER
#
'''

class Logger:
    """
    Esta classe fornece funcionalidades para criar e registrar mensagens de log em um arquivo.

    Attributes:
        log_directory (str): O diretório onde os arquivos de log serão armazenados.
        log_file (str): O nome do arquivo de log atual.

    Methods:
        create_log_directory(): Cria o diretório de logs se ele não existir.
        generate_log_filename(): Gera o nome do arquivo de log com base na data atual.
        create_log_file(): Cria o arquivo de log se ele não existir.
        log(message): Registra uma mensagem no arquivo de log com um timestamp.
    """
    def __init__(self, param, log_directory = 'logger/log'):
        """
        Inicializa uma instância da classe `Logger`.

        Args:
            log_directory (str): O diretório onde os arquivos de log serão armazenados.

        Atributos:
            log_directory (str): O diretório onde os arquivos de log serão armazenados.
            log_file (str): O nome do arquivo de log atual.
        """
        self.log_directory = log_directory
        self.param = param
        self.create_log_directory()
        self.log_file = self.generate_log_filename()
        self.create_log_file()

    def create_log_directory(self):
        """
        Cria o diretório de logs se ele não existir.

        Returns:
            None
        """
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

    def generate_log_filename(self):
        """
        Gera o nome do arquivo de log com base na data atual.

        Returns:
            str: O nome completo do arquivo de log.
        """
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        log_filename = f"{current_date}_{self.param}_log.txt"
        return os.path.join(self.log_directory, log_filename)

    def create_log_file(self):
        """
        Cria o arquivo de log se ele não existir.

        Returns:
            None
        """
        try:
            with open(self.log_file, 'a'):
                pass  # Cria o arquivo se ele não existir
        except Exception as e:
            print(f"Erro ao criar o arquivo de log: {e}")

    def log(self, message):
        """
        Registra uma mensagem no arquivo de log com um timestamp.

        Args:
            message (str): A mensagem a ser registrada no arquivo de log.

        Returns:
            None
        """
        try:
            with open(self.log_file, 'a') as file:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"[{timestamp}] [{self.param}] - {message}\n"
                file.write(log_entry)
            print(log_entry)
        except Exception as e:
            print(f"Erro ao escrever no arquivo de log: {e}")


'''
#
#====== Iniciando lógica
#
'''

class InsertTransactionsCache():
    def __init__(self):
        # Usa a função de conexão do db.py
        self.connection = pega_conexao_bd()

    def consulta_bd(self, query):
        resultados = True
        cursor = self.connection.cursor()
        cursor.execute(query)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    def insert_bd(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()

    def pd_results(self, query):
        df = pd.read_sql_query(query, self.connection)
        return df

    def converter_valor(self, valor):
        return "OK" if valor else "N EXISTE"
    
    def est_not_cache_xlsx(self, arrecadadora, inicio = "current_date - INTERVAL '9 Days'", fim = 'current_date'):
        dfs = []
        collectEstabelecimentos = """
        SELECT e.id_estabelecimento FROM arrecada.estabelecimentos e 
        JOIN arrecada.sub_redes sr ON sr.id_sub_rede = e.id_sub_rede 
        WHERE sr.id_arrecadadora = %i
        """ % (arrecadadora)
        
        #for i in self.consulta_bd(collectEstabelecimentos):
        consultaTransacoes = """
        SELECT 
            t2.id_estabelecimento estabelecimento,
            SUM(CASE WHEN ctl.id_transacao IS NULL THEN 1 ELSE 0 END) AS cache_transacoes_loja,
            SUM(CASE WHEN ctp.id_transacao IS NULL THEN 1 ELSE 0 END) AS cache_transacoes_pdv,
            SUM(CASE WHEN ctpp.id_transacao IS NULL THEN 1 ELSE 0 END) AS cache_transacoes_pdv_pe
        FROM arrecada.transacoes t 
        JOIN arrecada.terminais t2 ON t2.id_terminal = t.id_terminal 
        LEFT JOIN arrecada.cache_transacoes_loja ctl ON (ctl.id_transacao = t.id_transacao)
        LEFT JOIN arrecada.cache_transacoes_pdv ctp  ON (ctp.id_transacao = t.id_transacao)
        LEFT JOIN arrecada.cache_transacoes_pdv_pe ctpp ON (ctpp.id_transacao = t.id_transacao)
        WHERE t.id_arrecadadora = %i
        AND t.momento_cadastro::date BETWEEN %s AND  %s
        GROUP BY t2.id_estabelecimento;
        """ % (arrecadadora, inicio, fim)
        dfs.append(self.pd_results(consultaTransacoes))
        dfs = pd.concat(dfs, ignore_index=True)
        dfs.to_excel(f'{arrecadadora}_not_cache.xlsx', index=False) 
        self.connection.close()
        return 'Arquivo gerado'
    
    def get_transaction_in_cache(self, id_transacao):
        """
        Consulta as tabelas de cache com base no ID de transação fornecido.

        Parâmetros:
        id_transacao (str): O ID da transação que deve ser pesquisado nas tabelas de cache.

        Retorna:
        str: Uma mensagem indicando se o registro foi encontrado nas tabelas de cache ou não.
        """
        consultaTransacao = """
            SELECT t.id_transacao, ctl.id_cache_transacoes_loja, ctp.id_transacao, ctpp.id_transacao FROM arrecada.transacoes t 
            LEFT JOIN arrecada.cache_transacoes_loja ctl ON (ctl.id_transacao = t.id_transacao)
            LEFT JOIN arrecada.cache_transacoes_pdv ctp  ON (ctp.id_transacao = t.id_transacao)
            LEFT JOIN arrecada.cache_transacoes_pdv_pe ctpp ON (ctpp.id_transacao = t.id_transacao)
            WHERE t.id_transacao = %i
        """ % (id_transacao)
        consulta = self.consulta_bd(consultaTransacao)
        if consulta == []:
            return 'Não foi encontrado transações.'
        else:
            data = {
                'Tabela': ['cache_transacoes_loja', 'cache_transacoes_pdv', 'cache_transacoes_pdv_pe'],
                'Valor': [self.converter_valor(consulta[0][1]), self.converter_valor(consulta[0][2]), self.converter_valor(consulta[0][3])]
            }
            return pd.DataFrame(data)
    
    def insert_transaction_in_cache(self, id_transacao):
        consultaTransacao = """
            SELECT t.id_transacao, t.valor_pago, t.momento_cadastro, t.id_operador, t.id_terminal, t.id_convenio, 
            t.id_tipo_transacao, t.nsu, t.lote_pos, t2.id_loja, t.cb 
            FROM arrecada.transacoes t 
            JOIN arrecada.terminais t2 ON (t2.id_terminal = t.id_terminal) 
            WHERE t.id_transacao = %i
        """ % (id_transacao)

        consultaTransacaoCondicao = """
        SELECT t.id_transacao, ctl.id_cache_transacoes_loja, ctp.id_transacao, ctpp.id_transacao FROM arrecada.transacoes t 
        LEFT JOIN arrecada.cache_transacoes_loja ctl ON (ctl.id_transacao = t.id_transacao)
        LEFT JOIN arrecada.cache_transacoes_pdv ctp  ON (ctp.id_transacao = t.id_transacao)
        LEFT JOIN arrecada.cache_transacoes_pdv_pe ctpp ON (ctpp.id_transacao = t.id_transacao)
        WHERE t.id_transacao = %i
        """ % (id_transacao)
        consulta = self.consulta_bd(consultaTransacao)
        #print(consulta[0][2])

        cache_transacoes_loja = f"""
            INSERT INTO arrecada.cache_transacoes_loja
            (id_loja, cb, valor_pago, momento_cadastro, id_transacao)
            VALUES ({consulta[0][9]}, {consulta[0][10]}, {consulta[0][1]}, '{consulta[0][2]}', {consulta[0][0]});
        """
        cache_transacoes_pdv = f"""
            INSERT INTO arrecada.cache_transacoes_pdv 
            (id_transacao, valor_pago, momento_cadastro, id_operador, id_terminal, id_convenio)
            VALUES ({consulta[0][0]}, {consulta[0][1]}, '{consulta[0][2]}', {consulta[0][3]}, {consulta[0][4]}, {consulta[0][5]});
        """
        cache_transacoes_pdv_pe = f"""
            INSERT INTO arrecada.cache_transacoes_pdv_pe 
            (id_transacao, valor_pago, momento_cadastro, id_operador, id_terminal, id_convenio, id_tipo_transacao, nsu, lote_pos)
            VALUES ({consulta[0][0]}, {consulta[0][1]}, '{consulta[0][2]}', {consulta[0][3]}, {consulta[0][4]}, {consulta[0][5]}, {consulta[0][6]}, {consulta[0][7]}, {consulta[0][8]});
        """
        try:
            verifica = self.consulta_bd(consultaTransacaoCondicao)
            Logger(id_transacao).log(f'''Iniciando...''')
            Logger(id_transacao).log('''Verificando se transação existe nas caches...''')
            if not None in verifica[0]:
                Logger(id_transacao).log(f'''Todas as tabelas de cache estão devidamente preenchidas para a transação {id_transacao}''')
            if verifica[0][1] is None:
                self.insert_bd(cache_transacoes_loja)
                Logger(id_transacao).log(f'''cache_transacoes_loja...ok''')
            if verifica[0][2] is None:
                self.insert_bd(cache_transacoes_pdv)
                Logger(id_transacao).log(f'''cache_transacoes_pdv...ok''')
            if verifica[0][3] is None:
                self.insert_bd(cache_transacoes_pdv_pe)
                Logger(id_transacao).log(f'''cache_transacoes_pdv_pe...ok''')
            self.connection.close()
            Logger(id_transacao).log(f'''Fim do Script''')
        except ValueError:
            Logger(id_transacao).log(f'''Não foi possível encontrar transações''')
            self.connection.close()
        except Exception as e:
            Logger(id_transacao).log(f'''Erros encontrados.''')
            Logger(id_transacao).log(f'''{e}''')
            self.connection.close()

def insert_cache_from_other_script(id_transacao):
    obj = InsertTransactionsCache()
    obj.insert_transaction_in_cache(id_transacao)
    

'''
#
#======= MAIN()
#
'''

def main():
    while True:
        obj = InsertTransactionsCache()
        print('Informe o que deseja fazer:')
        print('1 - Consultar transação\n2 - Gerar Arquivo Quantitativo\n3 - Inserir transação nas tabelas cache\n0 - Sair')
        esc = int(input('==> '))
        if esc == 0:
            break
        elif esc == 1:
            os.system('clear')
            id_transacao = int(input('Informe o ID da transação: '))
            print('#-----------------------------------------#')
            print(obj.get_transaction_in_cache(id_transacao))
            print('#-----------------------------------------#')
        elif esc == 2:
            os.system('clear')
            id_transacao = int(input('Informe o ID da ARRECADADORA: '))
            print('#-----------------------------------------#')
            print(obj.est_not_cache_xlsx(id_transacao))
            print('#-----------------------------------------#')
        elif esc == 3:
            os.system('clear')
            id_transacao = int(input('Informe o ID da transação: '))
            print('#-----------------------------------------#')
            print(obj.insert_transaction_in_cache(id_transacao))
            print('#-----------------------------------------#')
        else:
            os.system('clear')
            print('#-----------------------------------------#')
            print('Opção Inválida...')
            print('#-----------------------------------------#')
    return


if __name__ == '__main__':
    main()
