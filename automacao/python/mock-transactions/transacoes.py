from db import pega_conexao_bd 
from TransactionsCacheMain import insert_cache_from_other_script
from contextlib import contextmanager

@contextmanager
def obter_conexao_bd():
    """
    Context manager para gerenciar conexão com o banco de dados.
    Garante que a conexão e cursor sejam fechados adequadamente.
    """
    conn = pega_conexao_bd()
    if conn is None:
        raise Exception("Conexão com o banco de dados falhou.")
    
    cursor = conn.cursor()
    try:
        yield conn, cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def trans_867(id_terminal, id_operador, id_convenio, id_arr, id_loja):
    """Executa o fluxo de inserção para a transação 867."""
    id_transacao = None
    try:
        with obter_conexao_bd() as (conn, cursor):
            print(f"💾 Inserindo transação com os seguintes dados: id_tipo_transacao=74, id_operador={id_operador}, id_convenio={id_convenio}, id_arrecadadora={id_arr}, id_terminal={id_terminal}\n")

            cursor.execute(f"""
                INSERT INTO arrecada.transacoes
                (id_tipo_transacao, id_operador, id_convenio, id_arrecadadora, id_terminal, nsu, momento_solicitacao, momento_resposta, momento_cadastro, tarifa, solicitacao, resposta, qtd_faturas, valor_pago, cb, id_conciliacao, pendente, estornada, lote_pos, autorizada, impressa, cupom_base64)
                VALUES (74, {id_operador}, {id_convenio}, {id_arr}, {id_terminal}, 2, 'now()', 'now()', 'now()', 0.01, 
                '00006721282700000010768320001000000010000000000000000000000000000000005867001P000000600000000000013426000000579000010004500011002030001100012004500019600000000013426000000337338341500111661700099001700000000000013426001130017000000000000134260047600190000000000000013426001150003002004540045A765739D0821B1B211SN00602105323312406100634430008800374984071163591582=27122060000025890770001360248777A82023C005F3401008407A000000003201057134984071163591582D27122060000025890770F9F02060000000000009F03060000000000009F1A020076950580800408005F2A0209869A032406109C01009F37042A1494B49F3501219F2701809F260896EB34D0EA1806BD9F360200329F100706050A03A0A81100180001620FA10001F803E5C001550016F24EA21B8383714B@', 
                '000067212827000000107683200010000000100000000000000000J9626262020201965867001P000000700000000000013426000001259F1254   COBAN:076832 LOJA:0001 PDV:000001  10/06/2024   BANCO DO BRASIL  06:34:43827076832 CORRESPONDENTE BANCARIO 0196                                         COMPROVANTE DE PAGAMENTO DE TITULOS                                      CLIENTE: JOSE LUIZ SOUSA OLIVEIRA     AGENCIA: 8270-8 CONTA:         2.243-8======================================BANCO DO BRASIL                       --------------------------------------001900000903373383417500111661756     00000000013426                        BENEFICIARIO:                         EQUATORIAL PIAUI DISTRIBUIDORA        NOME FANTASIA:                        EQUATORIAL PIAUI DISTRIBUIDORA DE E   CNPJ: 06.840.748/0001-89              PAGADOR:                              MARIA  DE DEMICIANA DE OLIVEIRA LIM   CPF: 005.449.353-65                   --------------------------------------NR. DOCUMENTO                   61.001DATA DO PAGAMENTO           10/06/2024VLR DOCUMENTO                   134,26VALOR COBRADO                   134,26======================================NR.AUTENTICACAO  0.A47.CAE.093.BC5.1EE--------------------------------------                                      SR(A) CLIENTE, ESTE SERVICO NAO TEM   TARIFA. NAO PAGUE NENHUM VALOR EXTRA  AO ATENDENTE. DENUNCIE 4004-0001.     ', 
                NULL, 134.26, '00196000000000134260000003373383415001116617', NULL, false, false, 1944, false, false, NULL);
                """)

            cursor.execute(f"""select id_transacao from arrecada.transacoes where id_terminal ={id_terminal}
                and momento_cadastro :: date = current_date order by id_transacao desc limit 1
                """)

            resultado = cursor.fetchone()

            if resultado:
                id_transacao = resultado[0]

                cursor.execute(f"""INSERT INTO arrecada.cache_transacoes_pdv
                    (id_transacao, valor_pago, momento_cadastro, id_operador, id_terminal, id_convenio)
                    VALUES({id_transacao}, 134.26, 'now()', {id_operador}, {id_terminal}, {id_convenio});""")

                cursor.execute(f"""INSERT INTO arrecada.cache_transacoes_pdv_pe
                    (id_transacao, valor_pago, momento_cadastro, id_operador, id_terminal, id_convenio, id_tipo_transacao, nsu, lote_pos)
                    VALUES({id_transacao}, 134.26, 'now()', {id_operador}, {id_terminal}, {id_convenio}, 74, 2, 1944)""")

                cursor.execute(f"""INSERT INTO arrecada.transacao_bb
                    (chave_j, agencia, tipo_trn, valor_desconto, valor_nominal, nr_autenticacao, inf_cheque, cedente, cod_autorizacao, fk_transacao, valor_pago, reimpressao, cupom_impressao, id_fechamento, loja, convenio, coban, lojase, pdv)
                    VALUES('J9626262', '8270', '5867', 0.00, 134.26, {id_transacao}, '', '', '0196', {id_transacao}, 134.26, NULL, '   COBAN:076832 LOJA:0001 PDV:000001  10/06/2024   BANCO DO BRASIL  06:34:43827076832 CORRESPONDENTE BANCARIO 0196                                         COMPROVANTE DE PAGAMENTO DE TITULOS                                      CLIENTE: JOSE LUIZ SOUSA OLIVEIRA     AGENCIA: 8270-8 CONTA:         2.243-8======================================BANCO DO BRASIL                       --------------------------------------001900000903373383417500111661756     00000000013426                        BENEFICIARIO:                         EQUATORIAL PIAUI DISTRIBUIDORA        NOME FANTASIA:                        EQUATORIAL PIAUI DISTRIBUIDORA DE E   CNPJ: 06.840.748/0001-89              PAGADOR:                              MARIA  DE DEMICIANA DE OLIVEIRA LIM   CPF: 005.449.353-65                   --------------------------------------NR. DOCUMENTO                   61.001DATA DO PAGAMENTO           10/06/2024VLR DOCUMENTO                   134,26VALOR COBRADO                   134,26======================================NR.AUTENTICACAO  0.A47.CAE.093.BC5.1EE--------------------------------------                                      SR(A) CLIENTE, ESTE SERVICO NAO TEM   TARIFA. NAO PAGUE NENHUM VALOR EXTRA  AO ATENDENTE. DENUNCIE 4004-0001.     ', NULL, '000001', '000067212', '076832', '0001', '00000001');""")

                cursor.execute(f"""INSERT INTO arrecada.cache_transacoes_loja
                    (id_loja, cb, valor_pago, momento_cadastro, id_transacao)
                    VALUES({id_loja}, '00196000000000134260000003373383415001116617', 134.26, 'now()', {id_transacao});""")

        if id_transacao:
            try:
                insert_cache_from_other_script(id_transacao)
            except Exception as cache_error:
                print(f"⚠️ Erro ao verificar cache para transação {id_transacao}: {cache_error}\n")
                print("⚠️ A transação foi inserida com sucesso, mas a verificação de cache falhou.\n")

            print("✅ Inserções para Tipo 867 realizadas com sucesso.\n")
        else:
            print("❌ Nenhuma transação encontrada para o terminal 29048 na data atual.\n")

    except Exception as e:
        print(f"❌ Erro ao realizar inserções para Tipo transação 867: {e}\n")


