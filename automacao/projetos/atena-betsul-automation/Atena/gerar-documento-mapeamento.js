// Script para gerar documento de mapeamento a partir do JSON
const fs = require('fs')
const path = require('path')

const mapeamento = require('./mapeamento_atena.json')

function gerarDocumento() {
  let documento = `# Mapeamento de Formulários de Cadastro - Atena\n\n`
  
  documento += `**Sistema:** ${mapeamento.sistema}\n\n`
  documento += `**Data do Mapeamento:** ${new Date().toLocaleString('pt-BR')}\n\n`
  documento += `**URL Base:** https://gestor-dev.sportingplay.info\n\n`
  
  // Calcular estatísticas
  let totalTelas = 0
  let totalModulos = mapeamento.roteiro_cadastros.length
  
  mapeamento.roteiro_cadastros.forEach(modulo => {
    totalTelas += modulo.telas.length
  })
  
  documento += `**Total de Módulos:** ${totalModulos}\n\n`
  documento += `**Total de Telas com Formulários:** ${totalTelas}\n\n`
  documento += `---\n\n`
  
  // Gerar conteúdo por módulo
  mapeamento.roteiro_cadastros.forEach((modulo, modIndex) => {
    documento += `## Módulo: ${modulo.modulo}\n\n`
    
    modulo.telas.forEach((tela, telaIndex) => {
      const numeroTela = `${modIndex + 1}.${telaIndex + 1}`
      
      documento += `### ${numeroTela} ${tela.nome}\n\n`
      documento += `**Caminho de Navegação:** ${tela.caminho}\n\n`
      
      // Campos do formulário
      if (tela.campos && tela.campos.length > 0) {
        documento += `**Campos do Formulário:**\n\n`
        tela.campos.forEach((campo, index) => {
          documento += `${index + 1}. \`${campo}\`\n`
        })
        documento += `\n`
      }
      
      // Ações disponíveis
      if (tela.acoes && tela.acoes.length > 0) {
        documento += `**Ações Disponíveis:**\n\n`
        tela.acoes.forEach((acao, index) => {
          documento += `${index + 1}. ${acao.replace(/_/g, ' ')}\n`
        })
        documento += `\n`
      }
      
      // Dependências
      if (tela.dependencias && tela.dependencias.length > 0) {
        documento += `**Dependências e Observações:**\n\n`
        tela.dependencias.forEach((dep, index) => {
          documento += `${index + 1}. ${dep}\n`
        })
        documento += `\n`
      }
      
      documento += `---\n\n`
    })
  })
  
  // Resumo geral
  documento += `## Resumo Geral\n\n`
  documento += `### Estatísticas por Módulo\n\n`
  
  mapeamento.roteiro_cadastros.forEach(modulo => {
    documento += `- **${modulo.modulo}:** ${modulo.telas.length} tela(s) com formulário\n`
  })
  
  documento += `\n### Total de Campos por Módulo\n\n`
  
  mapeamento.roteiro_cadastros.forEach(modulo => {
    let totalCampos = 0
    modulo.telas.forEach(tela => {
      if (tela.campos) {
        totalCampos += tela.campos.length
      }
    })
    documento += `- **${modulo.modulo}:** ${totalCampos} campo(s)\n`
  })
  
  documento += `\n### Total de Ações por Módulo\n\n`
  
  mapeamento.roteiro_cadastros.forEach(modulo => {
    let totalAcoes = 0
    modulo.telas.forEach(tela => {
      if (tela.acoes) {
        totalAcoes += tela.acoes.length
      }
    })
    documento += `- **${modulo.modulo}:** ${totalAcoes} ação(ões)\n`
  })
  
  documento += `\n---\n\n`
  documento += `## Índice de Telas\n\n`
  
  mapeamento.roteiro_cadastros.forEach((modulo, modIndex) => {
    documento += `### ${modulo.modulo}\n\n`
    modulo.telas.forEach((tela, telaIndex) => {
      const numeroTela = `${modIndex + 1}.${telaIndex + 1}`
      documento += `${numeroTela}. [${tela.nome}](#${numeroTela.toLowerCase().replace(/\./g, '')}-${tela.nome.toLowerCase().replace(/\s+/g, '-')}) - ${tela.caminho}\n`
    })
    documento += `\n`
  })
  
  return documento
}

// Gerar e salvar documento
const documento = gerarDocumento()
const caminhoArquivo = path.join(__dirname, 'mapeamento-cadastros-completo.md')

fs.writeFileSync(caminhoArquivo, documento, 'utf8')

console.log('✅ Documento gerado com sucesso!')
console.log(`📄 Arquivo: ${caminhoArquivo}`)
console.log(`📊 Total de módulos: ${mapeamento.roteiro_cadastros.length}`)
console.log(`📋 Total de telas: ${mapeamento.roteiro_cadastros.reduce((sum, mod) => sum + mod.telas.length, 0)}`)

