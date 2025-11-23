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
 */
Cypress.Commands.add('closeModals', () => {
  // Tentar fechar usando ESC
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

    // Tentar fechar prompts de notificação
    const webPushPrompt = $body.find('#webpush-custom-prompt-text, [id*="webpush"], [class*="webpush"]')
    if (webPushPrompt.length > 0) {
      // Tentar encontrar botão de fechar
      let closeButton = $body.find('[class*="close"]').first()
      if (closeButton.length === 0) {
        closeButton = $body.find('[class*="dismiss"]').first()
      }
      if (closeButton.length === 0) {
        closeButton = webPushPrompt.find('button').first()
      }
      
      if (closeButton.length > 0) {
        cy.wrap(closeButton).click({ force: true })
        cy.wait(500)
      } else {
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

/**
 * Comando para gerar código TOTP (2FA)
 */
Cypress.Commands.add('generateTOTP', (secret) => {
  // Importar otplib dinamicamente
  const { authenticator } = require('otplib')
  
  // Gerar código TOTP
  const token = authenticator.generate(secret)
  
  cy.log(`Código TOTP gerado: ${token}`)
  
  return cy.wrap(token)
})

/**
 * Comando para fazer login no Atena
 */
Cypress.Commands.add('loginAtena', () => {
  const email = Cypress.env('USER_EMAIL') || 'alexandre.costa@servicenet.com.br'
  const password = Cypress.env('USER_PASSWORD') || 'Aa@102030'
  const totpSecret = Cypress.env('TOTP_SECRET') || 'CLSUJ5BDR7QPUTSRKPYAI3CNURZWONBJ'
  const { authenticator } = require('otplib')
  
  cy.log('🔐 Fazendo login no Atena...')
  
  // Aguardar página carregar completamente
  cy.wait(2000)
  
  // Buscar e preencher email
  cy.get('body', { timeout: 15000 }).should('be.visible').then(($body) => {
    let emailField = null
    const inputs = $body.find('input')
    
    for (let i = 0; i < inputs.length && (!emailField || emailField.length === 0); i++) {
      const $input = Cypress.$(inputs[i])
      const type = ($input.attr('type') || '').toLowerCase()
      const name = ($input.attr('name') || '').toLowerCase()
      const id = ($input.attr('id') || '').toLowerCase()
      
      if (type === 'email' || name.includes('email') || name.includes('user') || 
          id.includes('email') || id.includes('user')) {
        emailField = $input
        break
      }
    }
    
    if (emailField && emailField.length > 0) {
      cy.wrap(emailField).scrollIntoView()
      cy.wait(500)
      cy.wrap(emailField).clear().type(email, { force: true })
      cy.log('✅ Email preenchido')
    } else {
      cy.log('⚠️ Campo de email não encontrado, tentando primeiro input')
      cy.get('input').first().then(($input) => {
        cy.wrap($input).scrollIntoView().clear().type(email, { force: true })
      })
    }
  })
  
  // Buscar e preencher senha
  cy.wait(500)
  cy.get('body').then(($body) => {
    let passwordField = null
    const inputs = $body.find('input[type="password"]')
    
    if (inputs.length > 0) {
      passwordField = inputs.first()
    } else {
      const allInputs = $body.find('input')
      for (let i = 0; i < allInputs.length && (!passwordField || passwordField.length === 0); i++) {
        const $input = Cypress.$(allInputs[i])
        const type = ($input.attr('type') || '').toLowerCase()
        if (type === 'password') {
          passwordField = $input
          break
        }
      }
    }
    
    if (passwordField && passwordField.length > 0) {
      cy.wrap(passwordField).scrollIntoView()
      cy.wait(500)
      cy.wrap(passwordField).clear().type(password, { force: true })
      cy.log('✅ Senha preenchida')
    } else {
      cy.log('⚠️ Campo de senha não encontrado')
    }
  })
  
  // Clicar no botão de login
  cy.wait(1000)
  cy.get('body').then(($body) => {
    const buttons = $body.find('button, input[type="submit"], input[type="button"], a[role="button"]')
    let loginButton = null
    
    // Buscar especificamente por botão de login
    for (let i = 0; i < buttons.length && (!loginButton || loginButton.length === 0); i++) {
      const $btn = Cypress.$(buttons[i])
      const text = $btn.text().toLowerCase().trim()
      const value = ($btn.attr('value') || '').toLowerCase()
      const type = ($btn.attr('type') || '').toLowerCase()
      const className = ($btn.attr('class') || '').toLowerCase()
      const id = ($btn.attr('id') || '').toLowerCase()
      
      // Buscar por texto específico de login
      if (text === 'entrar' || text === 'login' || text === 'sign in' || 
          text.includes('entrar') || text.includes('login') ||
          value === 'entrar' || value === 'login' || value.includes('entrar') || value.includes('login') ||
          className.includes('login') || className.includes('entrar') ||
          id.includes('login') || id.includes('entrar')) {
        loginButton = $btn
        cy.log(`✅ Botão de login encontrado: texto="${text}", value="${value}"`)
        break
      }
    }
    
    if (loginButton && loginButton.length > 0) {
      cy.wrap(loginButton).scrollIntoView()
      cy.wait(500)
      cy.wrap(loginButton).click({ force: true })
      cy.log('✅ Botão de login clicado')
    } else {
      // Se não encontrou botão específico de login, tentar buscar por submit APENAS se estiver na tela de login
      cy.log('⚠️ Botão de login não encontrado, verificando se está na tela de login...')
      cy.get('body').then(($bodyAfter) => {
        const bodyText = $bodyAfter.text().toLowerCase()
        const hasLoginElements = $bodyAfter.find('input[type="password"], input[type="email"]').length > 0
        
        if (bodyText.includes('login') || bodyText.includes('entrar') || hasLoginElements) {
          cy.log('⚠️ Está na tela de login mas botão não encontrado, tentando submit genérico')
          cy.get('button[type="submit"], input[type="submit"]').first().then(($submit) => {
            if ($submit.length > 0) {
              cy.wrap($submit).scrollIntoView().click({ force: true })
            } else {
              cy.log('❌ Nenhum botão de submit encontrado')
            }
          })
        } else {
          cy.log('⚠️ Não parece estar na tela de login')
        }
      })
    }
  })
  
  // Aguardar possível 2FA aparecer
  cy.wait(4000)
  
  // Verificar se apareceu campo de 2FA
  cy.get('body', { timeout: 15000 }).then(($body) => {
    const bodyText = $body.text().toLowerCase()
    const hasTotpText = bodyText.includes('código') || bodyText.includes('code') || bodyText.includes('2fa') || bodyText.includes('autenticação') || bodyText.includes('totp')
    
    if (hasTotpText) {
      cy.log('🔐 Campo de 2FA detectado, gerando código TOTP...')
      const token = authenticator.generate(totpSecret)
      cy.log(`Código TOTP gerado: ${token}`)
      
      // Buscar campo TOTP - tentar múltiplos tipos de input
      cy.get('body', { timeout: 10000 }).then(($bodyAfter) => {
        let totpField = null
        
        // Buscar em todos os tipos de input (text, number, password, sem type)
        const allInputs = $bodyAfter.find('input')
        
        cy.log(`🔍 Buscando campo TOTP entre ${allInputs.length} inputs...`)
        
        for (let i = 0; i < allInputs.length && (!totpField || totpField.length === 0); i++) {
          const $input = Cypress.$(allInputs[i])
          const type = ($input.attr('type') || '').toLowerCase()
          const name = ($input.attr('name') || '').toLowerCase()
          const id = ($input.attr('id') || '').toLowerCase()
          const placeholder = ($input.attr('placeholder') || '').toLowerCase()
          const className = ($input.attr('class') || '').toLowerCase()
          
          // Verificar se é um campo de código TOTP
          if (type === 'text' || type === 'number' || type === 'tel' || type === '' ||
              name.includes('code') || name.includes('totp') || name.includes('otp') || name.includes('2fa') ||
              id.includes('code') || id.includes('totp') || id.includes('otp') || id.includes('2fa') ||
              placeholder.includes('código') || placeholder.includes('code') || placeholder.includes('totp') ||
              className.includes('code') || className.includes('totp') || className.includes('otp')) {
            
            // Verificar se não é um campo de email ou senha
            if (!name.includes('email') && !name.includes('password') && !name.includes('senha') &&
                !id.includes('email') && !id.includes('password') && !id.includes('senha') &&
                type !== 'password' && type !== 'email') {
              totpField = $input
              cy.log(`✅ Campo TOTP encontrado: name="${name}", id="${id}", type="${type}"`)
              break
            }
          }
        }
        
        // Se não encontrou campo específico, buscar primeiro input de texto visível
        if (!totpField || totpField.length === 0) {
          cy.log('⚠️ Campo TOTP específico não encontrado, buscando primeiro input de texto...')
          const textInputs = $bodyAfter.find('input[type="text"], input[type="number"], input:not([type="password"]):not([type="email"]):not([type="hidden"])')
          
          for (let i = 0; i < textInputs.length; i++) {
            const $input = Cypress.$(textInputs[i])
            const name = ($input.attr('name') || '').toLowerCase()
            const id = ($input.attr('id') || '').toLowerCase()
            
            // Verificar se não é email ou senha
            if (!name.includes('email') && !name.includes('password') && !name.includes('senha') &&
                !id.includes('email') && !id.includes('password') && !id.includes('senha')) {
              totpField = $input
              cy.log(`✅ Usando input alternativo: name="${name}", id="${id}"`)
              break
            }
          }
        }
        
        // Preencher o campo TOTP
        if (totpField && totpField.length > 0) {
          cy.wrap(totpField).scrollIntoView({ duration: 500 })
          cy.wait(500)
          cy.wrap(totpField).clear({ force: true })
          cy.wait(300)
          cy.wrap(totpField).type(token, { force: true, delay: 100 })
          cy.log('✅ Código TOTP digitado no campo')
          
          // Verificar se o valor foi preenchido
          cy.wrap(totpField).should('have.value', token)
          cy.log(`✅ Verificação: Campo contém o código TOTP`)
        } else {
          cy.log('❌ Campo TOTP não encontrado, tentando preencher qualquer input disponível...')
          cy.get('input[type="text"]').first().then(($input) => {
            cy.wrap($input).scrollIntoView()
            cy.wait(500)
            cy.wrap($input).clear({ force: true })
            cy.wait(300)
            cy.wrap($input).type(token, { force: true, delay: 100 })
            cy.log('✅ Código TOTP digitado no primeiro input disponível')
          })
        }
      })
      
      // Aguardar um pouco antes de clicar no botão
      cy.wait(1500)
      
      // Clicar no botão de login (na tela de TOTP também tem botão de login)
      cy.get('body').then(($bodyAfter) => {
        const buttons = $bodyAfter.find('button, input[type="submit"], input[type="button"], a[role="button"]')
        let confirmButton = null
        
        cy.log(`🔍 Buscando botão de login na tela de TOTP entre ${buttons.length} botões...`)
        
        // Buscar especificamente por botão de login primeiro (na tela de TOTP também tem botão de login)
        for (let i = 0; i < buttons.length && (!confirmButton || confirmButton.length === 0); i++) {
          const $btn = Cypress.$(buttons[i])
          const text = $btn.text().toLowerCase().trim()
          const value = ($btn.attr('value') || '').toLowerCase()
          const type = ($btn.attr('type') || '').toLowerCase()
          const className = ($btn.attr('class') || '').toLowerCase()
          const id = ($btn.attr('id') || '').toLowerCase()
          
          // Buscar por botão de login primeiro
          if (text === 'entrar' || text === 'login' || text === 'sign in' ||
              text.includes('entrar') || text.includes('login') ||
              value === 'entrar' || value === 'login' || value.includes('entrar') || value.includes('login') ||
              className.includes('login') || className.includes('entrar') ||
              id.includes('login') || id.includes('entrar')) {
            confirmButton = $btn
            cy.log(`✅ Botão de login encontrado na tela de TOTP: texto="${text}", value="${value}"`)
            break
          }
        }
        
        // Se não encontrou botão de login, buscar por botões de confirmação/verificação
        if (!confirmButton || confirmButton.length === 0) {
          cy.log('⚠️ Botão de login não encontrado, buscando por botões de confirmação...')
          for (let i = 0; i < buttons.length && (!confirmButton || confirmButton.length === 0); i++) {
            const $btn = Cypress.$(buttons[i])
            const text = $btn.text().toLowerCase().trim()
            const value = ($btn.attr('value') || '').toLowerCase()
            const type = ($btn.attr('type') || '').toLowerCase()
            const className = ($btn.attr('class') || '').toLowerCase()
            
            if (text.includes('confirmar') || text.includes('verificar') || text.includes('enviar') ||
                text.includes('continuar') || text.includes('próximo') || text.includes('next') ||
                value.includes('confirmar') || value.includes('verificar') || value.includes('enviar') ||
                type === 'submit' || className.includes('submit') || className.includes('confirm')) {
              confirmButton = $btn
              cy.log(`✅ Botão de confirmação encontrado: texto="${text}", value="${value}"`)
              break
            }
          }
        }
        
        if (confirmButton && confirmButton.length > 0) {
          cy.wrap(confirmButton).scrollIntoView({ duration: 500 })
          cy.wait(500)
          cy.wrap(confirmButton).click({ force: true })
          cy.log('✅ Botão clicado (login ou confirmação)')
        } else {
          cy.log('⚠️ Botão de login/confirmação não encontrado, verificando se está na tela de TOTP...')
          cy.get('body').then(($bodyFinal) => {
            const bodyText = $bodyFinal.text().toLowerCase()
            const hasTotpElements = $bodyFinal.find('input[type="text"]').length > 0
            
            // Verificar se está na tela de TOTP antes de usar submit genérico
            if (bodyText.includes('código') || bodyText.includes('code') || bodyText.includes('2fa') || 
                bodyText.includes('totp') || bodyText.includes('autenticação') || hasTotpElements) {
              cy.log('⚠️ Está na tela de TOTP mas botão não encontrado, tentando submit genérico...')
              const submitButtons = $bodyFinal.find('button[type="submit"], input[type="submit"]')
              if (submitButtons.length > 0) {
                cy.wrap(submitButtons.first()).scrollIntoView()
                cy.wait(500)
                cy.wrap(submitButtons.first()).click({ force: true })
                cy.log('✅ Botão submit genérico clicado')
              } else {
                cy.log('❌ Nenhum botão de submit encontrado')
              }
            } else {
              cy.log('⚠️ Não parece estar na tela de TOTP')
            }
          })
        }
      })
    } else {
      cy.log('ℹ️ Campo de 2FA não detectado, pode não ser necessário')
    }
  })
  
  // Aguardar login completar e verificar se saiu da tela de login
  cy.wait(5000)
  
  // Verificar se o login foi bem-sucedido
  cy.url().then((url) => {
    cy.log(`URL após login: ${url}`)
    
    // Verificar se não está mais na página de login
    if (!url.includes('login') && !url.includes('auth') && !url.includes('signin')) {
      cy.log('✅ Login realizado com sucesso!')
      
      // Verificar se há elementos indicando que está logado
      cy.get('body', { timeout: 10000 }).then(($body) => {
        const loggedIndicators = $body.find('[class*="user"], [class*="profile"], [class*="logout"], [class*="sair"], [id*="user"], [id*="profile"]')
        const bodyText = $body.text().toLowerCase()
        
        if (loggedIndicators.length > 0 || bodyText.includes('sair') || bodyText.includes('logout')) {
          cy.log('✅ Confirmação: Usuário está logado')
        } else {
          cy.log('ℹ️ Login pode ter sido realizado, mas indicadores não encontrados')
        }
      })
    } else {
      cy.log('⚠️ Ainda na página de login, pode ter havido algum problema')
      
      // Aguardar mais um pouco e verificar novamente
      cy.wait(3000)
      cy.url().then((url2) => {
        if (!url2.includes('login') && !url2.includes('auth')) {
          cy.log('✅ Login completado após aguardar mais tempo')
        }
      })
    }
  })
})