def trans_867_juros(id_terminal, id_operador, id_convenio, id_arr, id_loja):
    """Executa o fluxo de inserção para a transação 867."""
    id_transacao = None
    try:
        with obter_conexao_bd() as (conn, cursor):
            print(f"💾 Inserindo transação com os seguintes dados: id_tipo_transacao=74, id_operador={id_operador}, id_convenio={id_convenio}, id_arrecadadora={id_arr}, id_terminal={id_terminal}\n")

            cursor.execute(f"""
                INSERT INTO arrecada.transacoes
                (id_tipo_transacao, id_operador, id_convenio, id_arrecadadora, id_terminal, nsu, momento_solicitacao, momento_resposta, momento_cadastro, tarifa, solicitacao, resposta, qtd_faturas, valor_pago, cb, id_conciliacao, pendente, estornada, lote_pos, autorizada, impressa, cupom_base64)
                VALUES(74, {id_operador}, {id_convenio}, {id_arr}, {id_terminal}, 74, 'now()', 'now()', 'now()', 0.00, 
                '00005275032680000010164460001000000010000000000000000000000000000000005867001P00000060000000000012355400000062500001000450001100203000150001200450341979878000012355410901000540612480946490000009900170000000000012355400098001700000000000001974001130017000000000001255280047600195100000000000125528001150003002004540045AD69CA55FA21CFF581SN01204048991732410291545010008800376505710001583393=28082060000088290770001360268778183820279005F3401008407A000000494201057136505710001583393D28082060000088290770F9F02060000000000009F03060000000000009F1A020076950540800408005F2A0209869A032410299C01009F37043C90C02C9F3501219F2701809F26088C71A63B82948CEB9F360200869F10100205A00003400000011320000000000000180001620FA10001F8000790015500164800142D310CFE02@', '000052750326800000101644600010000000100000000000000000J9645279014601515867001P000000700000000000123554000001259F1254   COBAN:067212 LOJA:0279 PDV:000001  07/10/2024   BANCO DO BRASIL  07:07:20010667212 CORRESPONDENTE BANCARIO 0101                                        COMPROVANTE PAGAMENTOS COM COD.BARRA                                      AGENCIA: 0106-6 CONTA:        37.176-9CLIENTE: MARISE MAIA SALES            ======================================Convenio  SAAE CAMPO MAIOR            --------------------------------------    82620000000-9    93270373000-8        98840824240-0    11884900004-0    NR. DOCUMENTO                  100.733NR. CONVENIO                 118.273-0DATA DO PAGAMENTO           07/10/2024VALOR DO PAGAMENTO               93,27--------------------------------------NR.AUTENTICACAO  A.3BF.D00.FE0.F93.675--------------------------------------                                      SR(A) CLIENTE, ESTE SERVICO NAO TEM   TARIFA. NAO PAGUE NENHUM VALOR EXTRA  AO ATENDENTE. DENUNCIE 4004-0001.     ', NULL, 1235.54, '34197987800001235541090100054061248094649000', NULL, false, false, 89, false, false, NULL);
                """)

            cursor.execute(f"""select id_transacao from arrecada.transacoes where id_terminal ={id_terminal}
                and momento_cadastro :: date = current_date order by id_transacao desc limit 1
                """)

            resultado = cursor.fetchone()

            if resultado:
                id_transacao = resultado[0]

                cursor.execute(f"""      
                INSERT INTO arrecada.cache_transacoes_pdv
                (id_transacao, valor_pago, momento_cadastro, id_operador, id_terminal, id_convenio)
                VALUES({id_transacao}, 1235.54, 'now()', {id_operador}, {id_terminal}, {id_convenio});""")

                cursor.execute(f"""
                INSERT INTO arrecada.cache_transacoes_pdv_pe
                (id_transacao, valor_pago, momento_cadastro, id_operador, id_terminal, id_convenio, id_tipo_transacao, nsu, lote_pos)
                VALUES({id_transacao}, 1235.54, 'now()', {id_operador}, {id_terminal}, {id_convenio}, 74, 74, 89);""")

                cursor.execute(f"""
                INSERT INTO arrecada.transacao_bb
                (chave_j, agencia, tipo_trn, valor_desconto, valor_nominal, nr_autenticacao, inf_cheque, cedente, cod_autorizacao, fk_transacao, valor_pago, reimpressao, cupom_impressao, id_fechamento, loja, convenio, coban, lojase, pdv, valor_juros)
                VALUES('J9645279', '3268', '5867', 0.00, 1235.54, '{id_transacao}', '', '', '0151', {id_transacao}, 1255.28, NULL, '   COBAN:016446 LOJA:0001 PDV:000001  29/10/2024   BANCO DO BRASIL  15:45:01326816446 CORRESPONDENTE BANCARIO 0151                                         COMPROVANTE DE PAGAMENTO DE TITULOS                                      CLIENTE: IVONILDO UMBELINO SILVA      AGN: 3268-9  CTA:     12037-5  VAR: 51======================================ITAU UNIBANCO S.A.                    --------------------------------------341910901600054061247809464900027     98780000123554                        BENEFICIARIO:                         BANCO DAYCOVAL SA                     NOME FANTASIA:                        BANCO DAYCOVAL SA                     CNPJ: 62.232.889/0001-90              BENEFICIARIO FINAL:                   BETA COMERCIAL IMPORTADORA LTD        CNPJ: 09.557.640/0001-71              PAGADOR:                              ILNARA CELESTE DA SILVA E SILV        CNPJ: 22.475.749/0001-28              --------------------------------------NR. DOCUMENTO                  102.901DATA DE VENCIMENTO          23/10/2024DATA DO PAGAMENTO           29/10/2024VLR DOCUMENTO                 1.235,54JUROS/MULTA                      19,74VALOR COBRADO                 1.255,28======================================                                      NR.AUTENTICACAO  4.515.FFF.A22.89C.339--------------------------------------                                      SR(A) CLIENTE, ESTE SERVICO NAO TEM   TARIFA. NAO PAGUE NENHUM VALOR EXTRA  AO ATENDENTE. DENUNCIE 4004-0001.     ', NULL, '000001', '000052750', '016446', '0001', '00000001', 19.74);""")

                cursor.execute(f"""
                INSERT INTO arrecada.cache_transacoes_loja
                (id_loja, cb, valor_pago, momento_cadastro, id_transacao)
                VALUES({id_loja}, '34197987800001235541090100054061248094649000', 1235.54, 'now()', {id_transacao});""")

        if id_transacao:
            try:
                insert_cache_from_other_script(id_transacao)
            except Exception as cache_error:
                print(f"⚠️ Erro ao verificar cache para transação {id_transacao}: {cache_error}\n")
                print("⚠️ A transação foi inserida com sucesso, mas a verificação de cache falhou.\n")

            print("✅ Inserções para Tipo 867 realizadas com sucesso.\n")
        else:
            print(f"❌ Nenhuma transação encontrada para o terminal {id_terminal} na data atual.\n")

    except Exception as e:
        print(f"❌ Erro ao realizar inserções para Tipo transação 867: {e}\n")


