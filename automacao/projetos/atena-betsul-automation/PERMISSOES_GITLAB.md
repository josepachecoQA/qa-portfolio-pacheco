# 👥 Como Dar Permissão para Outras Pessoas no GitLab

## 📋 Método 1: Adicionar Membros ao Projeto (Recomendado)

### Passo a Passo:

1. **Acesse o projeto no GitLab**:
   - URL: https://gitlab.servicenet.com.br/qa/automacao-de-teste
   - Ou navegue até: **Projects** → **Your projects** → **automacao-de-teste**

2. **Vá para as configurações do projeto**:
   - No menu lateral esquerdo, clique em **Settings** → **Members**
   - Ou acesse diretamente: https://gitlab.servicenet.com.br/qa/automacao-de-teste/-/project_members

3. **Adicionar novo membro**:
   - Clique no botão **"Invite members"** ou **"Convidar membros"**
   - No campo **"GitLab member or Email address"**, digite:
     - O **username** do GitLab da pessoa (ex: `joao.silva`)
     - Ou o **email** da pessoa (ex: `joao.silva@servicenet.com.br`)

4. **Selecionar nível de permissão**:
   - Escolha uma das opções abaixo conforme necessário

5. **Definir data de expiração (opcional)**:
   - Se quiser que o acesso expire em uma data específica

6. **Clique em "Invite"** ou **"Convidar"**

## 🔐 Níveis de Permissão no GitLab

### **Guest** (Convidado)
- ✅ Pode visualizar o projeto
- ✅ Pode criar issues
- ✅ Pode comentar em issues e merge requests
- ❌ Não pode fazer push de código
- ❌ Não pode criar branches

### **Reporter** (Repórter)
- ✅ Todas as permissões de Guest
- ✅ Pode visualizar código
- ✅ Pode fazer download do código
- ✅ Pode visualizar CI/CD pipelines
- ❌ Não pode fazer push de código
- ❌ Não pode criar branches

### **Developer** (Desenvolvedor)
- ✅ Todas as permissões de Reporter
- ✅ Pode fazer push para branches não protegidas
- ✅ Pode criar branches
- ✅ Pode criar merge requests
- ✅ Pode criar tags
- ✅ Pode executar CI/CD pipelines
- ❌ Não pode fazer push para branch `main` (se protegida)
- ❌ Não pode deletar branches protegidas
- ❌ Não pode fazer merge de merge requests

### **Maintainer** (Mantenedor)
- ✅ Todas as permissões de Developer
- ✅ Pode fazer push para branches protegidas
- ✅ Pode fazer merge de merge requests
- ✅ Pode proteger branches
- ✅ Pode adicionar/remover membros (com permissão Owner)
- ✅ Pode configurar CI/CD
- ✅ Pode deletar branches
- ❌ Não pode deletar o projeto
- ❌ Não pode transferir o projeto

### **Owner** (Proprietário)
- ✅ Todas as permissões de Maintainer
- ✅ Pode deletar o projeto
- ✅ Pode transferir o projeto
- ✅ Pode gerenciar todos os membros
- ✅ Acesso total ao projeto

## 📝 Recomendações por Função

### Para Desenvolvedores/QA:
- **Developer** ou **Maintainer**
- Permite fazer push, criar branches e merge requests

### Para Gerentes/Stakeholders:
- **Reporter** ou **Guest**
- Permite visualizar e acompanhar o progresso

### Para Líderes Técnicos:
- **Maintainer** ou **Owner**
- Permite gerenciar o projeto completamente

## 🔧 Método 2: Adicionar via URL Direta

Você também pode acessar diretamente a página de membros:

```
https://gitlab.servicenet.com.br/qa/automacao-de-teste/-/project_members
```

## 📋 Método 3: Adicionar Múltiplos Membros

1. Vá em **Settings** → **Members**
2. Clique em **"Invite members"**
3. Você pode adicionar múltiplos usuários separando por vírgula ou linha
4. Todos receberão o mesmo nível de permissão selecionado

## 👀 Ver Membros Atuais

Para ver quem tem acesso ao projeto:

1. Acesse: **Settings** → **Members**
2. Você verá uma lista de todos os membros com seus níveis de permissão
3. Você pode:
   - **Editar** permissões de um membro
   - **Remover** um membro
   - **Reenviar convite** se ainda não foi aceito

## 🔄 Alterar Permissões de um Membro Existente

1. Vá em **Settings** → **Members**
2. Encontre o membro na lista
3. Clique no dropdown ao lado do nome
4. Selecione o novo nível de permissão
5. Clique em **"Update permissions"**

## 🗑️ Remover um Membro

1. Vá em **Settings** → **Members**
2. Encontre o membro na lista
3. Clique no ícone de **lixeira** ou **"Remove member"**
4. Confirme a remoção

## 🔒 Proteger Branches (Opcional)

Para proteger a branch `main` e exigir merge requests:

1. Vá em **Settings** → **Repository** → **Protected branches**
2. Selecione a branch `main`
3. Configure:
   - **Allowed to merge**: Developer, Maintainer, Owner
   - **Allowed to push**: Maintainer, Owner
4. Isso impede pushes diretos na branch principal

## 📧 Notificações

Quando você adiciona um membro:
- ✅ A pessoa recebe um email de convite
- ✅ A pessoa precisa aceitar o convite
- ✅ Você recebe uma notificação quando a pessoa aceita

## 🆘 Problemas Comuns

### "User not found"
- **Solução**: Verifique se o username ou email está correto
- Certifique-se de que a pessoa tem uma conta no GitLab

### "Permission denied"
- **Solução**: Você precisa ser **Owner** ou **Maintainer** para adicionar membros
- Verifique suas permissões no projeto

### "Invite already sent"
- **Solução**: A pessoa já foi convidada
- Você pode reenviar o convite na lista de membros

## 📚 Links Úteis

- **Página de Membros**: https://gitlab.servicenet.com.br/qa/automacao-de-teste/-/project_members
- **Configurações do Projeto**: https://gitlab.servicenet.com.br/qa/automacao-de-teste/-/settings
- **Documentação GitLab**: https://docs.gitlab.com/ee/user/project/members/

## ✅ Checklist Rápido

- [ ] Acessar Settings → Members
- [ ] Clicar em "Invite members"
- [ ] Digitar username ou email
- [ ] Selecionar nível de permissão
- [ ] Clicar em "Invite"
- [ ] Aguardar pessoa aceitar o convite

