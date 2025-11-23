# Mapeamento de Formulários de Cadastro - Atena

**Sistema:** Gestor Atena

**Data do Mapeamento:** 05/11/2025, 09:12:17

**URL Base:** https://gestor-dev.sportingplay.info

**Total de Módulos:** 9

**Total de Telas com Formulários:** 21

---

## Módulo: Sites

### 1.1 Cadastro de Site

**Caminho de Navegação:** Sites > Cadastros

**Campos do Formulário:**

1. `nome_fantasia`
2. `dominio_principal`
3. `tipo_site`
4. `companyKey`
5. `status`
6. `tempo_max_cancelamento`
7. `tema`
8. `idioma_padrao`
9. `moeda_padrao`

**Ações Disponíveis:**

1. criar
2. editar
3. duplicar
4. excluir
5. exportar

**Dependências e Observações:**

1. deve possuir pelo menos uma carteira e domínio vinculados

---

### 1.2 Domínios

**Caminho de Navegação:** Sites > Domínios

**Campos do Formulário:**

1. `dominio`
2. `tipo`
3. `site_vinculado`

**Ações Disponíveis:**

1. cadastrar
2. editar
3. excluir

**Dependências e Observações:**

1. domínio deve estar ativo e resolvendo DNS

---

### 1.3 Carteiras

**Caminho de Navegação:** Sites > Carteiras

**Campos do Formulário:**

1. `nome`
2. `tipo`
3. `codigo_interno`
4. `moeda`
5. `site_vinculado`
6. `tipo_saldo`

**Ações Disponíveis:**

1. cadastrar
2. editar
3. vincular site

**Dependências e Observações:**

1. requer site existente

---

### 1.4 Métodos de Pagamento

**Caminho de Navegação:** Sites > Pagamentos > Métodos

**Campos do Formulário:**

1. `nome`
2. `tipo`
3. `provedor`
4. `carteira_destino`
5. `taxa`
6. `limite_minimo`
7. `limite_maximo`

**Ações Disponíveis:**

1. criar
2. editar
3. ativar
4. inativar

**Dependências e Observações:**

1. configuração prévia no backend pode ser necessária

---

### 1.5 Promoções

**Caminho de Navegação:** Sites > Promoções > Cadastros

**Campos do Formulário:**

1. `titulo`
2. `descricao`
3. `validade`
4. `mercado`
5. `tipo`
6. `idTemplate`
7. `exibeSite`
8. `restrTypeText`
9. `fatorRollover`
10. `cupom`
11. `link`

**Ações Disponíveis:**

1. criar
2. editar
3. publicar
4. excluir

**Dependências e Observações:**

1. template e cupom devem estar configurados

---

### 1.6 Integrações

**Caminho de Navegação:** Sites > Integrações

**Campos do Formulário:**

1. `recaptcha_key`
2. `api_pix_client_id`
3. `api_pix_secret`
4. `chat_api_key`
5. `pesquisa_satisfacao_url`
6. `analytics_key`

**Ações Disponíveis:**

1. salvar
2. testar conexao

**Dependências e Observações:**

1. acesso restrito a usuários root

---

### 1.7 Configurações Gerais

**Caminho de Navegação:** Sites > Configurações

**Campos do Formulário:**

1. `tema`
2. `cores`
3. `cache`
4. `politica_privacidade`
5. `bloqueios_regionais`

**Ações Disponíveis:**

1. salvar
2. aplicar

**Dependências e Observações:**

1. alterações refletem em tempo real

---

## Módulo: Usuários

### 2.1 Cadastro de Usuários

**Caminho de Navegação:** Usuários > Cadastros

**Campos do Formulário:**

1. `nome_completo`
2. `email`
3. `login`
4. `senha`
5. `perfil`
6. `site_vinculado`

**Ações Disponíveis:**

1. criar
2. editar
3. resetar senha
4. bloquear

**Dependências e Observações:**

1. perfil e permissões devem estar configurados

---

### 2.2 Perfis e Permissões

**Caminho de Navegação:** Usuários > Perfis

**Campos do Formulário:**