def trans_892(id_terminal, id_operador, id_convenio, id_arr, id_loja):
    """Executa o fluxo de inserção para a transação 892."""
    id_transacao = None
    try:
        with obter_conexao_bd() as (conn, cursor):
            print(f"💾 Inserindo transação com os seguintes dados: id_tipo_transacao=73, id_operador={id_operador}, id_convenio={id_convenio}, id_arrecadadora={id_arr}, id_terminal={id_terminal}\n")
            
            cursor.execute(f"""INSERT INTO arrecada.transacoes
                (id_tipo_transacao, id_operador, id_convenio, id_arrecadadora, id_terminal, nsu, momento_solicitacao, momento_resposta, momento_cadastro, tarifa, solicitacao, resposta, qtd_faturas, valor_pago, cb, id_conciliacao, pendente, estornada, lote_pos, autorizada, impressa, cupom_base64)
                VALUES(73, {id_operador}, {id_convenio}, {id_arr}, {id_terminal}, 0, 'now()', 'now()', 'now()', 0.01, '00006721201060000010672120279000000010000000000000000000000000000000005892001P000001300000000000009327000000660000020045200448262000000093270373000988408242401188490000400066000100011700049327004510008071020240004400013001360272778185820239005F3401008407A000000004306057135464529251262644D26112060000095290770F9F02060000000000009F03060000000000009F1A020076950580800408005F2A0209869A032410079C01009F37041CF8A41E9F3501219F2701809F2608B893D53102A962829F360217129F10120310A00003220000000000000000000000FF0008800375464529251262644=2611206000009529077000180001620FA10001F8021CB0015500160F272FF53AF619160044700080011011900448000404090044900011004500016DFCF079AA85365170045401000300000000000009327361391402001118273000007102024826200000009327037300098840824240118849000040000001@', '000067212010600000106721202790000000100000000000000000J9626274009801015892001P000001400000000000009327000000917F0912   COBAN:067212 LOJA:0279 PDV:000001  07/10/2024   BANCO DO BRASIL  07:07:20010667212 CORRESPONDENTE BANCARIO 0101                                        COMPROVANTE PAGAMENTOS COM COD.BARRA                                      AGENCIA: 0106-6 CONTA:        37.176-9CLIENTE: MARISE MAIA SALES            ======================================Convenio  SAAE CAMPO MAIOR            --------------------------------------    82620000000-9    93270373000-8        98840824240-0    11884900004-0    NR. DOCUMENTO                  100.733NR. CONVENIO                 118.273-0DATA DO PAGAMENTO           07/10/2024VALOR DO PAGAMENTO               93,27--------------------------------------NR.AUTENTICACAO  A.3BF.D00.FE0.F93.675--------------------------------------                                      SR(A) CLIENTE, ESTE SERVICO NAO TEM   TARIFA. NAO PAGUE NENHUM VALOR EXTRA  AO ATENDENTE. DENUNCIE 4004-0001.     ', NULL, 93.27, '82620000000932703730009884082424011884900004', NULL, false, false, 148, false, false, NULL);""")
            
            cursor.execute(f"""select id_transacao from arrecada.transacoes where id_terminal = {id_terminal} 
                and momento_cadastro :: date = current_date order by id_transacao desc limit 1
                """)

            resultado892 = cursor.fetchone()

            if resultado892:
                id_transacao = resultado892[0]

                cursor.execute(f"""INSERT INTO arrecada.cache_transacoes_pdv
                    (id_transacao, valor_pago, momento_cadastro, id_operador, id_terminal, id_convenio)
                    VALUES({id_transacao}, 93.27, 'now()', {id_operador}, {id_terminal}, {id_convenio});""")

                cursor.execute(f"""INSERT INTO arrecada.cache_transacoes_pdv_pe
                    (id_transacao, valor_pago, momento_cadastro, id_operador, id_terminal, id_convenio, id_tipo_transacao, nsu, lote_pos)
                    VALUES({id_transacao}, 93.27, 'now()', {id_operador}, {id_terminal}, {id_convenio}, 73, 0, 148);""")

                cursor.execute(f"""INSERT INTO arrecada.transacao_bb
                    (chave_j, agencia, tipo_trn, valor_desconto, valor_nominal, nr_autenticacao, inf_cheque, cedente, cod_autorizacao, fk_transacao, valor_pago, reimpressao, cupom_impressao, id_fechamento, loja, convenio, coban, lojase, pdv)
                    VALUES('J9626274', '0106', '5892', NULL, NULL,{id_transacao}, NULL, 'SAAE CAMPO MAIOR            ', '0101', {id_transacao}, 93.2700000000000000, NULL, '   COBAN:067212 LOJA:0279 PDV:000001  07/10/2024   BANCO DO BRASIL  07:07:20010667212 CORRESPONDENTE BANCARIO 0101                                        COMPROVANTE PAGAMENTOS COM COD.BARRA                                      AGENCIA: 0106-6 CONTA:        37.176-9CLIENTE: MARISE MAIA SALES            ======================================Convenio  SAAE CAMPO MAIOR            --------------------------------------    82620000000-9    93270373000-8        98840824240-0    11884900004-0    NR. DOCUMENTO                  100.733NR. CONVENIO                 118.273-0DATA DO PAGAMENTO           07/10/2024VALOR DO PAGAMENTO               93,27--------------------------------------NR.AUTENTICACAO  A.3BF.D00.FE0.F93.675--------------------------------------                                      SR(A) CLIENTE, ESTE SERVICO NAO TEM   TARIFA. NAO PAGUE NENHUM VALOR EXTRA  AO ATENDENTE. DENUNCIE 4004-0001.     ', NULL, '000001', '000067212', '067212', '0279', '00000001');""")

                cursor.execute(f"""INSERT INTO arrecada.cache_transacoes_loja
                    (id_loja, cb, valor_pago, momento_cadastro, id_transacao)
                    VALUES({id_loja}, '82620000000932703730009884082424011884900004', 93.27, 'now()', {id_transacao});""")

        if id_transacao:
            try:
                insert_cache_from_other_script(id_transacao)
            except Exception as cache_error:
                print(f"⚠️ Erro ao verificar cache para transação {id_transacao}: {cache_error}\n")
                print("⚠️ A transação foi inserida com sucesso, mas a verificação de cache falhou.\n")

            print("✅ Inserções para Tipo 892 realizadas com sucesso.\n")
        else:
            print(f"❌ Nenhuma transação encontrada para o terminal {id_terminal} na data atual.\n")
        
    except Exception as e:
        print(f"❌ Erro ao realizar inserções para Tipo transação 892: {e}\n")


