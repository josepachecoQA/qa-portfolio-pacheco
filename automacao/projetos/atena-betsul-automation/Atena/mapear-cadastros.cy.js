// ***********************************************
// Mapeamento de Formulários de Cadastro no Atena
// Este teste faz login, navega pelo sistema e mapeia
// todas as telas que contêm formulários de cadastro
// ***********************************************

const fs = require('fs')
const path = require('path')

describe('Mapeamento de Formulários de Cadastro - Atena', () => {
  let mapeamento = {
    sistema: 'Atena',
    url: 'https://gestor-dev.sportingplay.info',
    dataMapeamento: new Date().toISOString(),
    telas: []
  }

  beforeEach(() => {
    // Acessar a página inicial
    cy.visit('/', {
      timeout: 60000,
      failOnStatusCode: false
    })
    
    cy.get('body', { timeout: 10000 }).should('be.visible')
    cy.closeModals()
  })

  it('Deve fazer login e mapear todas as telas com formulários de cadastro', () => {
    cy.log('🔍 Iniciando mapeamento de formulários de cadastro...')
    
    // Fazer login
    cy.loginAtena()
    
    // Aguardar um pouco para garantir que está logado
    cy.wait(3000)
    
    // Verificar se está logado
    cy.url().then((url) => {
      cy.log(`URL após login: ${url}`)
      
      // Mapear página inicial
      mapearTelaAtual('Página Inicial (Após Login)')
      
      // Buscar links de cadastro no menu
      cy.get('body').then(($body) => {
        cy.log('🔍 Buscando links de cadastro...')
        
        // Buscar por links que podem indicar cadastros
        const palavrasChave = [
          'cadastr', 'cadastro', 'novo', 'criar', 'adicionar', 'incluir',
          'registr', 'registro', 'inserir', 'adicion', 'create', 'new'
        ]
        
        const links = $body.find('a, button, [role="button"]')
        const linksEncontrados = []
        
        links.each((index, el) => {
          const $el = Cypress.$(el)
          const text = $el.text().toLowerCase()
          const href = ($el.attr('href') || '').toLowerCase()
          const title = ($el.attr('title') || '').toLowerCase()
          const ariaLabel = ($el.attr('aria-label') || '').toLowerCase()
          
          // Verificar se contém palavras-chave
          for (const palavra of palavrasChave) {
            if (text.includes(palavra) || href.includes(palavra) || 
                title.includes(palavra) || ariaLabel.includes(palavra)) {
              const linkInfo = {
                texto: $el.text().trim(),
                href: $el.attr('href') || '',
                type: $el.prop('tagName'),
                encontradoPor: palavra
              }
              
              // Verificar se já não foi adicionado
              if (!linksEncontrados.some(l => l.href === linkInfo.href && l.texto === linkInfo.texto)) {
                linksEncontrados.push(linkInfo)
              }
              break
            }
          }
        })
        
        cy.log(`✅ Encontrados ${linksEncontrados.length} links relacionados a cadastro`)
        
        // Visitar cada link encontrado
        linksEncontrados.forEach((link, index) => {
          if (link.href && link.href.startsWith('http') || link.href.startsWith('/')) {
            cy.log(`📄 Mapeando: ${link.texto || link.href}`)
            
            // Visitar o link
            if (link.href.startsWith('http')) {
              cy.visit(link.href, { timeout: 60000, failOnStatusCode: false })
            } else {
              cy.visit(link.href, { timeout: 60000, failOnStatusCode: false })
            }
            
            cy.wait(3000)
            cy.get('body', { timeout: 10000 }).should('be.visible')
            cy.closeModals()
            
            // Mapear a tela
            cy.url().then((currentUrl) => {
              mapearTelaAtual(link.texto || `Tela ${index + 1}`, currentUrl)
            })
            
            // Voltar para página inicial para continuar navegação
            cy.visit('/', { timeout: 60000, failOnStatusCode: false })
            cy.wait(2000)
            cy.closeModals()
          }
        })
      })
      
      // Buscar também por menus e navegação
      cy.log('🔍 Buscando menus e navegação...')
      cy.get('body').then(($body) => {
        const menus = $body.find('nav, [role="navigation"], [class*="menu"], [class*="nav"], [class*="sidebar"]')
        
        if (menus.length > 0) {
          cy.log(`✅ Encontrados ${menus.length} elementos de menu/navegação`)
          
          // Extrair links dos menus
          menus.each((index, menu) => {
            const $menu = Cypress.$(menu)
            const menuLinks = $menu.find('a')
            
            menuLinks.each((idx, link) => {
              const $link = Cypress.$(link)
              const text = $link.text().toLowerCase()
              const href = $link.attr('href') || ''
              
              // Verificar se é um link de cadastro
              if (text.includes('cadastr') || text.includes('novo') || text.includes('criar') || 
                  text.includes('adicionar') || href.includes('cadastr') || href.includes('create') || 
                  href.includes('new')) {
                
                cy.log(`📄 Link de menu encontrado: ${$link.text().trim()}`)
                
                if (href && (href.startsWith('http') || href.startsWith('/'))) {
                  cy.visit(href, { timeout: 60000, failOnStatusCode: false })
                  cy.wait(3000)
                  cy.get('body', { timeout: 10000 }).should('be.visible')
                  cy.closeModals()
                  
                  cy.url().then((currentUrl) => {
                    mapearTelaAtual($link.text().trim(), currentUrl)
                  })
                  
                  // Voltar
                  cy.visit('/', { timeout: 60000, failOnStatusCode: false })
                  cy.wait(2000)
                  cy.closeModals()
                }
              }
            })
          })
        }
      })
    })
    
    // Gerar documento de mapeamento
    gerarDocumentoMapeamento()
  })

  function mapearTelaAtual(nomeTela, url = null) {
    cy.url().then((currentUrl) => {
      const urlFinal = url || currentUrl
      
      cy.get('body').then(($body) => {
        // Buscar formulários
        const forms = $body.find('form')
        const formCount = forms.length
        
        // Buscar campos de formulário
        const inputs = $body.find('input, textarea, select')
        const inputCount = inputs.length
        
        // Identificar tipos de campos
        const tiposCampos = {
          input: $body.find('input').length,
          textarea: $body.find('textarea').length,
          select: $body.find('select').length,
          button: $body.find('button').length,
          submit: $body.find('input[type="submit"], button[type="submit"]').length
        }
        
        // Extrair informações dos campos
        const camposInfo = []
        inputs.slice(0, 50).each((index, input) => {
          const $input = Cypress.$(input)
          const type = $input.attr('type') || 'text'
          const name = $input.attr('name') || ''
          const id = $input.attr('id') || ''
          const placeholder = $input.attr('placeholder') || ''
          const label = $input.closest('label').text() || ''
          
          camposInfo.push({
            tipo: type || $input.prop('tagName').toLowerCase(),
            nome: name || id || `campo_${index + 1}`,
            placeholder: placeholder,
            label: label.trim()
          })
        })
        
        // Verificar se há botões de ação (salvar, criar, etc)
        const botoesAcao = []
        const buttons = $body.find('button, input[type="submit"], input[type="button"]')
        
        buttons.slice(0, 20).each((index, btn) => {
          const $btn = Cypress.$(btn)
          const text = $btn.text().toLowerCase()
          const value = ($btn.attr('value') || '').toLowerCase()
          
          if (text.includes('salvar') || text.includes('criar') || text.includes('cadastrar') ||
              text.includes('adicionar') || text.includes('enviar') || text.includes('submit') ||
              value.includes('salvar') || value.includes('criar') || value.includes('cadastrar')) {
            botoesAcao.push({
              texto: $btn.text().trim() || $btn.attr('value') || '',
              tipo: $btn.prop('tagName').toLowerCase()
            })
          }
        })
        
        const telaInfo = {
          nome: nomeTela,
          url: urlFinal,
          temFormulario: formCount > 0,
          quantidadeFormularios: formCount,
          quantidadeCampos: inputCount,
          tiposCampos: tiposCampos,
          campos: camposInfo.slice(0, 30), // Limitar a 30 campos por tela
          botoesAcao: botoesAcao,
          timestamp: new Date().toISOString()
        }
        
        // Verificar se a tela já foi mapeada
        const jaMapeada = mapeamento.telas.some(t => t.url === telaInfo.url)
        if (!jaMapeada) {
          mapeamento.telas.push(telaInfo)
          cy.log(`✅ Tela mapeada: ${nomeTela} - ${formCount} formulário(s) - ${inputCount} campo(s)`)
        }
      })
    })
  }

  function gerarDocumentoMapeamento() {
    cy.then(() => {
      const totalTelas = mapeamento.telas.length
      const totalFormularios = mapeamento.telas.reduce((sum, tela) => sum + tela.quantidadeFormularios, 0)
      const totalCampos = mapeamento.telas.reduce((sum, tela) => sum + tela.quantidadeCampos, 0)
      
      let documento = `# Mapeamento de Formulários de Cadastro - Atena\n\n`
      documento += `**Data do Mapeamento:** ${new Date(mapeamento.dataMapeamento).toLocaleString('pt-BR')}\n\n`
      documento += `**URL Base:** ${mapeamento.url}\n\n`
      documento += `**Total de Telas Mapeadas:** ${totalTelas}\n\n`
      documento += `**Total de Formulários:** ${totalFormularios}\n\n`
      documento += `**Total de Campos:** ${totalCampos}\n\n`
      documento += `---\n\n`
      
      // Listar cada tela
      mapeamento.telas.forEach((tela, index) => {
        documento += `## ${index + 1}. ${tela.nome}\n\n`
        documento += `**URL:** [${tela.url}](${tela.url})\n\n`
        documento += `**Tem formulário:** ${tela.temFormulario ? 'Sim' : 'Não'}\n\n`
        documento += `**Quantidade de formulários:** ${tela.quantidadeFormularios}\n\n`
        documento += `**Quantidade de campos:** ${tela.quantidadeCampos}\n\n`
        
        if (Object.keys(tela.tiposCampos).length > 0) {
          documento += `**Tipos de campos:**\n`
          Object.entries(tela.tiposCampos).forEach(([tipo, quantidade]) => {
            if (quantidade > 0) {
              documento += `- ${tipo}: ${quantidade}\n`
            }
          })
          documento += `\n`
        }
        
        if (tela.campos.length > 0) {
          documento += `**Campos identificados:**\n`
          tela.campos.slice(0, 20).forEach((campo, idx) => {
            documento += `${idx + 1}. **${campo.nome}** (${campo.tipo})`
            if (campo.label) documento += ` - Label: ${campo.label}`
            if (campo.placeholder) documento += ` - Placeholder: ${campo.placeholder}`
            documento += `\n`
          })
          documento += `\n`
        }
        
        if (tela.botoesAcao.length > 0) {
          documento += `**Botões de ação:**\n`
          tela.botoesAcao.forEach((botao, idx) => {
            documento += `${idx + 1}. ${botao.texto} (${botao.tipo})\n`
          })
          documento += `\n`
        }
        
        documento += `---\n\n`
      })
      
      // Resumo
      documento += `## Resumo\n\n`
      documento += `- Total de telas mapeadas: ${totalTelas}\n`
      documento += `- Total de formulários: ${totalFormularios}\n`
      documento += `- Total de campos: ${totalCampos}\n`
      documento += `- Telas com formulários: ${mapeamento.telas.filter(t => t.temFormulario).length}\n`
      
      // Salvar documento
      const caminhoArquivo = path.join(__dirname, '..', '..', 'mapeamento-cadastros.md')
      
      cy.writeFile(caminhoArquivo, documento).then(() => {
        cy.log(`✅ Documento de mapeamento gerado: ${caminhoArquivo}`)
        cy.log(`📊 Total de telas mapeadas: ${totalTelas}`)
        cy.log(`📋 Total de formulários: ${totalFormularios}`)
        cy.log(`📝 Total de campos: ${totalCampos}`)
      })
    })
  }
})
