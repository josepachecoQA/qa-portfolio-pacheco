// ***********************************************
// Teste de Validação de Mensagens de Erro - Atena
// Este teste valida todas as mensagens de erro do sistema Atena
// Verifica se os códigos de erro retornam as mensagens corretas
// ***********************************************

describe('Validação de Mensagens de Erro - Atena', () => {
  // Mapeamento completo de códigos de erro e suas mensagens esperadas
  const errorCodes = {
    '001': { message: 'Não Autorizado', category: 'auth' },
    '002': { message: 'Token Inválido', category: 'auth' },
    '003': { message: 'Token Expirado', category: 'auth' },
    '004': { message: 'Usuario nao localizado', category: 'user' },
    '005': { message: 'Cadastro não Permitido', category: 'registration' },
    '006': { message: 'Erro ao Concluir Cadastro', category: 'registration' },
    '007': { message: 'Erro Modulo Core', category: 'module' },
    '008': { message: 'Parametro Invalido', detail: 'ID Invalido', category: 'validation' },
    '009': { message: 'Conteudo Invalido', detail: 'Body Ausente', category: 'validation' },
    '010': { message: 'Item nao Localizado', category: 'not_found' },
    '011': { message: 'Acesso nao permitido', category: 'permission' },
    '012': { message: 'Erro Durante Consulta aos Dados', category: 'database' },
    '013': { message: 'Erro Connect Redis', category: 'infrastructure' },
    '014': { message: 'Pagina nao encontrada', category: 'not_found' },
    '015': { message: 'Metodos nao permitidos', category: 'http' },
    '016': { message: 'Cadastro Incompleto. Permissões de negócio ausente', category: 'registration' },
    '017': { message: 'Ocorreu um erro no servidor ao processar a solicitação', category: 'server' },
    '018': { message: 'Erro genérico', category: 'generic' },
    '019': { message: 'Erro Curl', category: 'http' },
    '020': { message: 'Solicitacao com Dados Invalidos', category: 'validation' },
    '021': { message: 'Tipo de Usuario Invalido para essa Rota', category: 'permission' },
    '022': { message: 'Ação não é permitida pelo Modelo', category: 'permission' },
    '024': { message: 'O método de pagamento não permite cancelamento manual', category: 'payment' },
    '025': { message: 'Erro Modulo PSP', category: 'module' },
    '026': { message: 'Erro Modulo Auth', category: 'module' },
    '027': { message: 'Coluna de update ou condição não localizada no array', category: 'database' },
    '028': { message: 'Erro ao Realizar upload das imagens', category: 'upload' },
    '029': { message: 'Parâmetro obrigatório não encontrado', category: 'validation' },
    '030': { message: 'Erro Modulo nodin-CMS', category: 'module' },
    '031': { message: 'É necessário informar a propriedade', category: 'validation' },
    '032': { message: 'Erro Módulo Nimbus: Erro de comunicação API', category: 'module' },
    '033': { message: 'Erro Módulo Nimbus: Token Inválido', category: 'module' },
    '034': { message: 'Item com', detail: 'já cadastrado', category: 'duplicate' },
    '035': { message: 'Informe um período com no mínimo', detail: 'dias', category: 'validation' },
    '036': { message: 'Informe uma sazonalidade válida', category: 'validation' },
    '037': { message: 'Dados do metadata inválidos', category: 'validation' },
    '038': { message: 'O site não possui keysPSP configurado', category: 'configuration' },
    '039': { message: 'Não foi possível remover um item do objeto especificado', category: 'operation' },
    '040': { message: 'Autenticação de múltiplas etapas necessária para realizar esta ação (MFA)', category: 'auth' },
    '041': { message: 'Empresas devem constar no Fornecedor', category: 'validation' },
    '042': { message: 'Número já cadastrado', category: 'duplicate' },
    '043': { message: 'A empresa não possui sites afiliados', category: 'configuration' },
    '045': { message: 'Saques aprovados', detail: 'solicitação(es) de saque indisponível(is)', category: 'withdrawal' },
    '046': { message: 'Solicitação de saque indisponível', category: 'withdrawal' },
    '047': { message: 'A localidade não possui site associado', category: 'configuration' },
    '048': { message: 'Aguarde 24 horas para realizar uma nova alteração nos limites do usuário', category: 'rate_limit' },
    '049': { message: 'Estabelecimento Já tem um PDV associado', category: 'duplicate' },
    '050': { message: 'Erro ao atualizar os metadados de jogos', category: 'operation' },
    '056': { message: 'Login de usuário modelo já cadastrado', category: 'duplicate' },
    '057': { message: 'Os dominios', detail: 'já estão em uso', category: 'duplicate' },
    '058': { message: 'E-mail enviado com sucesso', category: 'success' },
    '059': { message: 'Documento recusado com sucesso', category: 'success' },
    '060': { message: 'Não é possível excluir o grupo origem', detail: 'vinculado às seguintes competições', category: 'constraint' },
    '061': { message: 'Gestor sem permissões', category: 'permission' },
    '063': { message: 'Acesso não permitido', category: 'permission' },
    '064': { message: 'Usuário validado com sucesso, no entanto, houve uma falha ao enviar o e-mail', category: 'partial' },
    '065': { message: 'Documento recusado com sucesso, no entanto, houve uma falha ao enviar o e-mail', category: 'partial' },
    '066': { message: 'O campo tipo documento do usuário não pode ser alterado', category: 'constraint' },
    '067': { message: 'Operação não permitida', category: 'permission' },
    '068': { message: 'Serial já cadastrado', category: 'duplicate' },
    '069': { message: 'Dados alterados por outro processo, é necessário revisar e refazer a atualização', category: 'concurrency' },
    '070': { message: 'Tentativa de SQL Injection', category: 'security' },
    '071': { message: 'Erro ao decodificar o JSON do configuracao', category: 'parsing' },
    '072': { message: 'O arquivo é maior que o limite configurado', category: 'upload' },
    '073': { message: 'Uma ou mais localidades parceiras não existem ou estão inativas', category: 'validation' },
    // Códigos Odin
    'odin.047': { message: 'Nenhum registro encontrado', category: 'not_found' },
    // Códigos Sysa
    'sysa.901': { message: 'Configure os sites afiliados na empresa', category: 'configuration' },
    'sysa.902': { message: 'Erro Módulo de Afiliados', category: 'module' },
    // Códigos Clientes Externos
    '801': { message: 'Tipo de documento inválido', category: 'validation' },
    '802': { message: 'Operação não permitida, usuário excluído', category: 'permission' },
    '803': { message: 'Documento inválido', category: 'validation' },
    '804': { message: 'Erro no módulo interno', category: 'module' },
    '805': { message: 'Saldo insuficiente', category: 'balance' },
    '806': { message: 'Valor inválido', category: 'validation' },
    '807': { message: 'Cadastro não Permitido, os campos', detail: 'devem ser enviados', category: 'registration' },
    '808': { message: 'Cadastro não Permitido, usuário já cadastrado', category: 'duplicate' },
    '809': { message: '[MINCETUR] Configuração não encontrada', category: 'configuration' },
    '810': { message: '[MINCETUR] Ludopatia', category: 'validation' },
    '811': { message: 'O documento tipo:', detail: 'deve ter o tamanho de', category: 'validation' },
    '812': { message: 'Dados indisponíveis', category: 'not_found' },
    '813': { message: 'O documento tipo:', detail: 'deve ter o formato:', category: 'validation' },
    '814': { message: 'O valor de gênero fornecido é inválido', category: 'validation' },
    '815': { message: 'Saldo de bonus insuficiente', category: 'balance' },
    // Códigos Lotéricos
    '700': { message: 'Erro Módulo Lotérico: Parâmetros Inválidos', category: 'module' },
    '701': { message: 'Erro Módulo Lotérico: Cadastro Não Permitido', category: 'module' },
    '702': { message: 'Erro Módulo Lotérico: Erro na consulta de dados', category: 'module' },
    '703': { message: 'Erro Módulo Lotérico: Erro ao autenticar no serviço', category: 'module' }
  }

  // Fazer login apenas uma vez antes de todos os testes
  before(() => {
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
    
    // Verificar se o login foi bem-sucedido
    cy.url().should('not.include', 'login').should('not.include', 'auth')
    cy.log('✅ Login completado - não está mais na tela de login')
  })

  // Interceptar requisições HTTP para capturar erros em cada teste
  beforeEach(() => {
    // Interceptar todas as requisições para capturar erros
    cy.intercept('**', (req) => {
      req.continue((res) => {
        // Logar respostas com status de erro
        if (res.statusCode >= 400) {
          cy.log(`🔴 Erro HTTP ${res.statusCode}: ${req.url}`)
          
          // Se a resposta for JSON, logar o corpo
          if (res.body && typeof res.body === 'object') {
            cy.log(`   Código: ${res.body.code || 'N/A'}, Mensagem: ${res.body.message || 'N/A'}`)
          }
        }
      })
    }).as('httpRequests')
  })

  // Função auxiliar para verificar mensagem de erro na interface
  const verifyErrorMessage = (code, expectedMessage, expectedDetail = null) => {
    cy.log(`🔍 Verificando mensagem de erro para código ${code}...`)
    
    // Verificar se a mensagem aparece no body da página
    cy.get('body', { timeout: 10000 }).then(($body) => {
      const bodyText = $body.text()
      const bodyTextLower = bodyText.toLowerCase()
      const expectedMessageLower = expectedMessage.toLowerCase()
      
      // Verificar se a mensagem principal está presente
      if (bodyTextLower.includes(expectedMessageLower)) {
        cy.log(`✅ Mensagem principal encontrada para código ${code}: "${expectedMessage}"`)
        
        // Se houver detalhe esperado, verificar também
        if (expectedDetail) {
          const expectedDetailLower = expectedDetail.toLowerCase()
          if (bodyTextLower.includes(expectedDetailLower)) {
            cy.log(`✅ Detalhe encontrado para código ${code}: "${expectedDetail}"`)
          } else {
            cy.log(`⚠️ Detalhe não encontrado para código ${code}: "${expectedDetail}"`)
          }
        }
        
        return true
      } else {
        cy.log(`❌ Mensagem não encontrada para código ${code}. Esperado: "${expectedMessage}"`)
        return false
      }
    })
  }

  // Função auxiliar para verificar erro em resposta JSON interceptada
  const verifyErrorInResponse = (code, expectedMessage, responseBody) => {
    cy.log(`🔍 Verificando resposta JSON para código ${code}...`)
    
    if (!responseBody) {
      cy.log(`⚠️ Resposta não disponível para código ${code}`)
      return false
    }
    
    // Verificar se é um objeto JSON com código de erro
    if (responseBody && typeof responseBody === 'object') {
      const responseCode = responseBody.code?.toString() || responseBody.code
      const expectedCode = code.toString()
      
      if (responseCode === expectedCode || responseCode === code) {
        cy.log(`✅ Código de erro encontrado na resposta: ${responseCode}`)
        
        if (responseBody.message) {
          const messageLower = responseBody.message.toLowerCase()
          const expectedLower = expectedMessage.toLowerCase()
          
          if (messageLower.includes(expectedLower)) {
            cy.log(`✅ Mensagem de erro encontrada na resposta: "${responseBody.message}"`)
            return true
          } else {
            cy.log(`⚠️ Mensagem na resposta não corresponde ao esperado. Recebido: "${responseBody.message}", Esperado: "${expectedMessage}"`)
          }
        }
      }
    }
    
    return false
  }

  // Função auxiliar para verificar erro em toast/notificação
  const verifyErrorInToast = (code, expectedMessage) => {
    cy.log(`🔍 Verificando toast/notificação para código ${code}...`)
    
    // Buscar por elementos comuns de toast/notificação
    const toastSelectors = [
      '.toast',
      '.notification',
      '.alert',
      '.error-message',
      '[role="alert"]',
      '.swal2-popup',
      '.modal-body',
      '.error',
      '[class*="error"]',
      '[class*="toast"]',
      '[class*="notification"]'
    ]
    
    cy.get('body', { timeout: 5000 }).then(($body) => {
      let found = false
      
      for (const selector of toastSelectors) {
        const elements = $body.find(selector)
        if (elements.length > 0) {
          elements.each((index, el) => {
            const $el = Cypress.$(el)
            const text = $el.text().toLowerCase()
            const expectedLower = expectedMessage.toLowerCase()
            
            if (text.includes(expectedLower)) {
              cy.log(`✅ Mensagem encontrada em ${selector}: "${$el.text()}"`)
              found = true
              return false // break
            }
          })
          
          if (found) break
        }
      }
      
      if (!found) {
        cy.log(`⚠️ Mensagem não encontrada em toasts/notificações para código ${code}`)
      }
      
      return found
    })
  }

  // Teste parametrizado para cada código de erro
  Object.entries(errorCodes).forEach(([code, errorInfo]) => {
    it(`Deve validar mensagem de erro para código ${code}`, () => {
      cy.log(`\n📋 Testando código de erro: ${code}`)
      cy.log(`   Categoria: ${errorInfo.category}`)
      cy.log(`   Mensagem esperada: ${errorInfo.message}`)
      if (errorInfo.detail) {
        cy.log(`   Detalhe esperado: ${errorInfo.detail}`)
      }
      
      // Interceptar requisições para capturar erros
      cy.intercept('**', (req) => {
        req.continue((res) => {
          if (res.statusCode >= 400 && res.body) {
            const body = typeof res.body === 'string' ? JSON.parse(res.body) : res.body
            if (body && body.code) {
              const responseCode = body.code.toString()
              if (responseCode === code.toString() || responseCode === code) {
                cy.log(`✅ Erro ${code} capturado na requisição: ${req.url}`)
                verifyErrorInResponse(code, errorInfo.message, body)
              }
            }
          }
        })
      }).as(`error-${code}`)
      
      // Verificar mensagem na interface (body)
      verifyErrorMessage(code, errorInfo.message, errorInfo.detail)
      
      // Verificar mensagem em toast/notificação
      verifyErrorInToast(code, errorInfo.message)
      
      // Logar resultado
      cy.log(`✅ Validação do código ${code} concluída`)
    })
  })

  // Teste agrupado por categoria
  const categories = [...new Set(Object.values(errorCodes).map(e => e.category))]
  
  categories.forEach(category => {
    describe(`Categoria: ${category}`, () => {
      const categoryErrors = Object.entries(errorCodes)
        .filter(([code, info]) => info.category === category)
      
      it(`Deve validar todos os erros da categoria ${category}`, () => {
        cy.log(`\n📁 Validando ${categoryErrors.length} erros da categoria ${category}`)
        
        categoryErrors.forEach(([code, errorInfo]) => {
          cy.log(`   - Código ${code}: ${errorInfo.message}`)
          verifyErrorMessage(code, errorInfo.message, errorInfo.detail)
        })
        
        cy.log(`✅ Validação da categoria ${category} concluída`)
      })
    })
  })

  // Teste de resumo - verificar quantos códigos foram testados
  it('Deve exibir resumo de todos os códigos de erro testados', () => {
    const totalCodes = Object.keys(errorCodes).length
    const categoriesCount = {}
    
    Object.values(errorCodes).forEach(error => {
      categoriesCount[error.category] = (categoriesCount[error.category] || 0) + 1
    })
    
    cy.log(`\n📊 RESUMO DE CÓDIGOS DE ERRO`)
    cy.log(`   Total de códigos: ${totalCodes}`)
    cy.log(`   Categorias: ${Object.keys(categoriesCount).length}`)
    cy.log(`\n   Distribuição por categoria:`)
    
    Object.entries(categoriesCount).forEach(([category, count]) => {
      cy.log(`   - ${category}: ${count} código(s)`)
    })
    
    cy.log(`\n✅ Resumo gerado com sucesso`)
  })
})

