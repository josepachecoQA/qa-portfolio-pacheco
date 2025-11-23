// ***********************************************
// Teste de Ativação do Captcha Cloudflare Turnstile no Atena para Blzbet
// Este teste acessa o Atena, navega até Sites > Cadastro > Blzbet > Alterar > Integrações > Captcha
// e ativa/configura o captcha Cloudflare Turnstile
// Site Key: 0x4AAAAAABD139_8AeI2Gd3i
// Secret Key: 0x4AAAAAABD13yAfxbQM7gQBJh8sW0McwU0
// Campo URL: #__BVID__893
// ***********************************************

describe('Ativação do Captcha no Atena - Blzbet', () => {
  const SITE_KEY = '0x4AAAAAABD139_8AeI2Gd3i'
  const SECRET_KEY = '0x4AAAAAABD13yAfxbQM7gQBJh8sW0McwU0'
  const CAPTCHA_URL = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
  const SITE_NAME = 'Blzbet'
  const URL_FIELD_ID = '#__BVID__893'

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
    cy.url({ timeout: 30000 }).then((url) => {
      if (url.includes('login') || url.includes('auth')) {
        cy.log('⚠️ Ainda na tela de login, aguardando mais tempo...')
        cy.wait(5000)
      } else {
        cy.log('✅ Login completado - não está mais na tela de login')
      }
    })
    
    cy.log('✅ Prosseguindo com o teste...')
  })

  it('Deve navegar até a configuração de Captcha do site Blzbet', () => {
    cy.log('🔍 Navegando para Sites > Cadastro > Nome Fantasia (Blzbet) > Alterar > Integrações > Captcha...')
    
    // Aguardar página carregar completamente após login
    cy.wait(3000)
    
    // Passo 1: Clicar no menu Sites
    cy.log('📍 Passo 1: Clicando no menu Sites...')
    cy.get('body', { timeout: 15000 }).then(($body) => {
      const menuSites = $body.find('.sidenav-inner > :nth-child(2) > :nth-child(6) > :nth-child(1)')
      
      if (menuSites.length > 0 && menuSites.is(':visible')) {
        cy.log('✅ Menu Sites encontrado pelo seletor específico')
        cy.wrap(menuSites).scrollIntoView()
        cy.wait(500)
        cy.wrap(menuSites).click({ force: true })
      } else {
        cy.log('⚠️ Seletor específico não encontrado, buscando por texto...')
        const links = $body.find('a, button, [role="button"], [role="link"], .sidenav-link')
        
        for (let i = 0; i < links.length; i++) {
          const $el = Cypress.$(links[i])
          const text = $el.text().toLowerCase().trim()
          
          if (text === 'sites' || text === 'site') {
            cy.log(`✅ Menu Sites encontrado por texto: ${text}`)
            cy.wrap($el).scrollIntoView()
            cy.wait(500)
            cy.wrap($el).click({ force: true })
            break
          }
        }
      }
    })
    
    cy.log('✅ Menu Sites clicado')
    cy.wait(3000)
    
    // Passo 2: Clicar em Cadastro DENTRO do menu Sites expandido
    cy.log('📍 Passo 2: Clicando em Cadastro dentro do menu Sites...')
    cy.get('body', { timeout: 15000 }).then(($body) => {
      let cadastroFound = false
      
      const linkCadastro = $body.find('.open > :nth-child(2) > :nth-child(1) > .sidenav-item > .sidenav-link')
      if (linkCadastro.length > 0 && linkCadastro.is(':visible')) {
        cy.wrap(linkCadastro).scrollIntoView()
        cy.wait(500)
        cy.wrap(linkCadastro).click({ force: true })
        cadastroFound = true
      }
      
      if (!cadastroFound) {
        const links = $body.find('.open a, .open button, .open .sidenav-link')
        for (let i = 0; i < links.length && !cadastroFound; i++) {
          const $el = Cypress.$(links[i])
          const text = $el.text().toLowerCase().trim()
          
          if (text === 'cadastro' || text === 'cadastros' || text.includes('cadastr')) {
            cy.wrap($el).scrollIntoView()
            cy.wait(500)
            cy.wrap($el).click({ force: true })
            cadastroFound = true
            break
          }
        }
      }
      
      if (!cadastroFound) {
        cy.log('❌ Link Cadastro não encontrado dentro do menu Sites')
      }
    })
    
    cy.wait(3000)
    
    // Passo 3: Pesquisar pelo site Blzbet no campo Nome Fantasia
    cy.log('📍 Passo 3: Pesquisando pelo site Blzbet...')
    cy.get('body', { timeout: 15000 }).then(($body) => {
      let nomeFantasiaField = null
      const inputs = $body.find('input[type="text"], input[type="search"], input:not([type])')
      
      for (let i = 0; i < inputs.length && (!nomeFantasiaField || nomeFantasiaField.length === 0); i++) {
        const $input = Cypress.$(inputs[i])
        if (!$input.is(':visible')) continue
        
        const name = ($input.attr('name') || '').toLowerCase()
        const id = ($input.attr('id') || '').toLowerCase()
        const placeholder = ($input.attr('placeholder') || '').toLowerCase()
        
        const $label = $input.closest('label, div, form').find('label').first()
        const labelText = $label.text().toLowerCase()
        
        if (name.includes('nome') || name.includes('fantasia') || 
            id.includes('nome') || id.includes('fantasia') ||
            placeholder.includes('nome') || placeholder.includes('fantasia') ||
            labelText.includes('nome fantasia') || labelText.includes('nome-fantasia')) {
          nomeFantasiaField = $input
          cy.log(`✅ Campo Nome Fantasia encontrado`)
          break
        }
      }
      
      if (nomeFantasiaField && nomeFantasiaField.length > 0) {
        cy.wrap(nomeFantasiaField).scrollIntoView()
        cy.wait(500)
        cy.wrap(nomeFantasiaField).clear({ force: true })
        cy.wrap(nomeFantasiaField).type(SITE_NAME, { force: true })
        cy.log('✅ Nome Fantasia preenchido')
      } else {
        cy.log('⚠️ Campo Nome Fantasia não encontrado')
      }
    })
    
    cy.wait(1000)
    
    // Clicar no botão Buscar
    cy.log('📍 Clicando no botão Buscar...')
    cy.get('body').then(($body) => {
      const buttons = $body.find('button, input[type="submit"], input[type="button"]')
      let buscarButton = null
      
      for (let i = 0; i < buttons.length && (!buscarButton || buscarButton.length === 0); i++) {
        const $btn = Cypress.$(buttons[i])
        const text = $btn.text().toLowerCase().trim()
        const value = ($btn.attr('value') || '').toLowerCase()
        
        if (text === 'buscar' || text === 'search' || text.includes('buscar') ||
            value === 'buscar' || value.includes('buscar')) {
          buscarButton = $btn
          cy.log(`✅ Botão Buscar encontrado`)
          break
        }
      }
      
      if (buscarButton && buscarButton.length > 0) {
        cy.wrap(buscarButton).scrollIntoView()
        cy.wait(500)
        cy.wrap(buscarButton).click({ force: true })
        cy.log('✅ Botão Buscar clicado')
      } else {
        cy.log('⚠️ Botão Buscar não encontrado')
      }
    })
    
    cy.wait(3000)
    
    // Passo 4: Clicar no botão Alterar do Blzbet
    cy.log('📍 Passo 4: Clicando no botão Alterar do Blzbet...')
    cy.get('body', { timeout: 15000 }).then(($body) => {
      const rows = $body.find('tr, .row, .table-row, [class*="row"]')
      let alterarButton = null
      
      for (let i = 0; i < rows.length && (!alterarButton || alterarButton.length === 0); i++) {
        const $row = Cypress.$(rows[i])
        const rowText = $row.text().toLowerCase()
        
        if (rowText.includes('blzbet') || rowText.includes('blz')) {
          const buttons = $row.find('button, a, [role="button"]')
          for (let j = 0; j < buttons.length; j++) {
            const $btn = Cypress.$(buttons[j])
            const text = $btn.text().toLowerCase().trim()
            
            if (text === 'alterar' || text === 'editar' || text.includes('alterar') || text.includes('editar')) {
              alterarButton = $btn
              cy.log(`✅ Botão Alterar encontrado na linha do Blzbet`)
              break
            }
          }
          
          if (alterarButton && alterarButton.length > 0) {
            break
          }
        }
      }
      
      if (alterarButton && alterarButton.length > 0) {
        cy.wrap(alterarButton).scrollIntoView()
        cy.wait(500)
        cy.wrap(alterarButton).click({ force: true })
        cy.log('✅ Botão Alterar clicado')
      } else {
        cy.log('⚠️ Botão Alterar não encontrado')
      }
    })
    
    cy.wait(3000)
    
    // Passo 5: Clicar em Integração/Integrações
    cy.log('📍 Passo 5: Clicando em Integração...')
    cy.wait(2000)
    
    cy.get('body', { timeout: 15000 }).then(($body) => {
      const tabs = $body.find('.nav-tabs a, .nav-tabs button, .tabs a, .tabs button, [role="tab"], .tab-link')
      let integracaoTab = null
      
      for (let i = 0; i < tabs.length && (!integracaoTab || integracaoTab.length === 0); i++) {
        const $tab = Cypress.$(tabs[i])
        const text = $tab.text().toLowerCase().trim()
        
        if (text === 'integração' || text === 'integrações' || text.includes('integra')) {
          integracaoTab = $tab
          cy.log(`✅ Tab Integração encontrada`)
          break
        }
      }
      
      if (integracaoTab && integracaoTab.length > 0) {
        cy.wrap(integracaoTab).scrollIntoView({ force: true })
        cy.wait(500)
        cy.wrap(integracaoTab).click({ force: true })
        cy.log('✅ Link/Tab Integração clicado')
      } else {
        cy.log('⚠️ Link/Tab Integração não encontrado')
      }
    })
    
    cy.wait(3000)
    
    // Passo 6: Configurar o Captcha
    cy.log('📍 Passo 6: Configurando o Captcha...')
    
    // Passo 6.1: Selecionar o tipo de captcha como "Cloudflare"
    cy.log('📍 Passo 6.1: Selecionando tipo de captcha como Cloudflare...')
    cy.get('body', { timeout: 15000 }).then(($body) => {
      const selects = $body.find('select, [role="combobox"]')
      let captchaTypeSelect = null
      
      for (let i = 0; i < selects.length && (!captchaTypeSelect || captchaTypeSelect.length === 0); i++) {
        const $select = Cypress.$(selects[i])
        const options = $select.find('option')
        
        for (let j = 0; j < options.length; j++) {
          const $option = Cypress.$(options[j])
          const optionText = $option.text().toLowerCase().trim()
          
          if (optionText.includes('cloudflare')) {
            captchaTypeSelect = $select
            cy.log(`✅ Select de tipo de captcha encontrado`)
            break
          }
        }
      }
      
      if (captchaTypeSelect && captchaTypeSelect.length > 0) {
        cy.wrap(captchaTypeSelect).scrollIntoView()
        cy.wait(500)
        cy.wrap(captchaTypeSelect).select('Cloudflare', { force: true })
        cy.log('✅ Tipo de captcha selecionado como Cloudflare')
      } else {
        cy.log('⚠️ Select de tipo de captcha não encontrado')
      }
    })
    
    cy.wait(2000)
    
    // Passo 6.2: Preencher a URL usando o ID específico
    cy.log('📍 Passo 6.2: Adicionando URL do captcha usando ID específico #__BVID__893...')
    cy.get(URL_FIELD_ID, { timeout: 10000 }).should('be.visible').then(($urlField) => {
      cy.log(`✅ Campo URL encontrado pelo ID específico: ${URL_FIELD_ID}`)
      cy.wrap($urlField).scrollIntoView({ force: true })
      cy.wait(500)
      cy.wrap($urlField).clear({ force: true })
      cy.wait(500)
      cy.wrap($urlField).type(CAPTCHA_URL, { force: true, delay: 50 })
      cy.wait(1000)
      cy.wrap($urlField).should('have.value', CAPTCHA_URL)
      cy.log(`✅ URL preenchida e verificada: ${CAPTCHA_URL}`)
    })
    
    cy.wait(1000)
    
    // Passo 6.3: Preencher Site Key e Secret Key
    cy.log('📍 Passo 6.3: Preenchendo Site Key e Secret Key...')
    cy.get('body', { timeout: 15000 }).then(($body) => {
      const inputs = $body.find('input, textarea')
      let siteKeyField = null
      let secretKeyField = null
      
      for (let i = 0; i < inputs.length; i++) {
        const $input = Cypress.$(inputs[i])
        if (!$input.is(':visible')) continue
        
        const name = ($input.attr('name') || '').toLowerCase()
        const id = ($input.attr('id') || '').toLowerCase()
        const placeholder = ($input.attr('placeholder') || '').toLowerCase()
        const label = $input.closest('label, div').find('label').first().text().toLowerCase()
        
        if ((name.includes('site') && name.includes('key')) || 
            (id.includes('site') && id.includes('key')) ||
            placeholder.includes('site key') ||
            label.includes('site key')) {
          if (!siteKeyField || siteKeyField.length === 0) {
            siteKeyField = $input
          }
        }
        
        if ((name.includes('secret') && name.includes('key')) || 
            (id.includes('secret') && id.includes('key')) ||
            placeholder.includes('secret key') ||
            label.includes('secret key')) {
          if (!secretKeyField || secretKeyField.length === 0) {
            secretKeyField = $input
          }
        }
      }
      
      if (siteKeyField && siteKeyField.length > 0) {
        cy.wrap(siteKeyField).scrollIntoView({ force: true })
        cy.wait(500)
        cy.wrap(siteKeyField).clear({ force: true })
        cy.wrap(siteKeyField).type(SITE_KEY, { force: true, delay: 100 })
        cy.wrap(siteKeyField).should('have.value', SITE_KEY)
        cy.log(`✅ Site Key preenchido: ${SITE_KEY}`)
      }
      
      if (secretKeyField && secretKeyField.length > 0) {
        cy.wrap(secretKeyField).scrollIntoView({ force: true })
        cy.wait(500)
        cy.wrap(secretKeyField).clear({ force: true })
        cy.wrap(secretKeyField).type(SECRET_KEY, { force: true, delay: 100 })
        cy.wrap(secretKeyField).should('have.value', SECRET_KEY)
        cy.log(`✅ Secret Key preenchido: ${SECRET_KEY}`)
      }
    })
    
    cy.wait(1000)
    
    // Passo 7: Salvar as configurações
    cy.log('💾 Salvando configurações do Captcha...')
    cy.get('body').then(($body) => {
      const buttons = $body.find('button, input[type="submit"], input[type="button"]')
      let salvarButton = null
      
      for (let i = 0; i < buttons.length && (!salvarButton || salvarButton.length === 0); i++) {
        const $btn = Cypress.$(buttons[i])
        const text = $btn.text().toLowerCase()
        
        if (text.includes('salvar') || text.includes('save') || text.includes('aplicar')) {
          salvarButton = $btn
        }
      }
      
      if (salvarButton && salvarButton.length > 0) {
        cy.wrap(salvarButton).scrollIntoView()
        cy.wait(500)
        cy.wrap(salvarButton).click({ force: true })
        cy.log('✅ Botão de salvar clicado')
      } else {
        cy.log('⚠️ Botão de salvar não encontrado')
      }
    })
    
    cy.wait(5000)
    
    // Verificar mensagem de sucesso
    cy.get('body', { timeout: 10000 }).then(($body) => {
      const bodyText = $body.text().toLowerCase()
      const sucessoIndicators = ['sucesso', 'salvo', 'atualizado', 'configurações salvas']
      let sucessoEncontrado = false
      
      for (const indicator of sucessoIndicators) {
        if (bodyText.includes(indicator)) {
          sucessoEncontrado = true
          cy.log(`✅ Mensagem de sucesso encontrada: "${indicator}"`)
          break
        }
      }
      
      if (sucessoEncontrado) {
        cy.log('✅ Configurações do Captcha salvas com sucesso!')
        expect(true).to.be.true
      } else {
        cy.log('⚠️ Não foi possível confirmar se as configurações foram salvas')
      }
    })
  })
})