def trans_5bl(id_terminal, id_operador, id_convenio, id_arr, id_loja):
    """Executa o fluxo de inserção para a transação 5 blocos."""
    id_transacao = None
    try:
        with obter_conexao_bd() as (conn, cursor):
            print(f"💾 Inserindo transação com os seguintes dados: id_tipo_transacao=3, id_operador={id_operador}, id_convenio={id_convenio}, id_arrecadadora={id_arr}, id_terminal={id_terminal}\n")

            cursor.execute(f"""INSERT INTO arrecada.transacoes
                (id_tipo_transacao, id_operador, id_convenio, id_arrecadadora, id_terminal, nsu, momento_solicitacao, momento_resposta, momento_cadastro, tarifa, solicitacao, resposta, qtd_faturas, valor_pago, cb, id_conciliacao, pendente, estornada, lote_pos, autorizada, impressa, cupom_base64)
                VALUES(3, {id_operador}, {id_convenio}, {id_arr}, {id_terminal}, 8, 'now()', 'now()', 'now()', 0.00, '000067212010600000106721202790000000100000000000000002J9613407009900005268001P00000080000000000003600000000023600001004540100A3512B17651B28BB81SN0100155210069241007070828                                                       0001200450260919866000003600001954709884674793500000000002200011001150003001000990005360000011300053600000021000820241011@', '000067212010600000106721202790000000100000000000000002J9626272010001035268001P00000100000000000003600000000144810108NU PAGAMENTOS - IP                      00202410072024100707082900000000000036000848DE1017E21129E26011102024F1330   COBAN:067212 LOJA:0037 PDV:000039  11/11/2024   BANCO DO BRASIL  09:57:42180321237 CORRESPONDENTE BANCARIO 0242                                        COMPROVANTE PAGAMENTOS COM COD.BARRA                                      ======================================NU PAGAMENTOS - IP                    --------------------------------------260901954870988467471935000000001     98660000036000                        BENEFICIARIO:                         NU PAGAMENTOS SA                      NOME FANTASIA:                        NU PAGAMENTOS SA                      CNPJ: 18.236.120/0001-58              BENEFICIARIO FINAL:                   NU PAGAMENTOS SA                      CNPJ: 18.236.120/0001-58              PAGADOR:                              INARA DE CASTRO NASCIMENTO            CPF: 052.653.643-82                   --------------------------------------NR. DOCUMENTO                2.790.001DATA DE VENCIMENTO          11/10/2024DATA DO PAGAMENTO           07/10/2024VLR DOCUMENTO                   360,00VALOR COBRADO                   360,00======================================NR.AUTENTICACAO  8.48D.E10.17E.211.29E--------------------------------------                                      SR(A) CLIENTE, ESTE SERVICO NAO TEM   TARIFA. NAO PAGUE NENHUM VALOR EXTRA  AO ATENDENTE. DENUNCIE 4004-0001.     ', NULL, 360.00, '26091986600000360000195470988467479350000000', NULL, false, false, 148, false, false, NULL);""")

            cursor.execute(f"""select id_transacao from arrecada.transacoes where id_terminal = {id_terminal} 
                and momento_cadastro :: date = current_date order by id_transacao desc limit 1
                """)

            id_transacao_5bl = cursor.fetchone()

            if id_transacao_5bl:
                id_transacao = id_transacao_5bl[0]

                cursor.execute(f"""INSERT INTO arrecada.cache_transacoes_pdv
                    (id_transacao, valor_pago, momento_cadastro, id_operador, id_terminal, id_convenio)
                    VALUES({id_transacao}, 360.00, 'now()', {id_operador}, {id_terminal}, {id_convenio});""")

                cursor.execute(f"""INSERT INTO arrecada.cache_transacoes_pdv_pe
                    (id_transacao, valor_pago, momento_cadastro, id_operador, id_terminal, id_convenio, id_tipo_transacao, nsu, lote_pos)
                    VALUES({id_transacao}, 360.00, 'now()', {id_operador}, {id_terminal}, {id_convenio}, 3, 8, 148);""")

                cursor.execute(f"""INSERT INTO arrecada.transacao_bb
                    (chave_j, agencia, tipo_trn, valor_desconto, valor_nominal, nr_autenticacao, inf_cheque, cedente, cod_autorizacao, fk_transacao, valor_pago, reimpressao, cupom_impressao, id_fechamento, loja, convenio, coban, lojase, pdv)
                    VALUES('J9626272', '0106', '5268', 0.01000000000000000000, 360.0000000000000000, {id_transacao}, NULL, 'NU PAGAMENTOS - IP                      ', '0103', {id_transacao}, 360.0000000000000000, NULL, '   COBAN:067212 LOJA:0279 PDV:000001  07/10/2024   BANCO DO BRASIL  07:08:29010621279 CORRESPONDENTE BANCARIO 0103                                         COMPROVANTE DE PAGAMENTO DE TITULOS                                      ======================================NU PAGAMENTOS - IP                    --------------------------------------260901954870988467471935000000001     98660000036000                        BENEFICIARIO:                         NU PAGAMENTOS SA                      NOME FANTASIA:                        NU PAGAMENTOS SA                      CNPJ: 18.236.120/0001-58              BENEFICIARIO FINAL:                   NU PAGAMENTOS SA                      CNPJ: 18.236.120/0001-58              PAGADOR:                              INARA DE CASTRO NASCIMENTO            CPF: 052.653.643-82                   --------------------------------------NR. DOCUMENTO                2.790.001DATA DE VENCIMENTO          11/10/2024DATA DO PAGAMENTO           07/10/2024VLR DOCUMENTO                   360,00VALOR COBRADO                   360,00======================================NR.AUTENTICACAO  8.48D.E10.17E.211.29E--------------------------------------                                      SR(A) CLIENTE, ESTE SERVICO NAO TEM   TARIFA. NAO PAGUE NENHUM VALOR EXTRA  AO ATENDENTE. DENUNCIE 4004-0001.     ', NULL, '000001', '000067212', '067212', '0279', '00000001');""")

                cursor.execute(f"""INSERT INTO arrecada.cache_transacoes_loja
                    (id_loja, cb, valor_pago, momento_cadastro, id_transacao)
                    VALUES({id_loja}, '26091986600000360000195470988467479350000000', 360.00, 'now()', {id_transacao})""")

        if id_transacao:
            try:
                insert_cache_from_other_script(id_transacao)
            except Exception as cache_error:
                print(f"⚠️ Erro ao verificar cache para transação {id_transacao}: {cache_error}\n")
                print("⚠️ A transação foi inserida com sucesso, mas a verificação de cache falhou.\n")

            print("✅ Inserções para 5 blocos realizadas com sucesso.\n")

    except Exception as e:
        print(f"❌ Erro ao realizar inserções para Tipo transação 5 blocos: {e}\n")


