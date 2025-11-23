# Automação de Testes Frontend - Betsul

Projeto de testes automatizados frontend para a plataforma de apostas esportivas [Betsul](https://www.betsul.online/) usando Cypress.

## 📋 Sobre o Projeto

Este projeto contém testes end-to-end (E2E) automatizados para validar as funcionalidades principais da plataforma Betsul, incluindo:

- Navegação e elementos principais
- Seções de esportes
- Funcionalidades de apostas
- Seção de cassino
- Responsividade

## 🚀 Pré-requisitos

- Node.js (versão 14 ou superior)
- npm ou yarn

## 📦 Instalação

1. Clone o repositório ou navegue até o diretório do projeto:
```bash
cd automacao_de_testes
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

Este comando abre a interface gráfica do Cypress onde você pode:
- Ver todos os testes disponíveis
- Executar testes individualmente
- Ver o navegador em tempo real durante a execução
- Ver screenshots e vídeos das execuções

### Modo Headless (linha de comando)

Para executar todos os testes em modo headless (sem interface gráfica):

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
npx cypress run --spec "cypress/e2e/navegacao.cy.js"

# Executar múltiplos arquivos
npx cypress run --spec "cypress/e2e/navegacao.cy.js,cypress/e2e/esportes.cy.js"
```

## 📁 Estrutura do Projeto

```
automacao_de_testes/
├── cypress/
│   ├── e2e/                    # Arquivos de teste
│   │   ├── navegacao.cy.js     # Testes de navegação
│   │   ├── esportes.cy.js      # Testes da seção de esportes
│   │   ├── apostas.cy.js       # Testes de funcionalidades de apostas
│   │   └── cassino.cy.js       # Testes da seção de cassino
│   ├── fixtures/               # Dados de teste
│   │   └── example.json
│   └── support/                # Comandos e configurações personalizadas
│       ├── e2e.js             # Configurações globais
│       └── commands.js        # Comandos personalizados
├── cypress.config.js           # Configuração do Cypress
├── package.json
└── README.md
```

## 🧩 Testes Disponíveis

### 1. Navegação (navegacao.cy.js)
- Carregamento da página inicial
- Verificação do logo
- Menus principais de navegação
- Navegação entre seções
- Elementos de notificação e perfil

### 2. Esportes (esportes.cy.js)
- Menu de esportes
- Esportes populares disponíveis
- Navegação para futebol
- Ligas e campeonatos
- Eventos ao vivo

### 3. Apostas (apostas.cy.js)
- Elementos relacionados a apostas
- Eventos disponíveis
- Funcionalidade de busca
- Favoritos
- Resultados
- Testes de responsividade

### 4. Cassino (cassino.cy.js)
- Navegação para Cassino
- Cassino Ao Vivo
- Jogos disponíveis
- E-Sports

## ⚙️ Configuração

O arquivo `cypress.config.js` contém as configurações principais:

- **baseUrl**: https://www.betsul.online
- **viewportWidth**: 1920
- **viewportHeight**: 1080
- **defaultCommandTimeout**: 10000ms
- **video**: true (grava vídeos das execuções)
- **screenshotOnRunFailure**: true (captura screenshots em caso de falha)

Você pode modificar essas configurações conforme necessário.

## 📝 Comandos Personalizados

O projeto inclui comandos personalizados no arquivo `cypress/support/commands.js`:

- `cy.waitForElement(selector, timeout)` - Aguarda elemento estar visível
- `cy.navigateToSection(sectionName)` - Navega para uma seção específica
- `cy.elementExists(selector)` - Verifica se elemento existe sem falhar

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

## 📊 Relatórios e Evidências

Após executar os testes, você encontrará:

- **Vídeos**: `cypress/videos/` - Gravações de todas as execuções
- **Screenshots**: `cypress/screenshots/` - Screenshots de falhas

## 🔄 Próximos Passos

Para expandir a cobertura de testes, considere adicionar:

- Testes de login/registro
- Testes de fluxo de apostas completo
- Testes de interação com carrinho de apostas
- Testes de filtros e busca avançada
- Testes de API (se aplicável)

## 📄 Licença

MIT

## 👤 Autor

Projeto criado para automação de testes da plataforma Betsul.

---

**Nota**: Este projeto é para fins de teste e automação. Certifique-se de ter permissão para testar a plataforma antes de executar os testes em produção.

