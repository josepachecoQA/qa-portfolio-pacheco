# 🚀 Guia de Configuração do GitLab

## ✅ Status Atual

- ✅ Repositório Git inicializado
- ✅ Commit inicial criado
- ✅ Remote do GitLab configurado
- ⏳ Push pendente (requer autenticação)

## 📋 Próximos Passos

### 1. Criar o Projeto no GitLab

1. Acesse: https://gitlab.servicenet.com.br/dashboard/projects
2. Clique em **"New project"** ou **"Novo projeto"**
3. Escolha **"Create blank project"** ou **"Criar projeto em branco"**
4. Configure:
   - **Project name**: `automacao-de-testes` (ou o nome que preferir)
   - **Project slug**: será gerado automaticamente
   - **Visibility Level**: Escolha conforme necessário (Private/Internal/Public)
5. Clique em **"Create project"**

### 2. Fazer Push do Código

Você tem duas opções:

#### Opção A: Usando HTTPS (com credenciais)

```bash
cd /home/alexandre-costa/Documentos/Projetos/automacao_de_testes
git push -u origin main
```

Quando solicitado:
- **Username**: Seu usuário do GitLab
- **Password**: Seu token de acesso pessoal (não use sua senha)

> 💡 **Nota**: Se você não tem um token de acesso pessoal, crie um em:
> Settings → Access Tokens → Personal Access Tokens

#### Opção B: Usando SSH (recomendado)

1. **Gerar chave SSH** (se ainda não tiver):
```bash
ssh-keygen -t ed25519 -C "alexandre.costa@servicenet.com.br"
```

2. **Adicionar chave SSH ao GitLab**:
   - Copie a chave pública: `cat ~/.ssh/id_ed25519.pub`
   - Acesse: GitLab → Settings → SSH Keys
   - Cole a chave e salve

3. **Alterar o remote para SSH**:
```bash
cd /home/alexandre-costa/Documentos/Projetos/automacao_de_testes
git remote set-url origin git@gitlab.servicenet.com.br:automacao-de-testes.git
```

4. **Fazer push**:
```bash
git push -u origin main
```

### 3. Verificar o Push

Após o push bem-sucedido, você verá:
```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
Delta compression using up to X threads
Compressing objects: 100% (X/X), done.
Writing objects: 100% (X/X), done.
To https://gitlab.servicenet.com.br/automacao-de-testes.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

## 🔧 Configurações Adicionais

### Alterar o nome do projeto no GitLab

Se você criou o projeto com um nome diferente, atualize o remote:

```bash
git remote set-url origin https://gitlab.servicenet.com.br/SEU-NOME-DO-PROJETO.git
```

### Verificar configuração atual

```bash
git remote -v
git status
```

## 📝 Informações do Repositório

- **Local**: `/home/alexandre-costa/Documentos/Projetos/automacao_de_testes`
- **Remote**: `https://gitlab.servicenet.com.br/automacao-de-testes.git`
- **Branch**: `main`
- **Commit inicial**: `20975e9`

## 🆘 Problemas Comuns

### Erro: "fatal: could not read Username"
- **Solução**: Use um token de acesso pessoal ao invés da senha

### Erro: "remote: HTTP Basic: Access denied"
- **Solução**: Verifique suas credenciais ou use SSH

### Erro: "repository not found"
- **Solução**: Certifique-se de que o projeto foi criado no GitLab

## 📚 Recursos

- [Documentação do GitLab](https://docs.gitlab.com/)
- [Como criar token de acesso pessoal](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)
- [Configurar SSH no GitLab](https://docs.gitlab.com/ee/user/ssh.html)