def trans_pix(id_terminal, id_operador, id_convenio, id_arr, id_loja):
    """Executa o fluxo de inserção para a transação PIX."""
    id_transacao = None
    try:
        with obter_conexao_bd() as (conn, cursor):
            print(f"💾 Inserindo transação com os seguintes dados: id_tipo_transacao=75, id_operador={id_operador}, id_convenio={id_convenio}, id_arrecadadora={id_arr}, id_terminal={id_terminal}\n")

            cursor.execute(f"""
                INSERT INTO arrecada.transacoes
                (id_tipo_transacao, id_operador, id_convenio, id_arrecadadora, id_terminal, nsu, momento_solicitacao, momento_resposta, momento_cadastro, tarifa, solicitacao, resposta, qtd_faturas, valor_pago, cb, id_conciliacao, pendente, estornada, lote_pos, autorizada, impressa, cupom_base64)
                VALUES(75, {id_operador}, {id_convenio}, {id_arr}, {id_terminal}, 1, now(), now(), now(), 0.00, 
                '{{"userID":1,"currency":"BRL","language":"PT-BR","email":"","name":"Usuário PSP - PIX","country":"","methodType":36,"value":-29.43,"additional":{{"debtorCnpj":"23468882000381","debtorName":"LOG CRED TECNOLOGIA COMERCIO E","infoAdictional":"SANTOS DUMONT","merchantPixKey":"0623180d-f15f-45ba-b6a4-d26390826ad6","pixTTL":"170","pixTxId":"51435507900003700392024112591583791","typeService":"Geracao de cobranca via PIX"}}}}',
                '{{"urlRedirect":"","merchantInvoiceID":"6744781ee2e87da700f2124e","extraInfo":{{"debtorCnpj":"23468882000381","debtorName":"LOG CRED TECNOLOGIA COMERCIO E SERVICOS LTDA","pixTTL":"170","qrcodeLink":"00020101021226850014br.gov.bcb.pix2563qrcodepix.bb.com.br/pix/v2/dd9c1103-0417-4d7b-9496-9ac1521429af520400005303986540529.435802BR5925LOG CRED TECNOLOGIA COMER6015LAURO DE FREITA62070503***63041FE8","merchantPixKey":"0623180d-f15f-45ba-b6a4-d26390826ad6","transactionID2":"51435507900003700392024112591583791","value":"29.43"}},"amount":0}}',
                NULL, -29.43, '82650000002914300081826910000000210601100001', NULL, false, false, 1824, true, true, NULL)
                returning id_transacao;
            """)

            id_transacao = cursor.fetchone()[0]

            cursor.execute(f"""
                INSERT INTO arrecada.cache_transacoes_pdv (id_transacao, valor_pago, momento_cadastro, id_operador, id_terminal, id_convenio)
                VALUES({id_transacao}, -29.43, now(), {id_operador}, {id_terminal}, {id_convenio});
            """)

            cursor.execute(f"""
                INSERT INTO arrecada.cache_transacoes_pdv_pe (id_transacao, valor_pago, momento_cadastro, id_operador, id_terminal, id_convenio, id_tipo_transacao, nsu, lote_pos)
                VALUES({id_transacao}, -29.43, now(), {id_operador}, {id_terminal}, {id_convenio}, 75, 0, 1824);
            """)

            cursor.execute(f"""
                INSERT INTO arrecada.transacoes_pix (momento_cadastro, valor_pago, id_transacao, id_transacao_app_parceiro, id_terminal, id_operador, id_convenio, nsu, lote, solicitacao_parceiro, resposta_parceiro, pendente, autorizada, estornada, momento_alteracao, id_transacao_psp, end_2_end_id, resposta_estorno, id_tipo_pagamento_pix, id_tipo_parceiro_pix)
                VALUES(now(), -29.43, {id_transacao}, '82650000002914300081826910000000210601100001', {id_terminal}, {id_operador}, {id_convenio}, 1, 1824, 
                '{{"userID":1,"currency":"BRL","language":"PT-BR","email":"","name":"Usuário PSP - PIX"}}', 
                '{{"urlRedirect":"","merchantInvoiceID":"6744781ee2e87da700f2124e"}}', 
                false, true, false, now(), '6744781ee2e87da700f2124e', 'E60746948202411251314A32310dLYnA', '', 1, 1);
            """)

            cursor.execute(f"""
                INSERT INTO arrecada.cache_transacoes_loja (id_loja, cb, valor_pago, momento_cadastro, id_transacao)
                VALUES({id_loja}, '82650000002914300081826910000000210601100001', -29.43, now(), {id_transacao});
            """)

        if id_transacao:
            try:
                insert_cache_from_other_script(id_transacao)
            except Exception as cache_error:
                print(f"⚠️ Erro ao verificar cache para transação {id_transacao}: {cache_error}\n")
                print("⚠️ A transação foi inserida com sucesso, mas a verificação de cache falhou.\n")

            print("✅ Inserções para PIX realizadas com sucesso.\n")

    except Exception as e:
        print(f"❌ Erro ao realizar inserções para Tipo transação PIX: {e}\n")


def trans_4bl_pix(id_terminal, id_operador, id_convenio, id_arr):
    """Executa o fluxo de inserção para a transação PIX."""
    id_transacao = None
    try:
        with obter_conexao_bd() as (conn, cursor):
            print(f"💾 Inserindo transação com os seguintes dados: id_tipo_transacao=4, id_operador={id_operador}, id_convenio={id_convenio}, id_arrecadadora={id_arr}, id_terminal={id_terminal}\n")

            cursor.execute(f"""INSERT INTO arrecada.transacoes
            (id_tipo_transacao, id_operador, id_convenio, id_arrecadadora, id_terminal, nsu, momento_solicitacao, momento_resposta, momento_cadastro, tarifa, solicitacao, resposta, qtd_faturas, valor_pago, cb, id_conciliacao, pendente, estornada, lote_pos, autorizada, impressa, cupom_base64)
            VALUES(4, {id_operador}, {id_convenio}, {id_arr}, {id_terminal}, 1, now(), now(), now(), 0.00, 
            '{{"userID":1,"currency":"BRL","language":"PT-BR","email":"","name":"Usuário PSP - PIX","country":"","methodType":36,"value":29.43,"additional":{{"debtorCnpj":"23468882000381","debtorName":"LOG CRED TECNOLOGIA COMERCIO E","infoAdictional":"SANTOS DUMONT","merchantPixKey":"0623180d-f15f-45ba-b6a4-d26390826ad6","pixTTL":"170","pixTxId":"51435507900003700392024112591583791","typeService":"Geracao de cobranca via PIX"}}}}',
            '{{"urlRedirect":"","merchantInvoiceID":"6744781ee2e87da700f2124e","extraInfo":{{"debtorCnpj":"23468882000381","debtorName":"LOG CRED TECNOLOGIA COMERCIO E SERVICOS LTDA","pixTTL":"170","qrcodeLink":"00020101021226850014br.gov.bcb.pix2563qrcodepix.bb.com.br/pix/v2/dd9c1103-0417-4d7b-9496-9ac1521429af520400005303986540529.435802BR5925LOG CRED TECNOLOGIA COMER6015LAURO DE FREITA62070503***63041FE8","merchantPixKey":"0623180d-f15f-45ba-b6a4-d26390826ad6","transactionID2":"51435507900003700392024112591583791","value":"29.43"}},"amount":0}}',
            NULL, 29.43, '82650000002914300081826910000000210601100001', NULL, false, false, 1824, true, true, NULL)
            returning id_transacao;""")

            id_transacao = cursor.fetchone()[0]

            cursor.execute(f"""
                INSERT INTO arrecada.cache_transacoes_pdv
            (id_transacao, valor_pago, momento_cadastro, id_operador, id_terminal, id_convenio)
            VALUES({id_transacao}, 29.43, now(), {id_operador}, {id_terminal}, {id_convenio});
            """)

            cursor.execute(f"""
                INSERT INTO arrecada.transacao_bb
            (chave_j, agencia, tipo_trn, valor_desconto, valor_nominal, nr_autenticacao, inf_cheque, cedente, cod_autorizacao, fk_transacao, valor_pago, reimpressao, cupom_impressao, id_fechamento, loja, convenio, coban, lojase, pdv, valor_juros)
            VALUES('J9626274', '1803', '5358', NULL, NULL, '{id_transacao}', NULL, 'CLARO S.A.                              ', '0242', {id_transacao}, 29.43, NULL, '   COBAN:067212 LOJA:0037 PDV:000039  11/11/2024   BANCO DO BRASIL  09:57:42180321237 CORRESPONDENTE BANCARIO 0242                                        COMPROVANTE PAGAMENTOS COM COD.BARRA                                      ======================================CONVENIO: CLARO S.A.                  -------------------------------------- 84840000000 41590162202 41015168018   23801117122                          NR. DOCUMENTO                  370.039NR. CONVENIO                 102.188-5DATA DO PAGAMENTO           11/11/2024VLR DO PAGAMENTO                 41,59======================================NR.AUTENTICACAO  9.9F3.44E.28F.E7F.2CF--------------------------------------                                      SR(A) CLIENTE, ESTE SERVICO NAO TEM   TARIFA. NAO PAGUE NENHUM VALOR EXTRA  AO ATENDENTE. DENUNCIE 4004-0001.     ', NULL, '000001', '000067212', '067212', '0037', '00000039', 0);
            """)

        if id_transacao:
            try:
                insert_cache_from_other_script(id_transacao)
            except Exception as cache_error:
                print(f"⚠️ Erro ao verificar cache para transação {id_transacao}: {cache_error}\n")
                print("⚠️ A transação foi inserida com sucesso, mas a verificação de cache falhou.\n")

            print("✅ Inserções para 4bl realizadas com sucesso.\n")

    except Exception as e:
        print(f"❌ Erro ao realizar inserções para Tipo transação PIX: {e}\n")