1. `nome_perfil`
2. `descricao`
3. `modulos_acessiveis`
4. `permissoes_crud`

**Ações Disponíveis:**

1. criar
2. clonar
3. editar

**Dependências e Observações:**

1. controla acesso a funcionalidades sensíveis como WhatsApp e Chat

---

## Módulo: Financeiro

### 3.1 Carteiras e Saldos

**Caminho de Navegação:** Financeiro > Carteiras

**Campos do Formulário:**

1. `nome`
2. `saldo`
3. `tipo`
4. `site_vinculado`

**Ações Disponíveis:**

1. editar saldo
2. consultar historico

**Dependências e Observações:**

1. deve estar vinculada a um site

---

### 3.2 Saques e Depósitos

**Caminho de Navegação:** Financeiro > Movimentações

**Campos do Formulário:**

1. `tipo_transacao`
2. `valor`
3. `data`
4. `operador`
5. `status`

**Ações Disponíveis:**

1. aprovar
2. reprovar
3. cancelar

**Dependências e Observações:**

1. validação via API PSP (Paybrokers, BigPag, Bucks)

---

## Módulo: Jogos

### 4.1 Cadastro de Jogos

**Caminho de Navegação:** Jogos > Cadastros

**Campos do Formulário:**

1. `nome`
2. `provedor`
3. `tipo`
4. `rtp`
5. `volatilidade`
6. `status`

**Ações Disponíveis:**

1. cadastrar
2. editar
3. publicar

**Dependências e Observações:**

1. integração com RGS necessária

---

### 4.2 Categorias de Jogos

**Caminho de Navegação:** Jogos > Categorias

**Campos do Formulário:**

1. `nome`
2. `ordem_exibicao`
3. `icone`

**Ações Disponíveis:**

1. criar
2. editar
3. ordenar

---

## Módulo: Relatórios

### 5.1 Relatório de Sites

**Caminho de Navegação:** Relatórios > Sites

**Campos do Formulário:**

1. `site`
2. `periodo`
3. `status`

**Ações Disponíveis:**

1. filtrar
2. exportar csv
3. exportar pdf

---

### 5.2 Relatório de Transações

**Caminho de Navegação:** Relatórios > Financeiro > Transações

**Campos do Formulário:**

1. `tipo`
2. `data`
3. `status`
4. `operador`

**Ações Disponíveis:**

1. filtrar
2. exportar
3. exibir detalhes

---

## Módulo: Configurações do Sistema

### 6.1 Parâmetros Globais

**Caminho de Navegação:** Configurações > Parâmetros

**Campos do Formulário:**

1. `companyKey`
2. `ambiente`
3. `url_api`
4. `controle_sessao`
5. `modo_manutencao`

**Ações Disponíveis:**

1. atualizar
2. aplicar

**Dependências e Observações:**

1. requer acesso root

---

### 6.2 Logs do Sistema

**Caminho de Navegação:** Configurações > Logs

**Campos do Formulário:**

1. `data`
2. `usuario`
3. `modulo`
4. `acao`

**Ações Disponíveis:**

1. filtrar
2. exportar

**Dependências e Observações:**

1. armazenamento rotativo diário

---

## Módulo: Comunicação

### 7.1 WhatsApp

**Caminho de Navegação:** Comunicação > WhatsApp

**Campos do Formulário:**

1. `token_integracao`
2. `canal`
3. `mensagem_padrao`

**Ações Disponíveis:**

1. conectar
2. desconectar
3. testar

**Dependências e Observações:**

1. requer permissão root

---

### 7.2 Chat Online

**Caminho de Navegação:** Comunicação > Chat

**Campos do Formulário:**

1. `provedor`
2. `token_api`
3. `tempo_resposta`

**Ações Disponíveis:**

1. ativar
2. desativar

---

## Módulo: Pesquisa de Satisfação

### 8.1 Configuração de Pesquisa

**Caminho de Navegação:** Pesquisa > Configurações

**Campos do Formulário:**

1. `tipo_envio`
2. `metodo`
3. `mensagem_texto`
4. `link_externo`

**Ações Disponíveis:**

1. salvar
2. testar envio

**Dependências e Observações:**

