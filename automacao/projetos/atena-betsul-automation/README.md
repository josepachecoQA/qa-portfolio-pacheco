🤖 Automação – Projetos Atena & Betsul
por José Pacheco da Silva Neto

Este diretório contém automações reais e documentação técnica utilizadas para estruturar, configurar e executar testes automatizados em dois sistemas distintos:

Atena – Sistema interno de gestão

Betsul – Plataforma de apostas esportivas

🚀 Tecnologias e Ferramentas Utilizadas
🔹 Automação

Python

Selenium

Requests

Estrutura modular

Page Objects

Scripts independentes de execução

🔹 DevOps / GitLab

Pipelines de CI

Configurações de repositório

Permissões de grupos

Templates de projeto

Setup automatizado via shell script (.gitlab-setup.sh)

🔹 QA

Testes Web

Testes funcionais

Testes de API

Validação de fluxos internos

Organização por módulos (Atena e Betsul)

📁 Estrutura do Diretório
atena-betsul-automation/
│
├── atena/
│   └── testes e automações específicas do sistema Atena
│
├── betsul/
│   └── automações aplicadas ao sistema Betsul
│
├── CRIAR_PROJETO_GITLAB.md     # Guia de criação de projeto GitLab
├── GITLAB_SETUP.md             # Setup automatizado do repositório
├── PERMISSOES_GITLAB.md        # Documentação de permissões e papéis
├── RESUMO_GITLAB.md            # Resumo técnico das configurações
├── .gitlab-setup.sh            # Script automatizador
└── README.md                   # Este arquivo