def trans_alivio(id_terminal, id_operador, id_arr, id_estabelecimento, data_trans, data_hora):
    """Executa o fluxo de inserção para a transação Alivio."""
    id_transacao = None
    try:
        with obter_conexao_bd() as (conn, cursor):
            print(f"💾 Inserindo transação com os seguintes dados: id_tipo_transacao=14, id_operador={id_operador}, id_convenio=NULL, id_arrecadadora={id_arr}, id_terminal={id_terminal}\n")

            cursor.execute(f"""INSERT INTO conciliacao.cbf801_alivios (id_especializacao_transacao, id_arrecadadora, id_estabelecimento, codigo_transacao, data_transacao, hora_transacao, valor, loja, pdv) 
                        VALUES(171, {id_arr}, {id_estabelecimento}, 337, '{data_trans}', '111740', 586.13, 1, 9999)""")
            
            cursor.execute(f"""INSERT INTO arrecada.transacoes
                        (id_tipo_transacao, id_operador, id_convenio, id_arrecadadora, id_terminal, nsu, momento_solicitacao, momento_resposta, momento_cadastro, tarifa, solicitacao, resposta, qtd_faturas, valor_pago, cb, id_conciliacao, pendente, estornada, lote_pos, autorizada, impressa, cupom_base64)
                        VALUES(14, {id_operador}, NULL, {id_arr}, {id_terminal}, 6, '{data_hora}', '{data_trans}', '{data_trans}', 0.00, '00006721226600000010478880001000478880000000000000000200000000000000005A01002C000000000000000000000000000000025000010001000047888310001@', '000067212266000000104788800010004788800000000000000002J9613588001500005A01002C0000001000000000000000000000007801004400000000000000000347110000001500000000960716F003818/12/19    BANCO DO BRASIL   08:45:13F0038                                      F0038      CONSULTA SALDO E ALIVIOS        F0038                                      F0038DATA.: 18.12.2019                     F0038COBAN: 207500759 LOJINHA SANTANA      F0038======================================F0038LOJA  TIPO ALIVIO    VALOR            F0038----  -------------  -----------------F00380000                 R$           0,00F0038                                      F0038TOTAL DE ALIVIOS.:   R$           0,00F0038--------------------------------------F0038TOT. RECEBIMENTOS:   R$         347,11F0038TOT. PAGAMENTOS..:   R$         150,00F0038SALDO ATUAL...(-):   R$       9.607,16F0038======================================', NULL, 9607.16, '', NULL, true, false, 529, false, false, NULL);""")

            cursor.execute(f"""
                SELECT id_transacao FROM arrecada.transacoes 
                WHERE id_terminal = {id_terminal} AND momento_cadastro::date = '{data_trans}'
                ORDER BY id_transacao DESC LIMIT 1;
            """)
            id_transacao_alivio = cursor.fetchone()

            if id_transacao_alivio:
                id_transacao = id_transacao_alivio[0]

                cursor.execute(f"""
                    INSERT INTO arrecada.alivios_bb
                    (saldo_atual, total_alivio, total_recebimento, total_pagamento, momento_cadastro, id_transacao)
                    VALUES(9607.16, 0.00, 347.11, 150.00, '{data_hora}', {id_transacao});""")

        if id_transacao:
            try:
                insert_cache_from_other_script(id_transacao)
            except Exception as cache_error:
                print(f"⚠️ Erro ao verificar cache para transação {id_transacao}: {cache_error}\n")
                print("⚠️ A transação foi inserida com sucesso, mas a verificação de cache falhou.\n")
            
            print("✅ Inserções para alivio realizadas com sucesso.\n")

    except Exception as e:
        print(f"❌ Erro ao realizar inserções para transação alivio: {e}\n")