1. pode estar vinculado ao módulo de agendamento do Medicalsys

---

## Módulo: Segurança

### 9.1 Controle de Acesso

**Caminho de Navegação:** Segurança > Controle de Acesso

**Campos do Formulário:**

1. `logs_login`
2. `tentativas_falhas`
3. `sessoes_ativas`

**Ações Disponíveis:**

1. encerrar sessao
2. bloquear usuario

---

## Resumo Geral

### Estatísticas por Módulo

- **Sites:** 7 tela(s) com formulário
- **Usuários:** 2 tela(s) com formulário
- **Financeiro:** 2 tela(s) com formulário
- **Jogos:** 2 tela(s) com formulário
- **Relatórios:** 2 tela(s) com formulário
- **Configurações do Sistema:** 2 tela(s) com formulário
- **Comunicação:** 2 tela(s) com formulário
- **Pesquisa de Satisfação:** 1 tela(s) com formulário
- **Segurança:** 1 tela(s) com formulário

### Total de Campos por Módulo

- **Sites:** 47 campo(s)
- **Usuários:** 10 campo(s)
- **Financeiro:** 9 campo(s)
- **Jogos:** 9 campo(s)
- **Relatórios:** 7 campo(s)
- **Configurações do Sistema:** 9 campo(s)
- **Comunicação:** 6 campo(s)
- **Pesquisa de Satisfação:** 4 campo(s)
- **Segurança:** 3 campo(s)

### Total de Ações por Módulo

- **Sites:** 23 ação(ões)
- **Usuários:** 7 ação(ões)
- **Financeiro:** 5 ação(ões)
- **Jogos:** 6 ação(ões)
- **Relatórios:** 6 ação(ões)
- **Configurações do Sistema:** 4 ação(ões)
- **Comunicação:** 5 ação(ões)
- **Pesquisa de Satisfação:** 2 ação(ões)
- **Segurança:** 2 ação(ões)

---

## Índice de Telas

### Sites

1.1. [Cadastro de Site](#11-cadastro-de-site) - Sites > Cadastros
1.2. [Domínios](#12-domínios) - Sites > Domínios
1.3. [Carteiras](#13-carteiras) - Sites > Carteiras
1.4. [Métodos de Pagamento](#14-métodos-de-pagamento) - Sites > Pagamentos > Métodos
1.5. [Promoções](#15-promoções) - Sites > Promoções > Cadastros
1.6. [Integrações](#16-integrações) - Sites > Integrações
1.7. [Configurações Gerais](#17-configurações-gerais) - Sites > Configurações

### Usuários

2.1. [Cadastro de Usuários](#21-cadastro-de-usuários) - Usuários > Cadastros
2.2. [Perfis e Permissões](#22-perfis-e-permissões) - Usuários > Perfis

### Financeiro

3.1. [Carteiras e Saldos](#31-carteiras-e-saldos) - Financeiro > Carteiras
3.2. [Saques e Depósitos](#32-saques-e-depósitos) - Financeiro > Movimentações

### Jogos

4.1. [Cadastro de Jogos](#41-cadastro-de-jogos) - Jogos > Cadastros
4.2. [Categorias de Jogos](#42-categorias-de-jogos) - Jogos > Categorias

### Relatórios

5.1. [Relatório de Sites](#51-relatório-de-sites) - Relatórios > Sites
5.2. [Relatório de Transações](#52-relatório-de-transações) - Relatórios > Financeiro > Transações

### Configurações do Sistema

6.1. [Parâmetros Globais](#61-parâmetros-globais) - Configurações > Parâmetros
6.2. [Logs do Sistema](#62-logs-do-sistema) - Configurações > Logs

### Comunicação

7.1. [WhatsApp](#71-whatsapp) - Comunicação > WhatsApp
7.2. [Chat Online](#72-chat-online) - Comunicação > Chat

### Pesquisa de Satisfação

8.1. [Configuração de Pesquisa](#81-configuração-de-pesquisa) - Pesquisa > Configurações

### Segurança

9.1. [Controle de Acesso](#91-controle-de-acesso) - Segurança > Controle de Acesso

