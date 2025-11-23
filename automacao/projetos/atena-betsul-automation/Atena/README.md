# Automação de Testes Frontend - Atena

Projeto de testes automatizados frontend para a plataforma **Atena** (https://gestor-dev.sportingplay.info/) usando Cypress.

## 📋 Sobre o Projeto

Este projeto contém testes end-to-end (E2E) automatizados para validar as funcionalidades principais da plataforma Atena, incluindo:

- Login com autenticação de dois fatores (2FA)
- Navegação e elementos principais
- Funcionalidades do sistema

## 🚀 Pré-requisitos

- Node.js (versão 14 ou superior)
- npm ou yarn

## 📦 Instalação

1. Navegue até o diretório do projeto:
```bash
cd atena
```

2. Instale as dependências:
```bash
npm install
```

3. Instale o Cypress (se necessário):
```bash
npx cypress install
```

## 🧪 Executando os Testes

### Modo Interativo (Cypress Test Runner)

Para abrir o Cypress Test Runner e executar os testes de forma interativa:

```bash
npm run cy:open
```

### Modo Headless (linha de comando)

Para executar todos os testes em modo headless:

```bash
npm run cy:run
```

### Executar em Navegadores Específicos

```bash
# Chrome
npm run cy:run:chrome

# Firefox
npm run cy:run:firefox

# Edge
npm run cy:run:edge
```

### Executar Testes Específicos

```bash
# Executar um arquivo de teste específico
npx cypress run --spec "cypress/e2e/login-atena.cy.js"
```

## 🔐 Autenticação de Dois Fatores (2FA)

O projeto utiliza o pacote `otplib` para gerar códigos TOTP (Time-based One-Time Password) para autenticação de dois fatores.

O secret TOTP está configurado no `cypress.config.js` na variável de ambiente `TOTP_SECRET`.

## 📁 Estrutura do Projeto

```
atena/
├── cypress/
│   ├── e2e/                    # Arquivos de teste
│   │   └── login-atena.cy.js  # Teste de login com 2FA
│   ├── fixtures/               # Dados de teste
│   │   └── example.json
│   └── support/                # Comandos e configurações personalizadas
│       ├── e2e.js             # Configurações globais
│       └── commands.js        # Comandos personalizados
├── cypress.config.js           # Configuração do Cypress
├── package.json
└── README.md
```

## ⚙️ Configuração

O arquivo `cypress.config.js` contém as configurações principais:

- **baseUrl**: https://gestor-dev.sportingplay.info
- **viewportWidth**: 1920
- **viewportHeight**: 1080
- **defaultCommandTimeout**: 15000ms
- **video**: true (grava vídeos das execuções)
- **screenshotOnRunFailure**: true (captura screenshots em caso de falha)

### Variáveis de Ambiente

As credenciais estão configuradas no `cypress.config.js`:

- `USER_EMAIL`: Email do usuário
- `USER_PASSWORD`: Senha do usuário
- `TOTP_SECRET`: Secret para geração de código 2FA

## 📝 Comandos Personalizados

O projeto inclui comandos personalizados no arquivo `cypress/support/commands.js`:

- `cy.waitForElement(selector, timeout)` - Aguarda elemento estar visível
- `cy.navigateToSection(sectionName)` - Navega para uma seção específica
- `cy.elementExists(selector)` - Verifica se elemento existe sem falhar
- `cy.closeModals()` - Fecha modais e overlays
- `cy.clickSafe(selector, options)` - Clica com tratamento de elementos cobertos
- `cy.generateTOTP(secret)` - Gera código TOTP para 2FA

## 🐛 Troubleshooting

### Problemas Comuns

1. **Cypress não instala corretamente**
   ```bash
   npx cypress install --force
   ```

2. **Timeout em elementos**
   - Verifique se o site está acessível
   - Aumente o `defaultCommandTimeout` no `cypress.config.js`

3. **Testes falhando por elementos não encontrados**
   - A estrutura do site pode ter mudado
   - Verifique os seletores no arquivo de teste correspondente
   - Execute em modo interativo para debug: `npm run cy:open`

4. **Código 2FA não funciona**
   - Verifique se o secret TOTP está correto
   - Certifique-se de que o relógio do sistema está sincronizado

## 📊 Relatórios e Evidências

Após executar os testes, você encontrará:

- **Vídeos**: `cypress/videos/` - Gravações de todas as execuções
- **Screenshots**: `cypress/screenshots/` - Screenshots de falhas

## 📄 Licença

MIT

---

**Nota**: Este projeto é para fins de teste e automação. Certifique-se de ter permissão para testar a plataforma antes de executar os testes em produção.