def trans_5bl_juros(id_terminal, id_operador, id_convenio, id_arr, id_loja):
    """Executa o fluxo de inserção para a transação 5 blocos."""
    id_transacao = None
    try:
        with obter_conexao_bd() as (conn, cursor):
            print(f"💾 Inserindo transação com os seguintes dados: id_tipo_transacao=3, id_operador={id_operador}, id_convenio={id_convenio}, id_arrecadadora={id_arr}, id_terminal={id_terminal}\n")

            cursor.execute(f"""INSERT INTO arrecada.transacoes
            (id_tipo_transacao, id_operador, id_convenio, id_arrecadadora, id_terminal, nsu, momento_solicitacao, momento_resposta, momento_cadastro, tarifa, solicitacao, resposta, qtd_faturas, valor_pago, cb, id_conciliacao, pendente, estornada, lote_pos, autorizada, impressa, cupom_base64)
            VALUES(3, {id_operador}, {id_convenio}, {id_arr}, {id_terminal}, 7, 'now()', 'now()', 'now()', 0.00, '000066483103800000106690000010000000400000000000000002J9626702001200005268001P00000090000000000000406700000024500001004540100AEA41C9D51686D1731SN0190217518421250311062003                                                       0001200450756929988000000399013325010947385553919060010002200011001150003001000980002770009900043990001130004406700021000820250210@', '000066483103800000106690000010000000400000000000000002J9626702001300135268001P00000110000000000000406700000148610108BANCO SICOOB S.A.                       00202503112025031106200400000000000004067B29837C3B182252B75610022025F1368   COBAN:066900 LOJA:0001 PDV:000004  11/03/2025   BANCO DO BRASIL  06:20:04103890001 CORRESPONDENTE BANCARIO 0013                                         COMPROVANTE DE PAGAMENTO DE TITULOS                                      ======================================BANCO SICOOB S.A.                     --------------------------------------756913325401094738554539190600112     99880000003990                        BENEFICIARIO:                         USE TECH SOLUCOES EM PAGAMENTO        NOME FANTASIA:                        USE TECH SOLUCOES EM PAGAMENTOS LTD   CNPJ: 30.881.993/0001-19              BENEFICIARIO FINAL:                   FUNERARIA SAO LUIZ LTDA               CNPJ: 07.442.386/0001-30              PAGADOR:                              ADELICE PAULINA DA SILVA MORAIS       CPF: 025.380.504-05                   --------------------------------------NR. DOCUMENTO                   10.004DATA DE VENCIMENTO          10/02/2025DATA DO PAGAMENTO           11/03/2025VLR DOCUMENTO                    39,90JUROS/MULTA                       0,77VALOR COBRADO                    40,67======================================NR.AUTENTICACAO  B.298.37C.3B1.822.52B--------------------------------------                                      SR(A) CLIENTE, ESTE SERVICO NAO TEM   TARIFA. NAO PAGUE NENHUM VALOR EXTRA  AO ATENDENTE. DENUNCIE 4004-0001.     ', NULL, 40.67, '75692998800000039901332501094738555391906001', NULL, false, false, 168, false, false, NULL);""")

            cursor.execute(f"""select id_transacao from arrecada.transacoes where id_terminal = {id_terminal} 
                and momento_cadastro :: date = current_date order by id_transacao desc limit 1
                """)

            id_transacao_5bl = cursor.fetchone()

            if id_transacao_5bl:
                id_transacao = id_transacao_5bl[0]
                
                cursor.execute(f"""INSERT INTO arrecada.cache_transacoes_pdv
                    (id_transacao, valor_pago, momento_cadastro, id_operador, id_terminal, id_convenio)
                    VALUES({id_transacao}, 40.67, 'now()', {id_operador}, {id_terminal}, {id_convenio});""")

                cursor.execute(f"""INSERT INTO arrecada.cache_transacoes_pdv_pe
                    (id_transacao, valor_pago, momento_cadastro, id_operador, id_terminal, id_convenio, id_tipo_transacao, nsu, lote_pos)
                    VALUES({id_transacao}, 40.67, 'now()', {id_operador}, {id_terminal}, {id_convenio}, 3, 7, 168);""")

                cursor.execute(f"""INSERT INTO arrecada.transacao_bb
                    (chave_j, agencia, tipo_trn, valor_desconto, valor_nominal, nr_autenticacao, inf_cheque, cedente, cod_autorizacao, fk_transacao, valor_pago, reimpressao, cupom_impressao, id_fechamento, loja, convenio, coban, lojase, pdv, valor_juros)
                    VALUES('J9626702', '1038', '5268', 0.01000000000000000000, 0.77000000000000000000, {id_transacao}, NULL, 'BANCO SICOOB S.A.                       ', '0013', {id_transacao}, 40.6700000000000000, NULL, '   COBAN:066900 LOJA:0001 PDV:000004  11/03/2025   BANCO DO BRASIL  06:20:04103890001 CORRESPONDENTE BANCARIO 0013                                         COMPROVANTE DE PAGAMENTO DE TITULOS                                      ======================================BANCO SICOOB S.A.                     --------------------------------------756913325401094738554539190600112     99880000003990                        BENEFICIARIO:                         USE TECH SOLUCOES EM PAGAMENTO        NOME FANTASIA:                        USE TECH SOLUCOES EM PAGAMENTOS LTD   CNPJ: 30.881.993/0001-19              BENEFICIARIO FINAL:                   FUNERARIA SAO LUIZ LTDA               CNPJ: 07.442.386/0001-30              PAGADOR:                              ADELICE PAULINA DA SILVA MORAIS       CPF: 025.380.504-05                   --------------------------------------NR. DOCUMENTO                   10.004DATA DE VENCIMENTO          10/02/2025DATA DO PAGAMENTO           11/03/2025VLR DOCUMENTO                    39,90JUROS/MULTA                       0,77VALOR COBRADO                    40,67======================================NR.AUTENTICACAO  B.298.37C.3B1.822.52B--------------------------------------                                      SR(A) CLIENTE, ESTE SERVICO NAO TEM   TARIFA. NAO PAGUE NENHUM VALOR EXTRA  AO ATENDENTE. DENUNCIE 4004-0001.     ', NULL, '000001', '000066483', '066900', '0001', '00000004', 0);""")

                cursor.execute(f"""INSERT INTO arrecada.cache_transacoes_loja
                    (id_loja, cb, valor_pago, momento_cadastro, id_transacao)
                    VALUES({id_loja}, '75692998800000039901332501094738555391906001', 40.67, 'now()', {id_transacao});""")

        if id_transacao:
            try:
                insert_cache_from_other_script(id_transacao)
            except Exception as cache_error:
                print(f"⚠️ Erro ao verificar cache para transação {id_transacao}: {cache_error}\n")
                print("⚠️ A transação foi inserida com sucesso, mas a verificação de cache falhou.\n")
            
            print("✅ Inserções para 5 blocos realizadas com sucesso.\n")

    except Exception as e:
        print(f"❌ Erro ao realizar inserções para Tipo transação 5 blocos c/juros: {e}\n")


