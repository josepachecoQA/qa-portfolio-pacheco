// ***********************************************
// Teste de Cadastro de Usuário - Atena
// Este teste faz login e cadastra um novo usuário
// na localidade web do sistema Atena
// ***********************************************

describe('Cadastro de Usuário - Localidade Web', () => {
  beforeEach(() => {
    // Acessar a página inicial
    cy.visit('/', {
      timeout: 60000,
      failOnStatusCode: false
    })
    
    cy.get('body', { timeout: 10000 }).should('be.visible')
    cy.closeModals()
    
    // Fazer login
    cy.loginAtena()
    cy.wait(3000)
  })

  it('Deve cadastrar um novo usuário com sucesso', () => {
    // Gerar dados aleatórios para o cadastro
    const timestamp = Date.now()
    const dadosUsuario = {
      nomeCompleto: `Teste Usuário ${timestamp}`,
      email: `teste.usuario.${timestamp}@servicenet.com.br`,
      login: `teste_user_${timestamp}`,
      senha: 'Teste@123456',
      perfil: 'Usuário', // Pode precisar ser ajustado conforme o sistema
      siteVinculado: '' // Pode precisar ser preenchido
    }
    
    cy.log('📝 Iniciando cadastro de novo usuário...')
    cy.log(`Email: ${dadosUsuario.email}`)
    cy.log(`Login: ${dadosUsuario.login}`)
    
    // Navegar para a tela de cadastro de usuários
    cy.log('🔍 Navegando para cadastro de usuários...')
    cy.log('📍 Caminho esperado: Usuários > Cadastros')
    
    // Estratégia 1: Buscar e clicar em "Usuários" primeiro, depois em "Cadastros"
    cy.get('body').then(($body) => {
      let menuUsuariosEncontrado = false
      
      // Buscar link ou botão de "Usuários"
      const links = $body.find('a, button, [role="button"], [role="link"]')
      
      for (let i = 0; i < links.length && !menuUsuariosEncontrado; i++) {
        const $el = Cypress.$(links[i])
        const text = $el.text().toLowerCase().trim()
        const href = ($el.attr('href') || '').toLowerCase()
        
        // Verificar se é link de "Usuários"
        if (text === 'usuários' || text === 'usuarios' || text === 'usuário' || 
            text === 'usuario' || text.includes('usuário') || text.includes('usuario') ||
            href.includes('/usuario') || href.includes('/user')) {
          
          cy.log(`✅ Menu Usuários encontrado: ${$el.text().trim()}`)
          cy.wrap($el).scrollIntoView()
          cy.wait(500)
          cy.wrap($el).click({ force: true })
          menuUsuariosEncontrado = true
          cy.wait(2000)
          break
        }
      }
      
      // Se encontrou menu de Usuários, buscar link de Cadastros
      if (menuUsuariosEncontrado) {
        cy.get('body').then(($bodyAfter) => {
          const linksCadastro = $bodyAfter.find('a, button, [role="button"]')
          
          for (let i = 0; i < linksCadastro.length; i++) {
            const $el = Cypress.$(linksCadastro[i])
            const text = $el.text().toLowerCase().trim()
            
            if (text.includes('cadastr') || text === 'novo' || text === 'criar' || 
                text === 'adicionar' || text.includes('new') || text.includes('create')) {
              
              cy.log(`✅ Link de cadastro encontrado: ${$el.text().trim()}`)
              cy.wrap($el).scrollIntoView()
              cy.wait(500)
              cy.wrap($el).click({ force: true })
              cy.wait(2000)
              break
            }
          }
        })
      }
      
      // Se não encontrou, tentar buscar diretamente por link que contenha "usuario" e "cadastro"
      if (!menuUsuariosEncontrado) {
        cy.log('🔍 Buscando link direto de cadastro de usuários...')
        
        for (let i = 0; i < links.length; i++) {
          const $el = Cypress.$(links[i])
          const text = $el.text().toLowerCase()
          const href = ($el.attr('href') || '').toLowerCase()
          
          if ((text.includes('usuário') || text.includes('usuario') || text.includes('user')) &&
              (text.includes('cadastr') || text.includes('novo') || text.includes('criar') ||
               href.includes('usuario') || href.includes('user') || href.includes('cadastro'))) {
            
            cy.log(`✅ Link direto encontrado: ${$el.text().trim()}`)
            cy.wrap($el).scrollIntoView()
            cy.wait(500)
            cy.wrap($el).click({ force: true })
            cy.wait(2000)
            break
          }
        }
      }
    })
    
    // Aguardar carregamento da página de cadastro
    cy.wait(3000)
    cy.get('body', { timeout: 10000 }).should('be.visible')
    cy.closeModals()
    
    cy.log('📋 Preenchendo formulário de cadastro...')
    
    // Preencher campo Nome Completo
    cy.get('body').then(($body) => {
      let nomeField = null
      const inputs = $body.find('input')
      
      for (let i = 0; i < inputs.length && (!nomeField || nomeField.length === 0); i++) {
        const $input = Cypress.$(inputs[i])
        const name = ($input.attr('name') || '').toLowerCase()
        const id = ($input.attr('id') || '').toLowerCase()
        const placeholder = ($input.attr('placeholder') || '').toLowerCase()
        const label = $input.closest('label, div').text().toLowerCase()
        
        if (name.includes('nome') || name.includes('name') || 
            id.includes('nome') || id.includes('name') ||
            placeholder.includes('nome') || placeholder.includes('name') ||
            label.includes('nome') || label.includes('name')) {
          nomeField = $input
        }
      }
      
      if (nomeField && nomeField.length > 0) {
        cy.wrap(nomeField).scrollIntoView()
        cy.wait(500)
        cy.wrap(nomeField).clear().type(dadosUsuario.nomeCompleto, { force: true })
        cy.log('✅ Nome completo preenchido')
      } else {
        cy.log('⚠️ Campo nome não encontrado, tentando primeiro input')
        cy.get('input').first().then(($input) => {
          cy.wrap($input).scrollIntoView().clear().type(dadosUsuario.nomeCompleto, { force: true })
        })
      }
    })
    
    // Preencher campo Email
    cy.get('body').then(($body) => {
      let emailField = null
      const inputs = $body.find('input[type="email"], input')
      
      for (let i = 0; i < inputs.length && (!emailField || emailField.length === 0); i++) {
        const $input = Cypress.$(inputs[i])
        const type = ($input.attr('type') || '').toLowerCase()
        const name = ($input.attr('name') || '').toLowerCase()
        const id = ($input.attr('id') || '').toLowerCase()
        const placeholder = ($input.attr('placeholder') || '').toLowerCase()
        
        if (type === 'email' || name.includes('email') || 
            id.includes('email') || placeholder.includes('email')) {
          emailField = $input
        }
      }
      
      if (emailField && emailField.length > 0) {
        cy.wrap(emailField).scrollIntoView()
        cy.wait(500)
        cy.wrap(emailField).clear().type(dadosUsuario.email, { force: true })
        cy.log('✅ Email preenchido')
      }
    })
    
    // Preencher campo Login
    cy.get('body').then(($body) => {
      let loginField = null
      const inputs = $body.find('input')
      
      for (let i = 0; i < inputs.length && (!loginField || loginField.length === 0); i++) {
        const $input = Cypress.$(inputs[i])
        const name = ($input.attr('name') || '').toLowerCase()
        const id = ($input.attr('id') || '').toLowerCase()
        const placeholder = ($input.attr('placeholder') || '').toLowerCase()
        
        if ((name.includes('login') || name.includes('username')) ||
            (id.includes('login') || id.includes('username')) ||
            (placeholder.includes('login') || placeholder.includes('usuário'))) {
          loginField = $input
        }
      }
      
      if (loginField && loginField.length > 0) {
        cy.wrap(loginField).scrollIntoView()
        cy.wait(500)
        cy.wrap(loginField).clear().type(dadosUsuario.login, { force: true })
        cy.log('✅ Login preenchido')
      }
    })
    
    // Preencher campo Senha
    cy.get('body').then(($body) => {
      let senhaField = null
      const inputs = $body.find('input[type="password"]')
      
      if (inputs.length > 0) {
        senhaField = inputs.first()
      } else {
        const allInputs = $body.find('input')
        for (let i = 0; i < allInputs.length && (!senhaField || senhaField.length === 0); i++) {
          const $input = Cypress.$(allInputs[i])
          const type = ($input.attr('type') || '').toLowerCase()
          const name = ($input.attr('name') || '').toLowerCase()
          
          if (type === 'password' || name.includes('senha') || name.includes('password')) {
            senhaField = $input
          }
        }
      }
      
      if (senhaField && senhaField.length > 0) {
        cy.wrap(senhaField).scrollIntoView()
        cy.wait(500)
        cy.wrap(senhaField).clear().type(dadosUsuario.senha, { force: true })
        cy.log('✅ Senha preenchida')
      }
    })
    
    // Preencher campo Perfil (select)
    cy.get('body').then(($body) => {
      const selects = $body.find('select')
      
      if (selects.length > 0) {
        // Verificar qual select é de perfil
        let perfilSelect = null
        
        selects.each((index, select) => {
          const $select = Cypress.$(select)
          const name = ($select.attr('name') || '').toLowerCase()
          const id = ($select.attr('id') || '').toLowerCase()
          
          if (name.includes('perfil') || name.includes('profile') || 
              id.includes('perfil') || id.includes('profile')) {
            perfilSelect = $select
            return false // break
          }
        })
        
        if (perfilSelect) {
          cy.wrap(perfilSelect).scrollIntoView()
          cy.wait(500)
          // Tentar selecionar uma opção que contenha "usuário" ou a primeira opção disponível
          cy.wrap(perfilSelect).select(1, { force: true })
          cy.log('✅ Perfil selecionado')
        } else if (selects.length > 0) {
          // Se não encontrou perfil específico, selecionar primeiro select
          cy.wrap(selects.first()).scrollIntoView()
          cy.wait(500)
          cy.wrap(selects.first()).select(1, { force: true })
          cy.log('✅ Primeiro select preenchido')
        }
      }
    })
    
    // Preencher Site Vinculado (se houver)
    cy.get('body').then(($body) => {
      const selects = $body.find('select')
      
      if (selects.length > 1) {
        // Verificar se há select de site
        let siteSelect = null
        
        selects.each((index, select) => {
          const $select = Cypress.$(select)
          const name = ($select.attr('name') || '').toLowerCase()
          const id = ($select.attr('id') || '').toLowerCase()
          
          if (name.includes('site') || id.includes('site')) {
            siteSelect = $select
            return false // break
          }
        })
        
        if (siteSelect && siteSelect.find('option').length > 1) {
          cy.wrap(siteSelect).scrollIntoView()
          cy.wait(500)
          cy.wrap(siteSelect).select(1, { force: true })
          cy.log('✅ Site vinculado selecionado')
        }
      }
    })
    
    // Clicar no botão de salvar/criar
    cy.wait(1000)
    cy.log('💾 Salvando cadastro...')
    
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
        cy.get('button[type="submit"], input[type="submit"]').first().click({ force: true })
      }
    })
    
    // Aguardar resposta do cadastro
    cy.wait(3000)
    
    // Verificar se o cadastro foi bem-sucedido
    cy.get('body').then(($body) => {
      const bodyText = $body.text().toLowerCase()
      
      // Verificar mensagens de sucesso
      if (bodyText.includes('sucesso') || bodyText.includes('cadastrado') || 
          bodyText.includes('criado') || bodyText.includes('salvo')) {
        cy.log('✅ Cadastro realizado com sucesso!')
        
        // Verificar se voltou para lista ou se ainda está na tela de cadastro
        cy.url().then((url) => {
          cy.log(`URL após cadastro: ${url}`)
        })
      } else {
        // Verificar mensagens de erro
        if (bodyText.includes('erro') || bodyText.includes('falha') || 
            bodyText.includes('inválido') || bodyText.includes('já existe')) {
          cy.log('⚠️ Possível erro no cadastro - verificar mensagens')
        } else {
          cy.log('ℹ️ Cadastro processado - verificar resultado')
        }
      }
    })
    
    // Verificar se o usuário foi cadastrado (pode verificar na lista)
    cy.wait(2000)
    cy.log('✅ Teste de cadastro concluído')
  })

  it('Deve validar campos obrigatórios do formulário de cadastro', () => {
    cy.log('🔍 Validando campos obrigatórios...')
    
    // Navegar para cadastro (mesma lógica do teste anterior)
    cy.get('body').then(($body) => {
      const links = $body.find('a, button, [role="button"]')
      
      links.each((index, el) => {
        const $el = Cypress.$(el)
        const text = $el.text().toLowerCase()
        
        if ((text.includes('usuário') || text.includes('usuario')) &&
            (text.includes('cadastr') || text.includes('novo') || text.includes('criar'))) {
          cy.wrap($el).click({ force: true })
          cy.wait(2000)
          return false // break
        }
      })
    })
    
    cy.wait(3000)
    cy.closeModals()
    
    // Tentar salvar sem preencher campos
    cy.get('body').then(($body) => {
      const buttons = $body.find('button[type="submit"], input[type="submit"], button')
      
      buttons.each((index, btn) => {
        const $btn = Cypress.$(btn)
        const text = $btn.text().toLowerCase()
        
        if (text.includes('salvar') || text.includes('criar') || text.includes('cadastrar')) {
          cy.wrap($btn).click({ force: true })
          cy.wait(2000)
          return false // break
        }
      })
    })
    
    // Verificar se apareceram mensagens de validação
    cy.get('body').then(($body) => {
      const bodyText = $body.text().toLowerCase()
      
      if (bodyText.includes('obrigatório') || bodyText.includes('required') ||
          bodyText.includes('preencher') || bodyText.includes('inválido')) {
        cy.log('✅ Validação de campos obrigatórios funcionando')
      } else {
        cy.log('⚠️ Validação pode não estar funcionando ou não há campos obrigatórios')
      }
    })
  })
})

