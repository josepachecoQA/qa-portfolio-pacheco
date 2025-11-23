// ***********************************************
// Este arquivo contém comandos para contornar Cloudflare
// ***********************************************

/// <reference types="cypress" />

/**
 * Comando para aguardar verificação do Cloudflare
 */
Cypress.Commands.add('waitForCloudflare', (timeout = 30000) => {
  cy.log('Aguardando verificação do Cloudflare...')
  
  // Aguardar que o body esteja visível (indicando que passou Cloudflare)
  cy.get('body', { timeout }).should('be.visible')
  
  // Aguardar que não haja elementos de verificação do Cloudflare
  cy.get('body').then(($body) => {
    const hasCloudflareCheck = $body.find('[class*="cf-"], [id*="cf-"], [class*="cloudflare"], [id*="cloudflare"]').length > 0
    if (hasCloudflareCheck) {
      cy.log('Elementos do Cloudflare detectados, aguardando...')
      cy.wait(3000)
    }
  })
  
  cy.log('Verificação do Cloudflare concluída')
})

/**
 * Comando para remover detecção de automação
 */
Cypress.Commands.add('removeAutomationDetection', () => {
  cy.window().then((win) => {
    // Remover propriedade webdriver
    Object.defineProperty(win.navigator, 'webdriver', {
      get: () => undefined
    })
    
    // Adicionar propriedades do Chrome
    if (!win.chrome) {
      win.chrome = {
        runtime: {}
      }
    }
    
    // Configurar plugins
    Object.defineProperty(win.navigator, 'plugins', {
      get: () => [1, 2, 3, 4, 5]
    })
    
    // Configurar languages
    Object.defineProperty(win.navigator, 'languages', {
      get: () => ['pt-BR', 'pt', 'en-US', 'en']
    })
    
    cy.log('Detecção de automação removida')
  })
})

/**
 * Comando para visitar página com bypass completo do Cloudflare
 */
Cypress.Commands.add('visitWithCloudflareBypass', (url, options = {}) => {
  cy.log(`Visitando ${url} com bypass do Cloudflare...`)
  
  // Aplicar configurações de bypass
  cy.removeAutomationDetection()
  
  // Visitar a página
  cy.visit(url, {
    ...options,
    failOnStatusCode: false,
    timeout: 60000
  })
  
  // Aguardar Cloudflare se necessário
  cy.waitForCloudflare()
  
  cy.log('Página visitada com sucesso')
})

