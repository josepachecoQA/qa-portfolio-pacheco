#!/bin/bash

# Script para configurar e fazer push para o GitLab
# Uso: ./gitlab-setup.sh [nome-do-projeto]

PROJECT_NAME=${1:-"automacao-de-testes"}
GITLAB_URL="https://gitlab.servicenet.com.br"

echo "🚀 Configurando repositório GitLab..."
echo "📦 Nome do projeto: $PROJECT_NAME"
echo "🔗 URL do GitLab: $GITLAB_URL"
echo ""

# Verificar se o remote já existe
if git remote | grep -q "origin"; then
    echo "⚠️  Remote 'origin' já existe. Removendo..."
    git remote remove origin
fi

# Adicionar remote
echo "➕ Adicionando remote GitLab..."
git remote add origin "$GITLAB_URL/$PROJECT_NAME.git"

# Verificar conexão
echo "🔍 Verificando conexão com GitLab..."
git remote -v

echo ""
echo "✅ Remote configurado!"
echo ""
echo "📝 Próximos passos:"
echo "   1. Crie o projeto '$PROJECT_NAME' no GitLab se ainda não existir"
echo "   2. Execute: git push -u origin master"
echo "   ou"
echo "   2. Execute: git push -u origin master --force (se o repositório já existir)"
echo ""

