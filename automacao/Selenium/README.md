🤖 Automação Web com Selenium – Projeto de Portfólio
por José Pacheco da Silva Neto

Este diretório contém um projeto real desenvolvido em Python + Selenium WebDriver para automação de fluxos críticos do sistema interno.

🚀 Tecnologias utilizadas

Python

Selenium WebDriver

WebDriver Manager

PyAutoGUI

Requests

Estrutura baseada em módulos reutilizáveis

📁 Estrutura do Projeto
selenium/
├── GESTAO/               # Fluxos automatizados de gestão
├── REDE/                 # Automação de telas de rede e acessos
├── utils/                # Funções utilitárias gerais
│   └── ...
├── db_utils.py           # Funções de banco de dados
├── requirements.txt      # Dependências do projeto
└── README.md             # Este arquivo

▶️ Como executar
1️⃣ Criar ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

2️⃣ Instalar dependências
pip install -r requirements.txt

3️⃣ Executar um teste ou módulo
python GESTAO/nome_do_teste.py

🧠 Destaques técnicos

Uso de esperas explícitas no Selenium

Automação modular e reutilizável

Separação clara entre lógica, utilidades e fluxos

Scripts prontos para expansão

Organização profissional para equipes de QA
