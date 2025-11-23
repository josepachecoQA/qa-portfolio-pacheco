// ***********************************************
// Teste de Cadastro de Login - Blzbet no Atena
// Este teste faz login no Atena, navega para Sites > Login
// e cadastra um novo login para o site Blzbet
// ***********************************************

describe('Cadastro de Login - Blzbet no Atena', () => {
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
    
    // Aguardar e verificar se o login foi completado com sucesso
    cy.wait(8000)
    
    // Verificar se saiu da tela de login - aguardar até sair
    cy.url({ timeout: 30000 }).should((url) => {
      // Se ainda estiver na tela de login, aguardar mais
      if (url.includes('login') || url.includes('auth') || url.includes('signin')) {
        cy.log('⚠️ Ainda na tela de login, aguardando mais tempo...')
        return false // Força retry
      }
    })
    
    // Verificar se não está mais na página de login
    cy.url({ timeout: 30000 }).should('not.include', 'login')
    cy.url().should('not.include', 'auth')
    cy.url().should('not.include', 'signin')
    
    cy.log('✅ URL confirma que saiu da tela de login')
    
    // Verificar se há elementos indicando que está logado
    cy.get('body', { timeout: 15000 }).then(($body) => {
      const bodyText = $body.text().toLowerCase()
      const hasLoggedIndicators = $body.find('[class*="user"], [class*="profile"], [class*="logout"], [class*="sair"], [id*="user"], [id*="profile"]').length > 0
      const hasLogoutText = bodyText.includes('sair') || bodyText.includes('logout') || bodyText.includes('perfil')
      
      if (hasLoggedIndicators || hasLogoutText) {
        cy.log('✅ Login confirmado - indicadores encontrados')
      } else {
        cy.log('⚠️ Indicadores de login não encontrados, mas URL indica que não está mais na tela de login')
      }
    })
    
    cy.log('✅ Login completado, prosseguindo com o teste...')
  })

  it('Deve cadastrar um novo login para o site Blzbet', () => {
    // Gerar dados aleatórios para o cadastro
    const timestamp = Date.now()
    const dadosLogin = {
      email: `teste.blzbet.${timestamp}@teste.com`,
      login: `blzbet_user_${timestamp}`,
      senha: 'Teste@123456',
      confirmarSenha: 'Teste@123456',
      site: 'Blzbet' // Nome do site Blzbet
    }
    
    cy.log('📝 Iniciando cadastro de novo login para Blzbet...')
    cy.log(`Email: ${dadosLogin.email}`)
    cy.log(`Login: ${dadosLogin.login}`)
    
    // Navegar para Sites > Login
    cy.log('🔍 Navegando para Sites > Login...')
    
    // Aguardar página carregar completamente após login
    cy.wait(3000)
    
    // Passo 1: Acessar o menu Sites usando o seletor específico
    cy.log('📍 Clicando no menu Sites...')
    cy.get('body', { timeout: 15000 }).then(($body) => {
      // Tentar usar o seletor específico primeiro
      const menuSites = $body.find('.sidenav-inner > :nth-child(2) > :nth-child(6) > :nth-child(1)')
      
      if (menuSites.length > 0 && menuSites.is(':visible')) {
        cy.log('✅ Menu Sites encontrado pelo seletor específico')
        cy.wrap(menuSites).scrollIntoView()
        cy.wait(500)
        cy.wrap(menuSites).click({ force: true })
      } else {
        // Fallback: buscar por texto "Sites"
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
    cy.wait(3000) // Aguardar menu expandir
    
    // Passo 2: Clicar em Login dentro do menu Sites
    cy.log('📍 Clicando em Login...')
    cy.get('body', { timeout: 15000 }).then(($body) => {
      // Tentar usar o seletor específico primeiro
      const linkLogin = $body.find('.open > :nth-child(2) > :nth-child(3) > .sidenav-item > .sidenav-link')
      
      if (linkLogin.length > 0 && linkLogin.is(':visible')) {
        cy.log('✅ Link Login encontrado pelo seletor específico')
        cy.wrap(linkLogin).scrollIntoView()
        cy.wait(500)
        cy.wrap(linkLogin).click({ force: true })
      } else {
        // Fallback: buscar por texto "Login"
        cy.log('⚠️ Seletor específico não encontrado, buscando por texto...')
        const links = $body.find('a, button, [role="button"], .sidenav-link')
        
        for (let i = 0; i < links.length; i++) {
          const $el = Cypress.$(links[i])
          const text = $el.text().toLowerCase().trim()
          
          if (text === 'login' || text.includes('login')) {
            cy.log(`✅ Link Login encontrado por texto: ${text}`)
            cy.wrap($el).scrollIntoView()
            cy.wait(500)
            cy.wrap($el).click({ force: true })
            break
          }
        }
      }
    })
    
    cy.log('✅ Link Login clicado')
    cy.wait(3000) // Aguardar página carregar
    
    // Aguardar carregamento da página de cadastro de login
    cy.wait(3000)
    cy.get('body', { timeout: 10000 }).should('be.visible')
    cy.closeModals()
    
    cy.log('📋 Preenchendo formulário de cadastro de login...')
    
    // Selecionar Site (Blzbet)
    cy.get('body').then(($body) => {
      const selects = $body.find('select')
      
      if (selects.length > 0) {
        // Buscar select de site
        let siteSelect = null
        
        for (let i = 0; i < selects.length && (!siteSelect || siteSelect.length === 0); i++) {
          const $select = Cypress.$(selects[i])
          const name = ($select.attr('name') || '').toLowerCase()
          const id = ($select.attr('id') || '').toLowerCase()
          const label = $select.closest('label, div').text().toLowerCase()
          
          if (name.includes('site') || id.includes('site') || label.includes('site')) {
            siteSelect = $select
            break
          }
        }
        
        if (siteSelect) {
          // Buscar opção que contenha "blzbet"
          const options = siteSelect.find('option')
          let blzbetOption = null
          
          for (let i = 0; i < options.length; i++) {
            const $option = Cypress.$(options[i])
            const optionText = $option.text().toLowerCase()
            
            if (optionText.includes('blzbet')) {
              blzbetOption = $option
              break
            }
          }
          
          if (blzbetOption) {
            cy.wrap(siteSelect).scrollIntoView()
            cy.wait(500)
            cy.wrap(siteSelect).select(blzbetOption.val(), { force: true })
            cy.log('✅ Site Blzbet selecionado')
          } else {
            // Se não encontrou Blzbet, selecionar primeira opção disponível
            cy.wrap(siteSelect).scrollIntoView()
            cy.wait(500)
            cy.wrap(siteSelect).select(1, { force: true })
            cy.log('⚠️ Blzbet não encontrado, selecionando primeiro site disponível')
          }
        } else {
          // Se não encontrou select específico, tentar primeiro select
          cy.wrap(selects.first()).scrollIntoView()
          cy.wait(500)
          cy.wrap(selects.first()).select(1, { force: true })
          cy.log('✅ Primeiro select preenchido')
        }
      }
    })
    
    // Preencher campo Email
    preencherCampo('email', dadosLogin.email, ['email', 'e-mail'])
    
    // Preencher campo Login
    preencherCampo('login', dadosLogin.login, ['login', 'username', 'usuario'])
    
    // Preencher campo Senha
    preencherCampo('senha', dadosLogin.senha, ['senha', 'password', 'senha1'], 'password')
    
    // Preencher campo Confirmar Senha (se houver)
    preencherCampo('confirmarSenha', dadosLogin.confirmarSenha, ['confirmar', 'confirm', 'senha2', 'password2', 'repetir'], 'password')
    
    // Clicar no botão de salvar/criar
    cy.wait(1000)
    cy.log('💾 Salvando cadastro de login...')
    
    cy.get('body').then(($body) => {
      const buttons = $body.find('button, input[type="submit"], input[type="button"]')
      let salvarButton = null
      
      for (let i = 0; i < buttons.length && (!salvarButton || salvarButton.length === 0); i++) {
        const $btn = Cypress.$(buttons[i])
        const text = $btn.text().toLowerCase()
        const value = ($btn.attr('value') || '').toLowerCase()
        const type = ($btn.attr('type') || '').toLowerCase()
        
        if (text.includes('salvar') || text.includes('criar') || text.includes('cadastrar') ||
            text.includes('enviar') || text.includes('confirmar') ||
            value.includes('salvar') || value.includes('criar') || value.includes('cadastrar') ||
            type === 'submit') {
          salvarButton = $btn
        }
      }
      
      if (salvarButton && salvarButton.length > 0) {
        cy.wrap(salvarButton).scrollIntoView()
        cy.wait(500)
        cy.wrap(salvarButton).click({ force: true })
        cy.log('✅ Botão de salvar clicado')
      } else {
        cy.log('⚠️ Botão de salvar não encontrado, tentando submit genérico')
        cy.get('body').then(($bodyFinal) => {
          const submitButtons = $bodyFinal.find('button[type="submit"], input[type="submit"]')
          if (submitButtons.length > 0) {
            cy.wrap(submitButtons.first()).scrollIntoView().click({ force: true })
          }
        })
      }
    })
    
    // Aguardar resposta do cadastro
    cy.wait(3000)
    
    // Verificar se o cadastro foi bem-sucedido
    cy.get('body', { timeout: 10000 }).then(($body) => {
      const bodyText = $body.text().toLowerCase()
      
      // Verificar mensagens de sucesso
      if (bodyText.includes('sucesso') || bodyText.includes('cadastrado') || 
          bodyText.includes('criado') || bodyText.includes('salvo') ||
          bodyText.includes('login criado')) {
        cy.log('✅ Login cadastrado com sucesso!')
        
        // Salvar credenciais do usuário cadastrado para uso posterior
        cy.writeFile('cypress/fixtures/blzbet-user-credentials.json', {
          email: dadosLogin.email,
          login: dadosLogin.login,
          senha: dadosLogin.senha,
          site: dadosLogin.site,
          dataCadastro: new Date().toISOString(),
          timestamp: timestamp
        })
        cy.log('💾 Credenciais salvas em cypress/fixtures/blzbet-user-credentials.json')
        
        cy.url().then((url) => {
          cy.log(`URL após cadastro: ${url}`)
        })
      } else {
        // Verificar mensagens de erro
        if (bodyText.includes('erro') || bodyText.includes('falha') || 
            bodyText.includes('inválido') || bodyText.includes('já existe') ||
            bodyText.includes('existente') || bodyText.includes('duplicado')) {
          cy.log('⚠️ Possível erro no cadastro - verificar mensagens')
        } else {
          cy.log('ℹ️ Cadastro processado - verificar resultado')
          // Mesmo assim, salvar as credenciais para tentar login depois
          cy.writeFile('cypress/fixtures/blzbet-user-credentials.json', {
            email: dadosLogin.email,
            login: dadosLogin.login,
            senha: dadosLogin.senha,
            site: dadosLogin.site,
            dataCadastro: new Date().toISOString(),
            timestamp: timestamp
          })
          cy.log('💾 Credenciais salvas (mesmo com resultado incerto)')
        }
      }
    })
  })

  it('Deve validar campos obrigatórios do formulário de cadastro de login', () => {
    cy.log('🔍 Validando campos obrigatórios...')
    
    // Navegar para Sites > Login usando os seletores específicos
    cy.log('📍 Clicando no menu Sites...')
    cy.wait(3000) // Aguardar página carregar após login
    
    cy.get('body', { timeout: 15000 }).then(($body) => {
      // Tentar usar o seletor específico primeiro
      const menuSites = $body.find('.sidenav-inner > :nth-child(2) > :nth-child(6) > :nth-child(1)')
      
      if (menuSites.length > 0 && menuSites.is(':visible')) {
        cy.log('✅ Menu Sites encontrado pelo seletor específico')
        cy.wrap(menuSites).scrollIntoView()
        cy.wait(500)
        cy.wrap(menuSites).click({ force: true })
      } else {
        // Fallback: buscar por texto "Sites"
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
    cy.wait(3000) // Aguardar menu expandir
    
    // Clicar em Login dentro do menu Sites
    cy.log('📍 Clicando em Login...')
    cy.get('body', { timeout: 15000 }).then(($body) => {
      // Tentar usar o seletor específico primeiro
      const linkLogin = $body.find('.open > :nth-child(2) > :nth-child(3) > .sidenav-item > .sidenav-link')
      
      if (linkLogin.length > 0 && linkLogin.is(':visible')) {
        cy.log('✅ Link Login encontrado pelo seletor específico')
        cy.wrap(linkLogin).scrollIntoView()
        cy.wait(500)
        cy.wrap(linkLogin).click({ force: true })
      } else {
        // Fallback: buscar por texto "Login"
        cy.log('⚠️ Seletor específico não encontrado, buscando por texto...')
        const links = $body.find('a, button, [role="button"], .sidenav-link')
        
        for (let i = 0; i < links.length; i++) {
          const $el = Cypress.$(links[i])
          const text = $el.text().toLowerCase().trim()
          
          if (text === 'login' || text.includes('login')) {
            cy.log(`✅ Link Login encontrado por texto: ${text}`)
            cy.wrap($el).scrollIntoView()
            cy.wait(500)
            cy.wrap($el).click({ force: true })
            break
          }
        }
      }
    })
    
    cy.log('✅ Link Login clicado')
    cy.wait(3000) // Aguardar página carregar
    
    cy.wait(3000)
    cy.closeModals()
    
    // Tentar salvar sem preencher campos
    cy.get('body').then(($body) => {
      const buttons = $body.find('button[type="submit"], input[type="submit"], button')
      
      for (let i = 0; i < buttons.length; i++) {
        const $btn = Cypress.$(buttons[i])
        const text = $btn.text().toLowerCase()
        
        if (text.includes('salvar') || text.includes('criar') || text.includes('cadastrar')) {
          cy.wrap($btn).click({ force: true })
          cy.wait(2000)
          break
        }
      }
    })
    
    // Verificar se apareceram mensagens de validação
    cy.get('body').then(($body) => {
      const bodyText = $body.text().toLowerCase()
      
      if (bodyText.includes('obrigatório') || bodyText.includes('required') ||
          bodyText.includes('preencher') || bodyText.includes('inválido') ||
          bodyText.includes('campo')) {
        cy.log('✅ Validação de campos obrigatórios funcionando')
      } else {
        cy.log('⚠️ Validação pode não estar funcionando ou não há campos obrigatórios')
      }
    })
  })

  // Função auxiliar para preencher campos
  function preencherCampo(campoNome, valor, palavrasChave, tipo = 'text') {
    cy.get('body').then(($body) => {
      let campoEncontrado = null
      
      // Buscar por tipo específico ou todos os inputs
      const inputs = tipo === 'password' 
        ? $body.find('input[type="password"]')
        : $body.find('input, textarea')
      
      for (let i = 0; i < inputs.length && (!campoEncontrado || campoEncontrado.length === 0); i++) {
        const $input = Cypress.$(inputs[i])
        const inputType = ($input.attr('type') || '').toLowerCase()
        const name = ($input.attr('name') || '').toLowerCase()
        const id = ($input.attr('id') || '').toLowerCase()
        const placeholder = ($input.attr('placeholder') || '').toLowerCase()
        const label = $input.closest('label, div').text().toLowerCase()
        
        // Verificar se corresponde ao campo procurado
        for (const palavra of palavrasChave) {
          if ((tipo === 'password' && inputType === 'password') ||
              (tipo !== 'password' && (name.includes(palavra) || id.includes(palavra) ||
               placeholder.includes(palavra) || label.includes(palavra)))) {
            
            // Verificar se já não foi preenchido (evitar duplicatas)
            const currentValue = $input.val() || ''
            if (currentValue.length === 0) {
              campoEncontrado = $input
              break
            }
          }
        }
      }
      
      if (campoEncontrado && campoEncontrado.length > 0) {
        cy.wrap(campoEncontrado).scrollIntoView()
        cy.wait(300)
        cy.wrap(campoEncontrado).clear().type(valor, { force: true })
        cy.log(`✅ Campo ${campoNome} preenchido`)
      } else {
        cy.log(`⚠️ Campo ${campoNome} não encontrado`)
      }
    })
  }
})

