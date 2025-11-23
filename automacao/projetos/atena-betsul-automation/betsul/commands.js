// ***********************************************
// Este arquivo contém comandos personalizados do Cypress
// ***********************************************

/// <reference types="cypress" />

/**
 * Comando para aguardar elemento estar visível
 */
Cypress.Commands.add('waitForElement', (selector, timeout = 10000) => {
  cy.get(selector, { timeout }).should('be.visible')
})

/**
 * Comando para navegar para uma seção específica
 */
Cypress.Commands.add('navigateToSection', (sectionName) => {
  cy.contains(sectionName).click()
})

/**
 * Comando para verificar se o elemento existe sem falhar se não existir
 */
Cypress.Commands.add('elementExists', (selector) => {
  return cy.get('body').then(($body) => {
    return $body.find(selector).length > 0
  })
})

/**
 * Comando para fechar modais e overlays que podem aparecer
 * Este comando tenta fechar modais/overlays sem falhar se não encontrar elementos
 */
Cypress.Commands.add('closeModals', () => {
  // Tentar fechar usando ESC - usar window ao invés de body para evitar problemas de visibilidade
  cy.window().trigger('keydown', { key: 'Escape', code: 'Escape', keyCode: 27 })
  cy.wait(500)
  
  // Tentar fechar screen-block ou overlays
  cy.get('body').then(($body) => {
    // Verificar se há screen-block
    const screenBlock = $body.find('.screen-block, [class*="screen-block"]')
    if (screenBlock.length > 0) {
      cy.window().trigger('keydown', { key: 'Escape', code: 'Escape', keyCode: 27 })
      cy.wait(500)
    }

    // Tentar fechar prompts de notificação - simplificar seletores
    const webPushPrompt = $body.find('#webpush-custom-prompt-text, [id*="webpush"], [class*="webpush"]')
    if (webPushPrompt.length > 0) {
      // Tentar encontrar botão de fechar - simplificar busca
      let closeButton = $body.find('[class*="close"]').first()
      if (closeButton.length === 0) {
        closeButton = $body.find('[class*="dismiss"]').first()
      }
      if (closeButton.length === 0) {
        // Tentar encontrar botão dentro do webpush
        closeButton = webPushPrompt.find('button').first()
      }
      
      if (closeButton.length > 0) {
        // Tentar clicar no botão de fechar - usar force para não falhar se coberto
        cy.wrap(closeButton).click({ force: true })
        cy.wait(500)
      } else {
        // Se não encontrar botão, tentar ESC novamente
        cy.window().trigger('keydown', { key: 'Escape', code: 'Escape', keyCode: 27 })
        cy.wait(500)
      }
    }
  })
})

/**
 * Comando para clicar com tratamento de elementos cobertos
 */
Cypress.Commands.add('clickSafe', (selector, options = {}) => {
  cy.get(selector).scrollIntoView()
  cy.wait(500)
  cy.closeModals()
  cy.get(selector).click({ force: true, ...options })
})

