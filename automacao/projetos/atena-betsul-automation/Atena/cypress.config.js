const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    baseUrl: 'https://gestor-dev.sportingplay.info',
    viewportWidth: 1920,
    viewportHeight: 1080,
    defaultCommandTimeout: 15000,
    requestTimeout: 15000,
    responseTimeout: 15000,
    pageLoadTimeout: 60000,
    video: true,
    screenshotOnRunFailure: true,
    chromeWebSecurity: false,
    experimentalMemoryManagement: true,
    numTestsKeptInMemory: 1,
    setupNodeEvents(on, config) {
      // implement node event listeners here
      const fs = require('fs')
      const path = require('path')
      
      // Task para ler arquivo se existir (não falha se não existir)
      on('task', {
        readFileIfExists(filePath) {
          const fullPath = path.join(__dirname, filePath)
          if (fs.existsSync(fullPath)) {
            const fileContent = fs.readFileSync(fullPath, 'utf8')
            return JSON.parse(fileContent)
          }
          return null
        }
      })
      
      return config
    },
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    excludeSpecPattern: '*.skip.*',
    supportFile: 'cypress/support/e2e.js',
  },
  env: {
    // Variáveis de ambiente
    USER_EMAIL: 'alexandre.costa@servicenet.com.br',
    USER_PASSWORD: 'Aa@102030',
    TOTP_SECRET: 'CLSUJ5BDR7QPUTSRKPYAI3CNURZWONBJ'
  }
})

