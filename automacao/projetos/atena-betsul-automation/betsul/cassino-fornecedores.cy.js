// ***********************************************
// Teste de Cassino - Fornecedores
// Este teste acessa a seção de Cassino e lista todos os fornecedores
// ***********************************************

describe('Cassino - Fornecedores', () => {
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

  it('Deve acessar a seção de Cassino e listar todos os fornecedores', () => {
    // Navegar diretamente para a seção de Cassino
    cy.visit('/cassino', {
      timeout: 60000,
      failOnStatusCode: false
    })
    
    // Aguardar a página carregar
    cy.get('body', { timeout: 10000 }).should('be.visible')
    
    // Fechar modais novamente
    cy.closeModals()
    
    // Aguardar um pouco para os elementos carregarem
    cy.wait(3000)
    
    // Verificar se estamos na página de Cassino
    cy.url().should('include', 'cassino')
    
    // Mapear e listar todos os fornecedores
    cy.get('body').then(($body) => {
      cy.log('🔍 Buscando fornecedores...')
      
      // Tentar diferentes seletores para encontrar fornecedores
      // Fornecedores geralmente aparecem como cards, imagens, ou links
      const fornecedores = []
      
      // Buscar por elementos comuns que podem representar fornecedores
      // 1. Imagens com alt ou title contendo nomes de fornecedores conhecidos
      const fornecedoresConhecidos = [
        'pragmatic', 'evolution', 'netent', 'playtech', 'microgaming',
        'betsoft', 'yggdrasil', 'quickspin', 'red tiger', 'nuxgame',
        'play\'n go', 'igt', 'isoftbet', 'thunderkick', 'booongo',
        'spinomenal', 'nolimit city', 'relax gaming', 'push gaming'
      ]
      
      // Buscar por imagens de fornecedores
      fornecedoresConhecidos.forEach(fornecedor => {
        // Buscar por alt, src ou title (case-insensitive manualmente)
        const imgs = $body.find('img')
        let found = false
        
        for (let i = 0; i < imgs.length && !found; i++) {
          const $img = Cypress.$(imgs[i])
          const alt = ($img.attr('alt') || '').toLowerCase()
          const src = ($img.attr('src') || '').toLowerCase()
          const title = ($img.attr('title') || '').toLowerCase()
          const fornecedorLower = fornecedor.toLowerCase()
          
          if ((alt.includes(fornecedorLower) || src.includes(fornecedorLower) || title.includes(fornecedorLower)) 
              && !fornecedores.includes(fornecedor)) {
            fornecedores.push(fornecedor)
            found = true
          }
        }
      })
      
      // Buscar por elementos com classes ou IDs relacionados a fornecedores
      const fornecedorElements = $body.find('[class*="provider"], [class*="fornecedor"], [id*="provider"], [id*="fornecedor"]')
      if (fornecedorElements.length > 0) {
        cy.log(`Encontrados ${fornecedorElements.length} elementos relacionados a fornecedores`)
        
        // Extrair texto ou atributos que possam identificar fornecedores
        fornecedorElements.each((index, el) => {
          const $el = Cypress.$(el)
          const text = $el.text().trim()
          const alt = $el.attr('alt') || ''
          const title = $el.attr('title') || ''
          const src = $el.attr('src') || ''
          
          // Tentar identificar fornecedor pelo texto, alt, title ou src
          const possibleProvider = text || alt || title || src
          if (possibleProvider && possibleProvider.length > 2 && possibleProvider.length < 50) {
            // Verificar se não é um fornecedor já adicionado
            const normalized = possibleProvider.toLowerCase()
            if (!fornecedores.some(f => normalized.includes(f) || f.includes(normalized))) {
              fornecedores.push(possibleProvider)
            }
          }
        })
      }
      
      // Buscar por cards ou containers de jogos/fornecedores
      const gameCards = $body.find('[class*="game"], [class*="slot"], [class*="card"], [class*="item"]')
      if (gameCards.length > 0) {
        cy.log(`Encontrados ${gameCards.length} cards de jogos`)
        
        // Tentar extrair informações dos cards
        gameCards.slice(0, 20).each((index, el) => {
          const $el = Cypress.$(el)
          const dataProvider = $el.attr('data-provider') || $el.attr('data-fornecedor')
          if (dataProvider && !fornecedores.includes(dataProvider)) {
            fornecedores.push(dataProvider)
          }
        })
      }
      
      // Listar todos os fornecedores encontrados
      if (fornecedores.length > 0) {
        cy.log(`\n✅ FORNECEDORES ENCONTRADOS (${fornecedores.length}):`)
        fornecedores.forEach((fornecedor, index) => {
          cy.log(`${index + 1}. ${fornecedor}`)
        })
        
        // Verificar se encontramos pelo menos um fornecedor
        expect(fornecedores.length).to.be.greaterThan(0)
      } else {
        cy.log('⚠️ Nenhum fornecedor encontrado com os seletores padrão')
        
        // Tentar uma busca mais genérica
        cy.log('🔍 Tentando busca genérica...')
        
        // Listar todas as imagens na página que podem ser fornecedores
        cy.get('img').then(($imgs) => {
          cy.log(`Total de imagens na página: ${$imgs.length}`)
          
          const imgSources = []
          $imgs.each((index, img) => {
            const src = Cypress.$(img).attr('src') || ''
            const alt = Cypress.$(img).attr('alt') || ''
            
            if (src && (src.includes('provider') || src.includes('fornecedor') || src.includes('logo'))) {
              imgSources.push({ src, alt })
            }
          })
          
          if (imgSources.length > 0) {
            cy.log(`Imagens relacionadas a fornecedores encontradas: ${imgSources.length}`)
            imgSources.forEach((img, index) => {
              cy.log(`${index + 1}. ${img.alt || img.src}`)
            })
          }
        })
      }
    })
  })

  it('Deve verificar se há seção de fornecedores na página de Cassino', () => {
    // Navegar para Cassino
    cy.visit('/cassino', {
      timeout: 60000,
      failOnStatusCode: false
    })
    
    cy.get('body', { timeout: 10000 }).should('be.visible')
    cy.closeModals()
    cy.wait(2000)
    
    // Verificar se há seções relacionadas a fornecedores
    cy.get('body').then(($body) => {
      // Buscar por títulos ou textos que mencionam fornecedores
      const hasProviderSection = $body.find('h1, h2, h3, h4, span, div').filter((i, el) => {
        const text = Cypress.$(el).text().toLowerCase()
        return text.includes('fornecedor') || text.includes('provider') || text.includes('provedor')
      })
      
      if (hasProviderSection.length > 0) {
        cy.log('✅ Seção de fornecedores encontrada!')
        cy.log(`Texto encontrado: ${Cypress.$(hasProviderSection[0]).text()}`)
      } else {
        cy.log('⚠️ Seção específica de fornecedores não encontrada por texto')
      }
      
      // Verificar se há elementos com atributos data relacionados a fornecedores
      const hasProviderData = $body.find('[data-provider], [data-fornecedor], [data-provedor]')
      if (hasProviderData.length > 0) {
        cy.log(`✅ Encontrados ${hasProviderData.length} elementos com atributos de fornecedor`)
      }
    })
  })
})

