#!/bin/bash

export DB_NAME=snetdb
export DB_USER=jose_neto
export DB_HOST=db1.ec2.servicenet.dev.br
export DB_PORT=7432
export DB_PASSWORD=d1d95855-eed8-4bc3-a2f6-612313cc0703
export LOGIN=jose.pacheco
export SENHA=Pacheco159.

while true; do
    echo "Escolha uma opção:"
    echo "1 - Script SubRede"
    echo "2 - Script Estabelecimento"
    echo "3 - Script Loja"
    echo "4 - Script Terminal"
    echo "5 - Script configuracao padrao"
    echo "6 - Script Perfil gcb arrecadadora"
    echo "7 - Script Perfil gcb sub rede"
    echo "8 - Script Perfil gcb estabelecimento"
    echo "9 - Script Perfil gcb terminal"
    echo "10 - Script backoffice"
    echo "11 - Script Consultor"
    echo "12 - Script Operador"
    echo "13 - Script Perfil Comissoes"
    echo "14 - Script Recolhedor"
    echo "15 - Script Prospeccao"
    echo "16 - Executar todos os scripts"
    read -p "Digite um número de 1 a 16: " opcao

    case $opcao in
        1)
            python3 create_subrede.py 
            break
            ;;
        2)
            python3 create_estabelecimento.py
            break
            ;;
        3)
            python3 create_loja.py
            break
            ;;
        4)
            python3 create_terminal.py
            break
            ;;
        5)
            python3 create_config_padrao.py
            break
            ;;
        6)
            python3 create_perfilgcb_arrecadadora.py
            break
            ;;
        7)
            python3 create_perfilgcb_subrede.py
            break
            ;;
        8)
            python3 create_perfilgcb_estabelecimento.py
            break
            ;;
        9)
            python3 create_perfilgcb_terminal.py
            break
            ;;
        10)
            python3 create_backoffice.py
            break
            ;;
        11)
            python3 create_consultor.py
            break
            ;;
        12)
            python3 create_operador.py
            break
            ;;
        13)
            python3 create_perfilcomissoes.py
            break
            ;;
        14)
            python3 create_recolhedor.py
            break
            ;;
        15)
            python3 create_prospeccao.py
            break
            ;;
        16)
            echo "Executando todos os scripts em cascata..."
            python3 create_subrede.py && \
            python3 create_estabelecimento.py && \
            python3 create_loja.py && \
            python3 create_terminal.py && \
            python3 create_config_padrao.py && \
            python3 create_perfilgcb_arrecadadora.py && \
            python3 create_perfilgcb_subrede.py && \
            python3 create_perfilgcb_estabelecimento.py && \
            python3 create_perfilgcb_terminal.py && \
            python3 create_backoffice.py && \
            python3 create_consultor.py && \
            python3 create_operador.py && \
            python3 create_perfilcomissoes.py && \
            python3 create_recolhedor.py && \
            python3 create_prospeccao.py
            break
            ;;
        *)
            echo "Opção inválida. Por favor, digite um número de 1 a 16."
            ;;
    esac
done
