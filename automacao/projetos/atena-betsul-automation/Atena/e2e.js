// ***********************************************************
// Este arquivo é processado e carregado automaticamente antes
// de seus arquivos de teste. Este é um ótimo lugar para colocar
// configuração global e comportamento que modifica o Cypress.
//
// ***********************************************************

// Importar comandos personalizados
require('./commands')

// Comandos personalizados podem ser adicionados aqui
Cypress.Commands.add('login', (email, password) => {
  // Implementar login se necessário
  cy.log('Login command - implementar conforme necessário')
})

// Configurações globais
// Ignorar erros não tratados do JavaScript que podem ocorrer em páginas web
Cypress.on('uncaught:exception', (err, runnable) => {
  // Retornar false para evitar que o Cypress falhe o teste
  // em caso de erros não tratados do JavaScript
  return false
})

