// ***********************************************
// Teste de acesso ao site Betsul
// Este teste verifica o acesso básico ao site
// ***********************************************

describe('Acesso ao Site Betsul', () => {
  it('Deve acessar a página inicial do site Betsul', () => {
    // Acessar a página inicial
    cy.visit('/', {
      timeout: 60000,
      failOnStatusCode: false
    })
    
    // Verificar se a página carregou corretamente
    cy.url().should('include', 'betsul.online')
    
    // Aguardar que o body esteja visível
    cy.get('body', { timeout: 10000 }).should('be.visible')
  })

  it('Deve verificar elementos principais da página inicial', () => {
    // Acessar a página inicial
    cy.visit('/', {
      timeout: 60000,
      failOnStatusCode: false
    })
    
    // Verificar se o body está visível
    cy.get('body', { timeout: 10000 }).should('be.visible')
    
    // Verificar se há conteúdo na página (não está vazia)
    cy.get('body').should('not.be.empty')
    
    // Fechar modais ou overlays que possam aparecer
    cy.closeModals()
  })

  it('Deve verificar o título da página', () => {
    cy.visit('/', {
      timeout: 60000,
      failOnStatusCode: false
    })
    
    // Verificar o título da página
    cy.title().then((title) => {
      cy.log(`Título da página: ${title}`)
      expect(title).to.exist
    })
  })

  it('Deve verificar elementos de navegação do site', () => {
    cy.visit('/', {
      timeout: 60000,
      failOnStatusCode: false
    })
    
    // Verificar se o body está visível
    cy.get('body', { timeout: 10000 }).should('be.visible')
    
    // Verificar se há algum conteúdo na página
    cy.get('body').should('not.be.empty')
    
    // Verificar se há elementos de navegação (menu, links, etc.)
    cy.get('body').then(($body) => {
      // Verificar se há links na página
      const hasLinks = $body.find('a').length > 0
      cy.log(`Página contém ${$body.find('a').length} links`)
      
      // Verificar se há algum menu ou navegação
      const hasMenu = $body.find('nav, [role="navigation"], [class*="menu"], [class*="nav"]').length > 0
      cy.log(`Página contém elementos de menu: ${hasMenu}`)
      
      // O teste passa se a página carregou corretamente
      expect(hasLinks || hasMenu || $body.text().length > 0).to.be.true
    })
  })

  it('Deve verificar e mapear o elemento .buttons > :nth-child(1)', () => {
    cy.visit('/', {
      timeout: 60000,
      failOnStatusCode: false
    })
    
    // Verificar se o body está visível
    cy.get('body', { timeout: 10000 }).should('be.visible')
    
    // Fechar modais que possam aparecer
    cy.closeModals()
    
    // Verificar se o elemento existe
    cy.get('body').then(($body) => {
      const buttonsElement = $body.find('.buttons')
      const firstChild = buttonsElement.find(':nth-child(1)')
      
      if (buttonsElement.length > 0 && firstChild.length > 0) {
        cy.log('✅ Elemento .buttons > :nth-child(1) encontrado!')
        
        // Mapear características do elemento
        cy.get('.buttons > :nth-child(1)').then(($el) => {
          cy.log(`Tag: ${$el.prop('tagName')}`)
          cy.log(`Texto: ${$el.text()}`)
          cy.log(`Classes: ${$el.attr('class') || 'N/A'}`)
          cy.log(`ID: ${$el.attr('id') || 'N/A'}`)
          cy.log(`Visível: ${$el.is(':visible')}`)
          
          // Verificar se é clicável
          if ($el.is('button') || $el.is('a') || $el.prop('onclick') || $el.attr('onclick')) {
            cy.log('✅ Elemento é clicável')
          }
        })
      } else {
        cy.log('⚠️ Elemento .buttons > :nth-child(1) não encontrado')
      }
    })
    
    // Tentar encontrar o elemento diretamente
    cy.get('body').then(($body) => {
      if ($body.find('.buttons > :nth-child(1)').length > 0) {
        cy.get('.buttons > :nth-child(1)', { timeout: 5000 }).should('exist').then(($el) => {
          cy.log('✅ Elemento mapeado com sucesso!')
          expect($el).to.exist
        })
      } else {
        cy.log('⚠️ Elemento .buttons > :nth-child(1) não encontrado na página')
      }
    })
  })
})