def trans_vt(id_terminal, id_operador, id_convenio, id_arr, id_loja):
    """Executa o fluxo de inserção para a transação Vale transporte blocos."""
    id_transacao = None
    try:
        with obter_conexao_bd() as (conn, cursor):
            print(f"💾 Inserindo transação com os seguintes dados: id_tipo_transacao=4026, id_operador={id_operador}, id_convenio={id_convenio}, id_arrecadadora={id_arr}, id_terminal={id_terminal}\n")

            cursor.execute(f"""INSERT INTO arrecada.transacoes
                (id_tipo_transacao, id_operador, id_convenio, id_arrecadadora, id_terminal, nsu, momento_solicitacao, momento_resposta, momento_cadastro, tarifa, solicitacao, resposta, qtd_faturas, valor_pago, cb, id_conciliacao, pendente, estornada, lote_pos, autorizada, impressa, cupom_base64)
                VALUES(4026, {id_operador}, {id_convenio}, {id_arr}, {id_terminal}, 1, 'now()', 'now()', 'now()', 0.00, '{{IDTerminal:105496 LoginOperador:51590 KSUID:2v8vZneRHFl87OSPqt1fsXeEj31 NSU:1 Lote:31 CardSerialNumber:5804060856884 TipoCredito:58 CodigoProduto:500 DescricaoProduto:Comum Valor:1}}',
                '{{StatusCode:200 Status:Confirmado Message:Venda Efetuada Cupom:       RECARGA VALE TRANSPORTE        --------------------------------------AUTR:                         20214178NSU Operadora:               281879933SERIAL:                  5804060856884PRODUTO:                         ComumVALOR:                         R$ 0,01--------------------------------------O Sinetram oferece tres opcoes de cartao PassaFacil com imagens do Teatro Amazonas, Ponte Phelippe Daou e do Rio Negro. Saiba como agendar a emissao do seu cartao comum, estudante ou vale transporte.}}', 
                0, 0.01, 'vt', NULL, false, false, 31, false, false, 
                '       RECARGA VALE TRANSPORTE        --------------------------------------AUTR:                         20214178NSU Operadora:               281879933SERIAL:                  5804060856884PRODUTO:                         ComumVALOR:                         R$ 0,01--------------------------------------O Sinetram oferece tres opcoes de cartao PassaFacil com imagens do Teatro Amazonas, Ponte Phelippe Daou e do Rio Negro. Saiba como agendar a emissao do seu cartao comum, estudante ou vale transporte.');""")

            cursor.execute(f"""select id_transacao from arrecada.transacoes where id_terminal = {id_terminal} 
                and momento_cadastro :: date = current_date order by id_transacao desc limit 1
                """)

            id_transacao_vt = cursor.fetchone()

            if id_transacao_vt:
                id_transacao = id_transacao_vt[0]

                cursor.execute(f"""INSERT INTO arrecada.transacao_vale_transporte
                    (id_transacao, id_terminal, id_operador, ksuid, nsu_pos, lote_pos, tipo_credito, id_produto, nome_produto, tarifa, valor, cupom_impressao, cupom_via_caixa, nsu_parceiro, momento_cadastro, comissao, numero_serial_cartao, hmnsu, status)
                    VALUES({id_transacao}, {id_terminal}, {id_operador}, {id_transacao}, 1, 31, 58, 500, 'Comum', 0.0000, 0.01, '       RECARGA VALE TRANSPORTE        --------------------------------------AUTR:                         20214178NSU Operadora:               281879933SERIAL:                  5804060856884PRODUTO:                         ComumVALOR:                         R$ 0,01--------------------------------------O Sinetram oferece tres opcoes de cartao PassaFacil com imagens do Teatro Amazonas, Ponte Phelippe Daou e do Rio Negro. Saiba como agendar a emissao do seu cartao comum, estudante ou vale transporte.', '       RECARGA VALE TRANSPORTE        --------------------------------------AUTR:                         20214178NSU Operadora:               281879933SERIAL:                  5804060856884PRODUTO:                         ComumVALOR:                         R$ 0,01--------------------------------------O Sinetram oferece tres opcoes de cartao PassaFacil com imagens do Teatro Amazonas, Ponte Phelippe Daou e do Rio Negro. Saiba como agendar a emissao do seu cartao comum, estudante ou vale transporte.', 281879933, 'now()', 0.0000, '5804060856884', 20214178, 'confirmada'::public."status_enum");""")

                cursor.execute(f"""INSERT INTO arrecada.cache_transacoes_pdv
                    (id_transacao, valor_pago, momento_cadastro, id_operador, id_terminal, id_convenio)
                    VALUES({id_transacao}, 0.01, 'now()', {id_operador}, {id_terminal}, {id_convenio});""")

                cursor.execute(f"""INSERT INTO arrecada.cache_transacoes_pdv_pe
                    (id_transacao, valor_pago, momento_cadastro, id_operador, id_terminal, id_convenio, id_tipo_transacao, nsu, lote_pos)
                    VALUES({id_transacao}, 0.01, 'now()', {id_operador}, {id_terminal}, {id_convenio}, 4026, 1, 31);""")

                cursor.execute(f"""INSERT INTO arrecada.cache_transacoes_loja
                    (id_loja, cb, valor_pago, momento_cadastro, id_transacao)
                    VALUES({id_loja}, 'vt', 0.01, 'now()', {id_transacao});""")

        if id_transacao:
            try:
                insert_cache_from_other_script(id_transacao)
            except Exception as cache_error:
                print(f"⚠️ Erro ao verificar cache para transação {id_transacao}: {cache_error}\n")
                print("⚠️ A transação foi inserida com sucesso, mas a verificação de cache falhou.\n")

            print("✅ Inserções para Vale realizadas com sucesso.\n")

    except Exception as e:
        print(f"❌ Erro ao realizar inserções para Tipo transação VT: {e}\n")


def deletar_transacao_pix(id_transacao):
    """
    Deleta a transação PIX e sua transação associada de 4 blocos.
    """
    try:
        with obter_conexao_bd() as (conn, cursor):
            cursor.execute(f"""
                SELECT id_transacao, id_tipo_transacao, valor_pago, momento_cadastro
                FROM arrecada.transacoes 
                WHERE id_transacao IN ({id_transacao}, {id_transacao + 1});
            """)
            
            resultados = cursor.fetchall()
            
            if not resultados:
                print(f"\n❌ Transação com ID {id_transacao} não encontrada.\n")
                return False
            
            print(f"\n📋 Transações encontradas:\n")
            for resultado in resultados:
                id_trans, id_tipo_trans, valor, momento = resultado
                print(f"   ID: {id_trans}")
                print(f"   Tipo: {id_tipo_trans}")
                print(f"   Valor: R$ {valor}")
                print(f"   Data: {momento}")
                print("   " + "-" * 40)
            
            confirmacao = input("\n⚠️  Deseja realmente deletar estas transações? (S/N): ").strip().upper()
            
            if confirmacao != 'S':
                print("\n❌ Operação cancelada pelo usuário.\n")
                return False
            
            print("\n🗑️  Deletando registros...")

            cursor.execute(f"""
                DELETE FROM arrecada.cache_transacoes_loja
                WHERE id_transacao IN ({id_transacao}, {id_transacao + 1});
            """)
            registros_deletados = cursor.rowcount
            print(f"   ✓ cache_transacoes_loja: {registros_deletados} registro(s) deletado(s)")

            cursor.execute(f"""
                DELETE FROM arrecada.cache_transacoes_pdv
                WHERE id_transacao IN ({id_transacao}, {id_transacao + 1});
            """)
            registros_deletados = cursor.rowcount
            print(f"   ✓ cache_transacoes_pdv: {registros_deletados} registro(s) deletado(s)")

            cursor.execute(f"""
                DELETE FROM arrecada.cache_transacoes_pdv_pe
                WHERE id_transacao IN ({id_transacao}, {id_transacao + 1});
            """)
            registros_deletados = cursor.rowcount
            print(f"   ✓ cache_transacoes_pdv_pe: {registros_deletados} registro(s) deletado(s)")

            cursor.execute(f"""
                DELETE FROM arrecada.cache_transacoes
                WHERE id_transacao IN ({id_transacao}, {id_transacao + 1});
            """)
            registros_deletados = cursor.rowcount
            print(f"   ✓ cache_transacoes: {registros_deletados} registro(s) deletado(s)")

            cursor.execute(f"""
                DELETE FROM arrecada.autorizacoes_estorno
                WHERE id_transacao = {id_transacao + 1};
            """)
            registros_deletados = cursor.rowcount
            print(f"   ✓ autorizacoes_estorno: {registros_deletados} registro(s) deletado(s)")
            
            cursor.execute(f"""
                DELETE FROM arrecada.transacoes_pix
                WHERE id_transacao = {id_transacao};
            """)
            registros_deletados = cursor.rowcount
            print(f"   ✓ transacoes_pix: {registros_deletados} registro(s) deletado(s)")
            
            cursor.execute(f"""
                DELETE FROM arrecada.transacao_bb
                WHERE fk_transacao = {id_transacao + 1};
            """)
            registros_deletados = cursor.rowcount
            print(f"   ✓ transacao_bb: {registros_deletados} registro(s) deletado(s)")
            
            cursor.execute(f"""
                DELETE FROM arrecada.transacoes
                WHERE id_transacao IN ({id_transacao}, {id_transacao + 1});
            """)
            registros_deletados = cursor.rowcount
            print(f"   ✓ transacoes: {registros_deletados} registro(s) deletado(s)")
            
            print(f"\n✅ Transações [{id_transacao}] e [{id_transacao + 1}] deletadas com sucesso!\n")
            return True
            
    except Exception as e:
        print(f"\n❌ Erro ao deletar transação {id_transacao}: {e}\n")
        return False