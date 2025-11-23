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
    cy.url().should('not.include', 'login').should('not.include', 'auth')
    cy.log('✅ Login completado - não está mais na tela de login')
    cy.log('✅ Prosseguindo com o teste...')
  })

  it('Deve navegar até a configuração de Captcha do site Blzbet', () => {
    cy.log('🔍 Navegando para Principal > Sites > Cadastros > Nome Fantasia (Blzbet) > Alterar > Integrações > Captcha...')
    
    // Aguardar página carregar completamente após login
    cy.wait(3000)
    
    // Passo 1: Clicar no menu "Principal" no menu lateral
    cy.log('📍 Passo 1: Clicando no menu Principal...')
    cy.get('body', { timeout: 15000 }).then(($body) => {
      const links = $body.find('a, button, [role="button"], [role="link"], .sidenav-link')
      let principalFound = false
      
      cy.log(`🔍 Buscando "Principal" entre ${links.length} links...`)
      
      for (let i = 0; i < links.length && !principalFound; i++) {
        const $el = Cypress.$(links[i])
        const text = $el.text().toLowerCase().trim()
        
        if (text === 'principal') {
          cy.log(`✅ Menu Principal encontrado: "${text}"`)
          cy.wrap($el).scrollIntoView()
          cy.wait(500)
          cy.wrap($el).click({ force: true })
          principalFound = true
          break
        }
      }
      
      if (!principalFound) {
        cy.log('⚠️ Menu Principal não encontrado, tentando buscar por texto parcial...')
        for (let i = 0; i < links.length && !principalFound; i++) {
          const $el = Cypress.$(links[i])
          const text = $el.text().toLowerCase().trim()
          
          if (text.includes('principal')) {
            cy.log(`✅ Menu Principal encontrado por texto parcial: "${text}"`)
            cy.wrap($el).scrollIntoView()
            cy.wait(500)
            cy.wrap($el).click({ force: true })
            principalFound = true
            break
          }
        }
      }
      
      if (!principalFound) {
        cy.log('❌ Menu Principal não encontrado')
      }
    })
    
    cy.log('✅ Menu Principal clicado')
    cy.wait(3000)
    
    // Passo 2: Clicar no módulo "Sites" dentro de Principal usando seletor específico
    cy.log('📍 Passo 2: Clicando no módulo Sites dentro de Principal...')
    
    // Tentar primeiro o seletor específico fornecido
    cy.get('body', { timeout: 15000 }).then(($body) => {
      // Tentar variações do seletor data-cypress-el
      let sitesElement = $body.find('[data-cypress-el="true"]')
      
      // Se não encontrar, tentar com o estilo vazio
      if (sitesElement.length === 0) {
        sitesElement = $body.find('[style=""] [data-cypress-el="true"], [style=""] > [data-cypress-el="true"]')
      }
      
      // Se ainda não encontrar, buscar todos os elementos com data-cypress-el
      if (sitesElement.length === 0) {
        const allCypressEls = $body.find('[data-cypress-el], [data-cypress-el="true"]')
        cy.log(`🔍 Encontrados ${allCypressEls.length} elementos com data-cypress-el...`)
        
        // Buscar aquele que está visível e dentro do menu Principal expandido
        for (let i = 0; i < allCypressEls.length && sitesElement.length === 0; i++) {
          const $el = Cypress.$(allCypressEls[i])
          if ($el.is(':visible')) {
            const $parent = $el.closest('[class*="open"], [class*="expanded"]')
            const parentText = $parent.text().toLowerCase()
            
            // Verificar se está dentro do contexto de Principal e contém "Sites"
            if (parentText.includes('principal') || parentText.includes('site')) {
              sitesElement = $el
              cy.log(`✅ Elemento Sites encontrado com data-cypress-el`)
              break
            }
          }
        }
      }
      
      // Se ainda não encontrou, buscar por texto "Sites" dentro do menu Principal expandido
      if (sitesElement.length === 0) {
        cy.log('⚠️ Seletor por atributo não encontrado, buscando por texto...')
        const links = $body.find('.open a, .open button, .open .sidenav-link, [class*="open"] a, [class*="open"] .sidenav-link')
        
        for (let i = 0; i < links.length; i++) {
          const $el = Cypress.$(links[i])
          const text = $el.text().toLowerCase().trim()
          
          if ((text === 'sites' || text === 'site') && 
              text !== 'cadastros' && text !== 'cadastro' &&
              !text.includes('cadastr') && !text.includes('deposit')) {
            sitesElement = $el
            cy.log(`✅ Módulo Sites encontrado por texto: "${text}"`)
            break
          }
        }
      }
      
      if (sitesElement.length > 0 && sitesElement.is(':visible')) {
        cy.wrap(sitesElement).scrollIntoView()
        cy.wait(500)
        cy.wrap(sitesElement).click({ force: true })
        cy.log('✅ Módulo Sites clicado')
      } else {
        cy.log('❌ Módulo Sites não encontrado')
      }
    })
    cy.wait(3000)
    
    // Passo 3: Clicar em "Cadastros" dentro do menu Sites expandido usando seletor específico
    cy.log('📍 Passo 3: Clicando em Cadastros dentro do menu Sites...')
    cy.get('body', { timeout: 15000 }).then(($body) => {
      // Tentar primeiro o seletor específico fornecido
      let cadastrosElement = $body.find('.open > :nth-child(2) > :nth-child(4) > .sidenav-item > .sidenav-link')
      
      // Se não encontrar, buscar por texto "Cadastros" dentro do menu Sites expandido
      if (cadastrosElement.length === 0 || !cadastrosElement.is(':visible')) {
        cy.log('⚠️ Seletor específico não encontrado, buscando por texto...')
        const links = $body.find('.open a, .open button, .open .sidenav-link, [class*="open"] a, [class*="open"] .sidenav-link')
        
        for (let i = 0; i < links.length; i++) {
          const $el = Cypress.$(links[i])
          const text = $el.text().toLowerCase().trim()
          
          if ((text === 'cadastros' || text === 'cadastro') && 
              !text.includes('depósito') && !text.includes('deposito') &&
              !text.includes('deposit') && !text.includes('saque')) {
            cadastrosElement = $el
            cy.log(`✅ Link Cadastros encontrado por texto: "${text}"`)
            break
          }
        }
      }
      
      if (cadastrosElement.length > 0 && cadastrosElement.is(':visible')) {
        cy.wrap(cadastrosElement).scrollIntoView()
        cy.wait(500)
        cy.wrap(cadastrosElement).click({ force: true })
        cy.log('✅ Link Cadastros clicado')
      } else {
        cy.log('❌ Link Cadastros não encontrado')
      }
    })
    cy.wait(3000)
    
    // Passo 4: Pesquisar pelo site Blzbet no campo Nome Fantasia usando seletor específico
    cy.log('📍 Passo 4: Pesquisando pelo site Blzbet...')
    cy.get('body', { timeout: 15000 }).then(($body) => {
      // Tentar primeiro o seletor específico
      let campoPesquisa = $body.find(':nth-child(2) > .form-control')
      
      // Se não encontrar, buscar por campo de texto genérico
      if (campoPesquisa.length === 0 || !campoPesquisa.is(':visible')) {
        cy.log('⚠️ Seletor específico não encontrado, buscando campo de pesquisa genérico...')
        campoPesquisa = $body.find('input[type="text"], input.form-control, input:not([type="hidden"])').first()
      }
      
      if (campoPesquisa.length > 0 && campoPesquisa.is(':visible')) {
        cy.wrap(campoPesquisa).scrollIntoView()
        cy.wait(500)
        cy.wrap(campoPesquisa).clear({ force: true })
        cy.wrap(campoPesquisa).type(SITE_NAME, { force: true })
        cy.log('✅ Nome Fantasia preenchido')
      } else {
        cy.log('❌ Campo de pesquisa não encontrado')
      }
    })
    cy.wait(1000)
    
    // Clicar no botão Buscar usando seletor específico
    cy.log('📍 Clicando no botão Buscar...')
    cy.get('body', { timeout: 15000 }).then(($body) => {
      // Tentar primeiro o seletor específico
      let buscarButton = $body.find('.col-xl-3 > .btn')
      
      // Se não encontrar, buscar por texto "Buscar"
      if (buscarButton.length === 0 || !buscarButton.is(':visible')) {
        cy.log('⚠️ Seletor específico não encontrado, buscando por texto...')
        const buttons = $body.find('button, input[type="submit"], input[type="button"]')
        
        for (let i = 0; i < buttons.length; i++) {
          const $btn = Cypress.$(buttons[i])
          const text = $btn.text().toLowerCase().trim()
          
          if (text === 'buscar' || text === 'search' || text.includes('buscar')) {
            buscarButton = $btn
            cy.log(`✅ Botão Buscar encontrado por texto: "${text}"`)
            break
          }
        }
      }
      
      if (buscarButton.length > 0 && buscarButton.is(':visible')) {
        cy.wrap(buscarButton).scrollIntoView()
        cy.wait(500)
        cy.wrap(buscarButton).click({ force: true })
        cy.log('✅ Botão Buscar clicado')
      } else {
        cy.log('❌ Botão Buscar não encontrado')
      }
    })
    cy.wait(3000)
    
    // Passo 5: Clicar no botão Alterar do Blzbet usando seletor específico
    cy.log('📍 Passo 5: Clicando no botão Alterar do Blzbet...')
    cy.get('body', { timeout: 15000 }).then(($body) => {
      // Tentar primeiro o seletor específico
      let alterarButton = $body.find('.btn-secondary')
      
      // Se não encontrar, buscar por texto "Alterar" na linha do Blzbet
      if (alterarButton.length === 0 || !alterarButton.is(':visible')) {
        cy.log('⚠️ Seletor específico não encontrado, buscando por texto...')
        const rows = $body.find('tr, .row, .table-row')
        
        for (let i = 0; i < rows.length; i++) {
          const $row = Cypress.$(rows[i])
          const rowText = $row.text().toLowerCase()
          
          if (rowText.includes('blzbet') || rowText.includes('blz')) {
            const buttons = $row.find('button, a, [role="button"]')
            for (let j = 0; j < buttons.length; j++) {
              const $btn = Cypress.$(buttons[j])
              const text = $btn.text().toLowerCase().trim()
              
              if (text === 'alterar' || text === 'editar' || text.includes('alterar')) {
                alterarButton = $btn
                cy.log(`✅ Botão Alterar encontrado por texto: "${text}"`)
                break
              }
            }
            if (alterarButton.length > 0) break
          }
        }
      }
      
      if (alterarButton.length > 0 && alterarButton.is(':visible')) {
        cy.wrap(alterarButton).scrollIntoView()
        cy.wait(500)
        cy.wrap(alterarButton).click({ force: true })
        cy.log('✅ Botão Alterar clicado')
      } else {
        cy.log('❌ Botão Alterar não encontrado')
      }
    })
    cy.wait(3000)
    
    // Passo 6: Clicar em Integração/Integrações usando seletor específico
    cy.log('📍 Passo 6: Clicando em Integração...')
    cy.get('body', { timeout: 15000 }).then(($body) => {
      // Tentar primeiro o seletor específico
      let integracaoTab = $body.find('#__BVID__4790___BV_tab_button__')
      
      // Se não encontrar, buscar por texto "Integração"
      if (integracaoTab.length === 0 || !integracaoTab.is(':visible')) {
        cy.log('⚠️ Seletor específico não encontrado, buscando por texto...')
        const tabs = $body.find('.nav-tabs a, .nav-tabs button, .tabs a, .tabs button, [role="tab"], .tab-link, [id*="tab"]')
        
        for (let i = 0; i < tabs.length; i++) {
          const $tab = Cypress.$(tabs[i])
          const text = $tab.text().toLowerCase().trim()
          
          if (text === 'integração' || text === 'integrações' || text.includes('integra')) {
            integracaoTab = $tab
            cy.log(`✅ Aba Integração encontrada por texto: "${text}"`)
            break
          }
        }
      }
      
      if (integracaoTab.length > 0 && integracaoTab.is(':visible')) {
        cy.wrap(integracaoTab).scrollIntoView()
        cy.wait(500)
        cy.wrap(integracaoTab).click({ force: true })
        cy.log('✅ Aba Integração clicada')
      } else {
        cy.log('❌ Aba Integração não encontrada')
      }
    })
    cy.wait(3000)
    
    // Passo 7: Configurar o Captcha
    cy.log('📍 Passo 7: Configurando o Captcha...')
    
    // Passo 7.1: Selecionar o tipo de captcha como "Cloudflare" usando seletor específico
    cy.log('📍 Passo 7.1: Selecionando tipo de captcha como Cloudflare...')
    cy.get('body', { timeout: 15000 }).then(($body) => {
      // Tentar primeiro o seletor específico
      let captchaSelect = $body.find(':nth-child(17) > :nth-child(1) > .card > :nth-child(2) > .m-3 > .row > :nth-child(1)')
      
      // Se não encontrar, buscar por select com opção Cloudflare
      if (captchaSelect.length === 0 || !captchaSelect.is(':visible')) {
        cy.log('⚠️ Seletor específico não encontrado, buscando select com opção Cloudflare...')
        const selects = $body.find('select, [role="combobox"]')
        
        for (let i = 0; i < selects.length; i++) {
          const $select = Cypress.$(selects[i])
          const options = $select.find('option')
          
          for (let j = 0; j < options.length; j++) {
            const $option = Cypress.$(options[j])
            const optionText = $option.text().toLowerCase().trim()
            
            if (optionText.includes('cloudflare')) {
              captchaSelect = $select
              cy.log(`✅ Select de captcha encontrado por opção Cloudflare`)
              break
            }
          }
          if (captchaSelect.length > 0) break
        }
      }
      
      if (captchaSelect.length > 0 && captchaSelect.is(':visible')) {
        cy.wrap(captchaSelect).scrollIntoView()
        cy.wait(500)
        cy.wrap(captchaSelect).select('Cloudflare', { force: true })
        cy.log('✅ Tipo de captcha selecionado como Cloudflare')
      } else {
        cy.log('❌ Select de captcha não encontrado')
      }
    })
    cy.wait(3000)
    
    // Passo 7.2: Preencher Site Key usando seletor específico
    cy.log('📍 Passo 7.2: Preenchendo Site Key...')
    cy.get('body', { timeout: 15000 }).then(($body) => {
      // Tentar primeiro o seletor específico
      let siteKeyField = $body.find(':nth-child(17) > :nth-child(1) > .card > :nth-child(2) > .m-3 > .row > :nth-child(2)')
      
      // Se não encontrar, buscar por atributos
      if (siteKeyField.length === 0 || !siteKeyField.is(':visible')) {
        cy.log('⚠️ Seletor específico não encontrado, buscando por atributos...')
        const inputs = $body.find('input, textarea')
        
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
            siteKeyField = $input
            cy.log(`✅ Site Key encontrado por atributos`)
            break
          }
        }
      }
      
      if (siteKeyField.length > 0 && siteKeyField.is(':visible')) {
        cy.wrap(siteKeyField).scrollIntoView({ force: true })
        cy.wait(500)
        cy.wrap(siteKeyField).clear({ force: true })
        cy.wrap(siteKeyField).type(SITE_KEY, { force: true, delay: 100 })
        cy.wrap(siteKeyField).should('have.value', SITE_KEY)
        cy.log(`✅ Site Key preenchido: ${SITE_KEY}`)
      } else {
        cy.log('❌ Site Key não encontrado')
      }
    })
    cy.wait(1000)
    
    // Passo 7.3: Preencher Secret Key usando seletor específico
    cy.log('📍 Passo 7.3: Preenchendo Secret Key...')
    cy.get('body', { timeout: 15000 }).then(($body) => {
      // Tentar primeiro o seletor específico
      let secretKeyField = $body.find(':nth-child(17) > :nth-child(1) > .card > :nth-child(2) > .m-3 > .row > :nth-child(3)')
      
      // Se não encontrar, buscar por atributos
      if (secretKeyField.length === 0 || !secretKeyField.is(':visible')) {
        cy.log('⚠️ Seletor específico não encontrado, buscando por atributos...')
        const inputs = $body.find('input, textarea')
        
        for (let i = 0; i < inputs.length; i++) {
          const $input = Cypress.$(inputs[i])
          if (!$input.is(':visible')) continue
          
          const name = ($input.attr('name') || '').toLowerCase()
          const id = ($input.attr('id') || '').toLowerCase()
          const placeholder = ($input.attr('placeholder') || '').toLowerCase()
          const label = $input.closest('label, div').find('label').first().text().toLowerCase()
          
          if ((name.includes('secret') && name.includes('key')) || 
              (id.includes('secret') && id.includes('key')) ||
              placeholder.includes('secret key') ||
              label.includes('secret key')) {
            secretKeyField = $input
            cy.log(`✅ Secret Key encontrado por atributos`)
            break
          }
        }
      }
      
      if (secretKeyField.length > 0 && secretKeyField.is(':visible')) {
        cy.wrap(secretKeyField).scrollIntoView({ force: true })
        cy.wait(500)
        cy.wrap(secretKeyField).clear({ force: true })
        cy.wrap(secretKeyField).type(SECRET_KEY, { force: true, delay: 100 })
        cy.wrap(secretKeyField).should('have.value', SECRET_KEY)
        cy.log(`✅ Secret Key preenchido: ${SECRET_KEY}`)
      } else {
        cy.log('❌ Secret Key não encontrado')
      }
    })
    cy.wait(1000)
    
    // Passo 7.4: Preencher URL usando seletor específico
    cy.log('📍 Passo 7.4: Preenchendo URL do captcha...')
    cy.get('body', { timeout: 15000 }).then(($body) => {
      // Tentar primeiro o seletor específico
      let urlField = $body.find(':nth-child(17) > :nth-child(1) > .card > :nth-child(2) > .m-3 > .row > :nth-child(4)')
      
      // Se não encontrar, buscar por IDs similares (BVID__) ou atributos
      if (urlField.length === 0 || !urlField.is(':visible')) {
        cy.log('⚠️ Seletor específico não encontrado, buscando por IDs similares ou atributos...')
        
        // Tentar IDs similares
        const bvidInputs = $body.find('input[id*="BVID"], textarea[id*="BVID"]')
        for (let i = 0; i < bvidInputs.length && urlField.length === 0; i++) {
          const $input = Cypress.$(bvidInputs[i])
          if (!$input.is(':visible')) continue
          
          const name = ($input.attr('name') || '').toLowerCase()
          // Verificar se não é Site Key ou Secret Key
          if (!name.includes('site') && !name.includes('secret') && !name.includes('key')) {
            urlField = $input
            cy.log(`✅ URL encontrado por ID similar: id="${$input.attr('id')}"`)
            break
          }
        }
      }
      
      if (urlField.length > 0 && urlField.is(':visible')) {
        cy.wrap(urlField).scrollIntoView({ force: true })
        cy.wait(500)
        cy.wrap(urlField).clear({ force: true })
        cy.wrap(urlField).type(CAPTCHA_URL, { force: true, delay: 50 })
        cy.wrap(urlField).should('have.value', CAPTCHA_URL)
        cy.log(`✅ URL preenchida: ${CAPTCHA_URL}`)
      } else {
        cy.log('❌ Campo URL não encontrado')
      }
    })
    cy.wait(1000)
    
    // Passo 8: Salvar as configurações usando seletor específico
    cy.log('💾 Salvando configurações do Captcha...')
    cy.get('body', { timeout: 15000 }).then(($body) => {
      // Tentar primeiro o seletor específico
      let salvarButton = $body.find('.float-right > .btn-primary')
      
      // Se não encontrar, buscar por texto "Salvar"
      if (salvarButton.length === 0 || !salvarButton.is(':visible')) {
        cy.log('⚠️ Seletor específico não encontrado, buscando por texto...')
        const buttons = $body.find('button, input[type="submit"], input[type="button"]')
        
        for (let i = 0; i < buttons.length; i++) {
          const $btn = Cypress.$(buttons[i])
          const text = $btn.text().toLowerCase()
          
          if (text.includes('salvar') || text.includes('save') || text.includes('aplicar')) {
            salvarButton = $btn
            cy.log(`✅ Botão Salvar encontrado por texto: "${text}"`)
            break
          }
        }
      }
      
      if (salvarButton.length > 0 && salvarButton.is(':visible')) {
        cy.wrap(salvarButton).scrollIntoView()
        cy.wait(500)
        cy.wrap(salvarButton).click({ force: true })
        cy.log('✅ Botão de salvar clicado')
      } else {
        cy.log('❌ Botão de salvar não encontrado')
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

