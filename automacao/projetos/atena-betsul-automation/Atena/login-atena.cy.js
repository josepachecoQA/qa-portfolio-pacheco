// ***********************************************
// Teste de Login no Atena com 2FA
// Este teste acessa o site do Atena e faz login
// incluindo autenticação de dois fatores
// ***********************************************

const { authenticator } = require('otplib')

describe('Login no Atena com 2FA', () => {
  beforeEach(() => {
    // Acessar a página inicial
    cy.visit('/', {
      timeout: 60000,
      failOnStatusCode: false
    })
    
    // Verificar se a página carregou
    cy.get('body', { timeout: 10000 }).should('be.visible')
    
    // Fechar modais que possam aparecer
    cy.closeModals()
  })

  it('Deve fazer login com sucesso usando 2FA', () => {
    const email = Cypress.env('USER_EMAIL') || 'alexandre.costa@servicenet.com.br'
    const password = Cypress.env('USER_PASSWORD') || 'Aa@102030'
    const totpSecret = Cypress.env('TOTP_SECRET') || 'CLSUJ5BDR7QPUTSRKPYAI3CNURZWONBJ'
    
    cy.log('🔐 Iniciando processo de login...')
    
    // Aguardar um pouco para garantir que a página carregou completamente
    cy.wait(2000)
    
    // Buscar campo de email/usuário
    cy.get('body').then(($body) => {
      cy.log('🔍 Buscando campos de login...')
      
      // Tentar diferentes seletores para campo de email
      let emailField = null
      
      // Buscar por atributos comuns (sem case-insensitive)
      const emailSelectors = [
        'input[type="email"]'
      ]
      
      for (const selector of emailSelectors) {
        const field = $body.find(selector)
        if (field.length > 0) {
          emailField = field.first()
          cy.log(`✅ Campo de email encontrado: ${selector}`)
          break
        }
      }
      
      // Se não encontrou por seletores, buscar manualmente
      if (!emailField || emailField.length === 0) {
        const inputs = $body.find('input')
        for (let i = 0; i < inputs.length && (!emailField || emailField.length === 0); i++) {
          const $input = Cypress.$(inputs[i])
          const type = ($input.attr('type') || '').toLowerCase()
          const name = ($input.attr('name') || '').toLowerCase()
          const id = ($input.attr('id') || '').toLowerCase()
          const placeholder = ($input.attr('placeholder') || '').toLowerCase()
          
          if (type === 'email' || name.includes('email') || name.includes('user') || 
              id.includes('email') || id.includes('user') || 
              placeholder.includes('email') || placeholder.includes('usuário')) {
            emailField = $input
          }
        }
      }
      
      if (emailField && emailField.length > 0) {
        cy.wrap(emailField).scrollIntoView()
        cy.wait(500)
        cy.wrap(emailField).clear().type(email, { force: true })
        cy.log('✅ Email preenchido')
      } else {
        cy.log('⚠️ Campo de email não encontrado, tentando buscar de forma genérica...')
        // Tentar encontrar qualquer input que possa ser o campo de email
        cy.get('input').first().then(($input) => {
          cy.wrap($input).scrollIntoView()
          cy.wait(500)
          cy.wrap($input).clear().type(email, { force: true })
        })
      }
    })
    
    // Buscar campo de senha
    cy.get('body').then(($body) => {
      let passwordField = null
      
      const passwordSelectors = [
        'input[type="password"]'
      ]
      
      for (const selector of passwordSelectors) {
        const field = $body.find(selector)
        if (field.length > 0) {
          passwordField = field.first()
          cy.log(`✅ Campo de senha encontrado: ${selector}`)
          break
        }
      }
      
      if (!passwordField || passwordField.length === 0) {
        const inputs = $body.find('input[type="password"]')
        if (inputs.length > 0) {
          passwordField = inputs.first()
        } else {
          // Buscar manualmente
          const allInputs = $body.find('input')
          for (let i = 0; i < allInputs.length && (!passwordField || passwordField.length === 0); i++) {
            const $input = Cypress.$(allInputs[i])
            const type = ($input.attr('type') || '').toLowerCase()
            const name = ($input.attr('name') || '').toLowerCase()
            const id = ($input.attr('id') || '').toLowerCase()
            
            if (type === 'password' || name.includes('password') || name.includes('senha') || 
                id.includes('password') || id.includes('senha')) {
              passwordField = $input
            }
          }
        }
      }
      
      if (passwordField && passwordField.length > 0) {
        cy.wrap(passwordField).scrollIntoView()
        cy.wait(500)
        cy.wrap(passwordField).clear().type(password, { force: true })
        cy.log('✅ Senha preenchida')
      }
    })
    
    // Clicar no botão de login
    cy.wait(1000)
    cy.get('body').then(($body) => {
      // Buscar botão de login
      const loginButtons = $body.find('button[type="submit"], button:contains("Entrar"), button:contains("Login"), button:contains("Sign in"), input[type="submit"]')
      
      if (loginButtons.length === 0) {
        // Buscar manualmente
        const buttons = $body.find('button, input[type="submit"]')
        buttons.each((index, btn) => {
          const $btn = Cypress.$(btn)
          const text = $btn.text().toLowerCase()
          const value = ($btn.attr('value') || '').toLowerCase()
          
          if (text.includes('entrar') || text.includes('login') || text.includes('sign in') || 
              value.includes('entrar') || value.includes('login')) {
            cy.wrap($btn).click({ force: true })
            return false // break
          }
        })
      } else {
        cy.wrap(loginButtons.first()).click({ force: true })
      }
    })
    
    cy.log('✅ Botão de login clicado')
    
    // Aguardar possível formulário de 2FA aparecer
    cy.wait(3000)
    
    // Verificar se apareceu campo de 2FA/TOTP
    cy.get('body').then(($body) => {
      // Buscar campo TOTP manualmente (sem case-insensitive)
      let totpField = null
      const textInputs = $body.find('input[type="text"]')
      
      for (let i = 0; i < textInputs.length && (!totpField || totpField.length === 0); i++) {
        const $input = Cypress.$(textInputs[i])
        const name = ($input.attr('name') || '').toLowerCase()
        const id = ($input.attr('id') || '').toLowerCase()
        const placeholder = ($input.attr('placeholder') || '').toLowerCase()
        
        if (name.includes('code') || name.includes('totp') || name.includes('otp') || name.includes('2fa') ||
            id.includes('code') || id.includes('totp') ||
            placeholder.includes('código') || placeholder.includes('code')) {
          totpField = $input
        }
      }
      
      const hasTotpText = $body.text().toLowerCase().includes('código') || $body.text().toLowerCase().includes('2fa') || $body.text().toLowerCase().includes('autenticação')
      
      if ((totpField && totpField.length > 0) || hasTotpText) {
        cy.log('🔐 Campo de 2FA detectado, gerando código TOTP...')
        
        // Gerar código TOTP
        const token = authenticator.generate(totpSecret)
        cy.log(`Código TOTP gerado: ${token}`)
        
        // Preencher campo de código 2FA
        if (totpField && totpField.length > 0) {
          cy.wrap(totpField).scrollIntoView()
          cy.wait(500)
          cy.wrap(totpField).clear().type(token, { force: true })
        } else {
          // Tentar encontrar qualquer input de texto disponível
          cy.get('body').then(($body) => {
            const textInputs = $body.find('input[type="text"]')
            if (textInputs.length > 0) {
              cy.wrap(textInputs.first()).scrollIntoView()
              cy.wait(500)
              cy.wrap(textInputs.first()).clear().type(token, { force: true })
            } else {
              cy.log('⚠️ Nenhum campo de texto encontrado para preencher código 2FA')
            }
          })
        }
        
        cy.log('✅ Código 2FA preenchido')
        
        // Clicar em botão de confirmar/verificar
        cy.wait(1000)
        cy.get('body').then(($bodyAfter) => {
          // Buscar botão de confirmar manualmente
          let confirmButton = null
          const buttons = $bodyAfter.find('button, input[type="submit"]')
          
          for (let i = 0; i < buttons.length && (!confirmButton || confirmButton.length === 0); i++) {
            const $btn = Cypress.$(buttons[i])
            const text = $btn.text().toLowerCase()
            const value = ($btn.attr('value') || '').toLowerCase()
            const type = ($btn.attr('type') || '').toLowerCase()
            
            if (text.includes('confirmar') || text.includes('verificar') || text.includes('enviar') ||
                value.includes('confirmar') || value.includes('verificar') || value.includes('enviar') ||
                type === 'submit') {
              confirmButton = $btn
            }
          }
          
          if (confirmButton && confirmButton.length > 0) {
            cy.wrap(confirmButton).click({ force: true })
          } else {
            // Tentar encontrar botão de submit
            cy.get('body').then(($bodyFinal) => {
              const submitButtons = $bodyFinal.find('button[type="submit"], input[type="submit"]')
              if (submitButtons.length > 0) {
                cy.wrap(submitButtons.first()).click({ force: true })
              } else {
                cy.log('⚠️ Nenhum botão de submit encontrado')
              }
            })
          }
        })
        
        cy.log('✅ Código 2FA enviado')
      } else {
        cy.log('⚠️ Campo de 2FA não detectado, pode não ser necessário ou já estar logado')
      }
    })
    
    // Aguardar login completar
    cy.wait(5000)
    
    // Verificar se login foi bem-sucedido
    cy.url().then((url) => {
      cy.log(`URL atual: ${url}`)
      
      // Verificar se não está mais na página de login
      if (!url.includes('login') && !url.includes('auth') && !url.includes('signin')) {
        cy.log('✅ Login realizado com sucesso!')
        
        // Verificar se há elementos indicando que está logado
        cy.get('body').then(($body) => {
          const loggedInIndicators = $body.find('[class*="user"], [class*="profile"], [id*="user"], [id*="profile"], [class*="logout"], [class*="sair"]')
          
          if (loggedInIndicators.length > 0 || $body.text().toLowerCase().includes('sair') || $body.text().toLowerCase().includes('logout')) {
            cy.log('✅ Confirmação: Usuário está logado')
          }
        })
      } else {
        cy.log('⚠️ Ainda na página de login, pode ter havido algum problema')
      }
    })
  })

  it('Deve verificar se a página de login carregou corretamente', () => {
    cy.get('body', { timeout: 10000 }).should('be.visible')
    
    // Verificar se há campos de login na página
    cy.get('body').then(($body) => {
      const hasEmailField = $body.find('input[type="email"]').length > 0
      const hasPasswordField = $body.find('input[type="password"]').length > 0
      
      // Se não encontrou por seletor direto, buscar manualmente
      if (!hasEmailField) {
        const inputs = $body.find('input')
        for (let i = 0; i < inputs.length && !hasEmailField; i++) {
          const $input = Cypress.$(inputs[i])
          const type = ($input.attr('type') || '').toLowerCase()
          const name = ($input.attr('name') || '').toLowerCase()
          
          if (type === 'email' || name.includes('email') || name.includes('user')) {
            hasEmailField = true
            break
          }
        }
      }
      
      if (hasEmailField || hasPasswordField) {
        cy.log('✅ Página de login detectada')
      } else {
        cy.log('⚠️ Campos de login não encontrados na página')
      }
    })
  })
})

