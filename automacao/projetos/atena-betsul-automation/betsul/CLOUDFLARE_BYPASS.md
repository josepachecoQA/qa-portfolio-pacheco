# Configurações para Contornar Cloudflare

## Técnicas Implementadas

### 1. **Desabilitar Chrome Web Security**
No `cypress.config.js`:
```javascript
chromeWebSecurity: false
```
- Permite contornar restrições CORS e outras políticas de segurança
- Facilita testes em sites protegidos por Cloudflare

### 2. **Headers Personalizados**
Configurado no `cypress/support/e2e.js`:
- **User-Agent**: Simula um navegador Chrome real
- **Accept**: Headers de navegador real
- **Accept-Language**: pt-BR, pt, en-US, en
- **Sec-Fetch-***: Headers de segurança modernos
- **Connection**: keep-alive

### 3. **Remover Detecção de Automação**
Técnicas aplicadas:
- Remover propriedade `navigator.webdriver`
- Adicionar propriedades do Chrome (`window.chrome`)
- Configurar `navigator.plugins` e `navigator.languages`
- Sobrescrever `navigator.permissions.query`

### 4. **Comandos Personalizados**
Criado arquivo `cypress/support/cloudflare-bypass.js` com:
- `cy.waitForCloudflare()`: Aguarda verificação do Cloudflare
- `cy.removeAutomationDetection()`: Remove detecção de automação
- `cy.visitWithCloudflareBypass()`: Visita página com bypass completo

## Como Usar

### Opção 1: Usar comando personalizado
```javascript
cy.visitWithCloudflareBypass('/')
```

### Opção 2: Usar visit normal (já configurado automaticamente)
```javascript
cy.visit('/')
// O bypass já está configurado automaticamente
```

### Opção 3: Aguardar Cloudflare manualmente
```javascript
cy.visit('/')
cy.waitForCloudflare()
cy.removeAutomationDetection()
```

## Limitações

⚠️ **Importante**: O Cloudflare está constantemente atualizando suas técnicas de detecção. Estas configurações podem não funcionar 100% do tempo, especialmente se:

- O Cloudflare detectar padrões suspeitos
- O site usar Cloudflare Bot Management avançado
- O Cloudflare exigir captcha ou verificação interativa

## Soluções Alternativas

Se as técnicas acima não funcionarem:

1. **Usar Cypress com Stealth Plugin** (requer instalação adicional)
2. **Usar Playwright** ao invés de Cypress (melhor suporte para bypass)
3. **Aguardar verificação manual** em modo headed
4. **Usar sessões do Cypress** para manter cookies entre testes

## Testando

Para testar se o bypass está funcionando:

```javascript
cy.visit('/')
cy.waitForCloudflare() // Aguarda verificação
cy.get('body').should('be.visible') // Verifica se página carregou
```

## Notas de Segurança

- Estas configurações são apenas para testes automatizados
- Não use para atividades maliciosas
- Respeite os termos de serviço do site

