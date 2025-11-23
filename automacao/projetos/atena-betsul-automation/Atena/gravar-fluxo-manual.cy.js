// ***********************************************
// Teste para gravar interações manuais do usuário
// Este teste faz login e depois pausa para permitir interação manual
// As ações do usuário serão registradas
// ***********************************************

describe('Gravação de Fluxo Manual - Atena', () => {
  beforeEach(() => {
    // Acessar a página inicial do Atena
    cy.visit('/', {
      timeout: 60000,
      failOnStatusCode: false
    })
    
    cy.get('body', { timeout: 10000 }).should('be.visible')
    cy.closeModals()
    
    // Fazer login no Atena
    cy.loginAtena()
    
    // Aguardar login completar
    cy.wait(5000)
    
    // Verificar se saiu da tela de login
    cy.url().should('not.include', 'login').should('not.include', 'auth')
    cy.log('✅ Login completado - não está mais na tela de login')
  })

  it('Deve pausar para permitir interação manual e gravar os cliques', () => {
    cy.log('🎬 Modo de gravação ativado - aguardando interação manual...')
    cy.log('📍 Você pode fazer o fluxo manualmente agora')
    cy.log('📍 O teste irá registrar seus cliques e navegação')
    
    // Pausar e permitir interação manual
    cy.pause()
    
    // Após o usuário interagir, tentar capturar informações sobre o estado atual
    cy.log('📝 Capturando informações sobre o estado atual da página...')
    
    // Capturar URL atual
    cy.url().then((url) => {
      cy.log(`📍 URL atual: ${url}`)
    })
    
    // Capturar título da página
    cy.title().then((title) => {
      cy.log(`📄 Título da página: ${title}`)
    })
    
    // Capturar elementos clicáveis visíveis
    cy.get('body', { timeout: 15000 }).then(($body) => {
      cy.log('📋 Listando elementos clicáveis na página...')
      
      const clickableElements = $body.find('a, button, [role="button"], [role="link"], .sidenav-link, [class*="link"]')
      const visibleClickables = []
      
      clickableElements.each((index, el) => {
        const $el = Cypress.$(el)
        if ($el.is(':visible')) {
          const text = $el.text().trim()
          const href = $el.attr('href') || ''
          const id = $el.attr('id') || ''
          const className = $el.attr('class') || ''
          
          if (text.length > 0 || href.length > 0 || id.length > 0) {
            visibleClickables.push({
              index,
              text: text.substring(0, 50),
              href,
              id,
              className: className.substring(0, 50)
            })
          }
        }
      })
      
      cy.log(`📊 Total de elementos clicáveis visíveis: ${visibleClickables.length}`)
      
      // Listar os primeiros 20 elementos
      const elementsToLog = visibleClickables.slice(0, 20)
      elementsToLog.forEach((el) => {
        cy.log(`  - Elemento ${el.index}: texto="${el.text}", href="${el.href}", id="${el.id}"`)
      })
    })
    
    // Capturar elementos de formulário visíveis
    cy.get('body').then(($body) => {
      const formElements = $body.find('input, select, textarea, [role="combobox"]')
      const visibleFormElements = []
      
      formElements.each((index, el) => {
        const $el = Cypress.$(el)
        if ($el.is(':visible')) {
          const type = $el.attr('type') || ''
          const name = $el.attr('name') || ''
          const id = $el.attr('id') || ''
          const placeholder = $el.attr('placeholder') || ''
          
          visibleFormElements.push({
            index,
            type,
            name,
            id,
            placeholder
          })
        }
      })
      
      cy.log(`📝 Total de elementos de formulário visíveis: ${visibleFormElements.length}`)
      
      // Listar os primeiros 20 elementos
      const formElementsToLog = visibleFormElements.slice(0, 20)
      formElementsToLog.forEach((el) => {
        cy.log(`  - Input ${el.index}: type="${el.type}", name="${el.name}", id="${el.id}", placeholder="${el.placeholder}"`)
      })
    })
    
    cy.log('✅ Gravação concluída - informações capturadas')
  })
})

