const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    baseUrl: 'https://www.betsul.online',
    viewportWidth: 1920,
    viewportHeight: 1080,
    defaultCommandTimeout: 15000,
    requestTimeout: 15000,
    responseTimeout: 15000,
    pageLoadTimeout: 60000,
    video: true,
    screenshotOnRunFailure: true,
    chromeWebSecurity: false, // Desabilitar segurança web do Chrome para contornar CORS e Cloudflare
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    excludeSpecPattern: '*.skip.*',
    supportFile: 'cypress/support/e2e.js',
  },
  env: {
    // Variáveis de ambiente podem ser adicionadas aqui
  }
})

