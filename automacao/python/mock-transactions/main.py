from datetime import datetime
from db import pega_conexao_bd
from transacoes import trans_867, trans_892, trans_5bl, trans_867_juros, trans_pix, trans_4bl_pix, trans_alivio, trans_5bl_juros, trans_vt, deletar_transacao_pix


def verifica_operador(id_terminal):
    try:
        
        conn = pega_conexao_bd()
        cursor = conn.cursor()

        consulta_id_operador = """SELECT id_operador FROM arrecada.operadores WHERE id_terminal = %s"""    
        cursor.execute(consulta_id_operador, (id_terminal,))
        resultado_id_operador = cursor.fetchone()

        if resultado_id_operador:
            id_operador = resultado_id_operador[0]  # Armazena o id_operador
            print('ID Operador =', id_operador)
        else:
            print('Nenhum operador encontrado para este terminal.')
            return False, None, None, None  # Retorna False e None se não encontrar

        consulta_id_arr = """SELECT id_arrecadadora, id_loja, id_estabelecimento FROM arrecada.terminais WHERE id_terminal = %s"""    
        cursor.execute(consulta_id_arr, (id_terminal,))
        resultado_id_arr = cursor.fetchone()

        if resultado_id_arr:
            id_arr = resultado_id_arr[0]  # Armazena o id_arrecadadora
            id_loja = resultado_id_arr[1]   # Armazena o id_loja
            id_estabelecimento = resultado_id_arr[2]  # Armazena o id_estabelecimento
            print('ID Arrecadadora =', id_arr)
            print('ID Loja =', id_loja)
            print('ID Estabelecimento =', id_estabelecimento)
        else:
            print('Nenhum id arrecadadora ou id loja encontrado para este terminal.')
            return False, None, None, None  # Retorna False e None se não encontrar

        consulta_operador = """SELECT COUNT(*) FROM arrecada.operadores WHERE id_terminal = %s"""
        cursor.execute(consulta_operador, (id_terminal,))
        resultado_operador = cursor.fetchone()

        if resultado_operador and resultado_operador[0] >= 1:
            return id_operador, id_arr, id_loja, id_estabelecimento  # Retorna o id_operador, id_arrecadadora, id_loja e id_estabelecimento
        return False, None, None, None

    except Exception as e:
        print(f"Erro ao verificar operador: {e}")
        return False, None, None, None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def verificar_convenios(id_terminal, num_convenio):
    try:

        conn = pega_conexao_bd()
        cursor = conn.cursor()
  
        # Consulta SQL para verificar os convênios
        consulta = """
        SELECT COUNT(*), c.id_convenio
        FROM arrecada.tarifa_terminais tt
        INNER JOIN arrecada.convenios c ON tt.id_convenio = c.id_convenio
        WHERE tt.id_terminal = %s AND c.num_convenio = %s
        GROUP BY c.id_convenio;
        """
        cursor.execute(consulta, (id_terminal, num_convenio))
        resultado = cursor.fetchone()

        # if resultado[0] == 1:
        #     return True
        # return False

        if resultado[0] == 1:
            count, id_convenio = resultado
            return True, id_convenio
        return False, None
       


    except Exception as e:
        print(f"Erro ao verificar convênios: {e}")
        return False, None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def validar_data(data):
    try:
        # Tenta converter a data no formato 'YYYY-MM-DD'
        datetime.strptime(data, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def menu_transacoes():
    while True:
        id_terminal = input("Insira o id_terminal: ")
        id_operador, id_arr, id_loja, id_estabelecimento = verifica_operador(id_terminal)  

        if not id_operador:
            print("Erro ao verificar operador.")
            return
        
        print("\nEscolha uma transação:")
        print("1. Transacao 867")
        print("2. Transacao 892")
        print("3. Transacao 5 blocos")
        print("4. Transacao 867 com juros")
        print("5. Transacao Pix")
        print("6. Transacao alivio")
        print("7. Transacao 5 blocos com juros")
        print("8. Transacao Vale transporte")
        print("9. Deletar transação PIX")
        print("10. Sair")

        opcao = input("\nDigite o número da transação desejada: ")
        print()

        if opcao == "1":
            print("Executando Transação 867...")
            convenio_verificado, id_convenio = verificar_convenios(id_terminal, '0867')
            if convenio_verificado:
                trans_867(id_terminal, id_operador, id_convenio, id_arr, id_loja)  
            else:
                print("Não tem a tarifa para essa transacao\n")

        elif opcao == "2":
            print("Executando Transação 892...")
            convenio_verificado, id_convenio = verificar_convenios(id_terminal, '359')
            if convenio_verificado:
                trans_892(id_terminal, id_operador, id_convenio, id_arr, id_loja)
            else:
                print("Não tem a tarifa para essa transacao\n")

        elif opcao == "3":
            print("Executando Transação 5 Blocos...")
            convenio_verificado, id_convenio = verificar_convenios(id_terminal, '0268')
            if convenio_verificado:
                trans_5bl(id_terminal, id_operador, id_convenio, id_arr, id_loja)
            else:
                print("Não tem a tarifa para essa transacao\n")

        elif opcao == "4":
            print("Executando Transação 867 com juros...")
            convenio_verificado, id_convenio = verificar_convenios(id_terminal, '0867')
            if convenio_verificado:
                trans_867_juros(id_terminal, id_operador, id_convenio, id_arr, id_loja)
            else:
                print("Não tem a tarifa para essa transacao\n")

        elif opcao == "5":
            print("Executando Transação Pix...")
            convenio_verificado, id_convenio = verificar_convenios(id_terminal, '0331')
            if convenio_verificado:
                trans_pix(id_terminal, id_operador, id_convenio, id_arr, id_loja)
            else:
                print("Não tem a tarifa para essa transacao\n")
            convenio_verificado, id_convenio = verificar_convenios(id_terminal, '0358')
            if convenio_verificado:
                trans_4bl_pix(id_terminal, id_operador, id_convenio, id_arr)
            else:
                print("Não tem a tarifa para essa transacao\n")

        elif opcao == "6":
            print("Executando Transação Alivio...")
            
            # Valida a data
            while True:
                data_trans = input("Insira a data da transacao (EX: 2025-01-01): ")
                if validar_data(data_trans):
                    break
                else:
                    print("Data inválida! Por favor, insira a data no formato correto (YYYY-MM-DD).")
            
            hora_trans = "08:45:13.000"
            data_hora = f"{data_trans} {hora_trans}"

            trans_alivio(id_terminal, id_operador, id_arr, id_estabelecimento, data_trans, data_hora)

        elif opcao == "7":
            print("Executando Transação 5 Blocos c/juros...")
            convenio_verificado, id_convenio = verificar_convenios(id_terminal, '0268')
            if convenio_verificado:
                trans_5bl_juros(id_terminal, id_operador, id_convenio, id_arr, id_loja)
            else:
                print("Não tem a tarifa para essa transacao\n")

        elif opcao == "8":
            print("Executando Transação Vale Transporte...")
            convenio_verificado, id_convenio = verificar_convenios(id_terminal, '6006')
            if convenio_verificado:
                trans_vt(id_terminal, id_operador, id_convenio, id_arr, id_loja)
            else:
                print("Não tem a tarifa para essa transacao\n")

        elif opcao == "9":
            print("Deletar transação PIX...")
            try:
                id_transacao_deletar = input("Informe o ID da transação que deseja deletar: ")
                if id_transacao_deletar.strip().isdigit():
                    deletar_transacao_pix(int(id_transacao_deletar))
                else:
                    print("ID inválido! Por favor, informe um número válido.\n")
            except Exception as e:
                print(f"Erro ao processar a solicitação: {e}\n")

        elif opcao == "10":
            print("Saindo do programa...")
            break  
        else:
            print("Opção inválida! Tente novamente.")

# Executa o menu
menu_transacoes()