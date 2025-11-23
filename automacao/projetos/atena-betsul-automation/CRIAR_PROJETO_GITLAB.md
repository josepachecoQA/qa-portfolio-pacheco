# 🚀 Criar Projeto no GitLab - Passo a Passo

## 📋 Passo 1: Criar o Projeto no GitLab

1. **Acesse a URL**: https://gitlab.servicenet.com.br/projects/new?namespace_id=800

2. **Preencha o formulário**:
   - **Project name**: `automacao-de-testes`
   - **Project slug**: Será gerado automaticamente (automacao-de-testes)
   - **Project description** (opcional): `Projeto de automação de testes Cypress para sistemas Atena e Betsul`
   - **Visibility Level**: Escolha conforme necessário
     - **Private**: Apenas membros do projeto
     - **Internal**: Membros do GitLab
     - **Public**: Todos podem ver

3. **IMPORTANTE**: 
   - ❌ **NÃO** marque "Initialize repository with a README"
   - ❌ **NÃO** marque "Add .gitignore"
   - ❌ **NÃO** marque "Choose a license"
   
   (Já temos esses arquivos no repositório local)

4. **Clique em "Create project"**

## 📋 Passo 2: Adicionar Chave SSH ao GitLab

1. **Copie sua chave SSH pública**:
```bash
cat ~/.ssh/id_ed25519.pub
```

2. **No GitLab**:
   - Vá em: **Settings** (ícone de engrenagem no canto superior direito) → **SSH Keys**
   - Ou acesse diretamente: https://gitlab.servicenet.com.br/-/profile/keys
   - Cole a chave SSH no campo "Key"
   - Adicione um título (ex: "Notebook - Alexandre")
   - Clique em "Add key"

## 📋 Passo 3: Fazer Push do Código

Após criar o projeto e adicionar a chave SSH, execute:

```bash
cd /home/alexandre-costa/Documentos/Projetos/automacao_de_testes
git push -u origin main
```

## ✅ Verificação

Após o push bem-sucedido, você verá algo como:

```
Enumerating objects: 40, done.
Counting objects: 100% (40/40), done.
Delta compression using up to 8 threads
Compressing objects: 100% (38/38), done.
Writing objects: 100% (40/40), 6.45 KiB | 6.45 MiB/s, done.
Total 40 (delta 2), reused 0 (delta 0), pack-reused 0
To gitlab.servicenet.com.br:automacao-de-testes.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

## 🔧 Se o nome do projeto for diferente

Se você criou o projeto com outro nome, atualize o remote:

```bash
git remote set-url origin git@gitlab.servicenet.com.br:SEU-NOME-DO-PROJETO.git
git push -u origin main
```

## 🆘 Problemas Comuns

### Erro: "Host key verification failed"
**Solução**: Adicione o GitLab aos hosts conhecidos:
```bash
ssh-keyscan gitlab.servicenet.com.br >> ~/.ssh/known_hosts
```

### Erro: "Permission denied (publickey)"
**Solução**: 
1. Verifique se a chave SSH está adicionada ao GitLab
2. Teste a conexão: `ssh -T git@gitlab.servicenet.com.br`
3. Se não funcionar, verifique se está usando a chave correta:
   ```bash
   ssh-add -l
   ssh-add ~/.ssh/id_ed25519
   ```

### Erro: "repository not found"
**Solução**: 
1. Verifique se o projeto foi criado no GitLab
2. Verifique se você tem permissão de acesso ao projeto
3. Verifique se o nome do projeto está correto no remote:
   ```bash
   git remote -v
   ```

## 📝 Informações do Repositório Local

- **Localização**: `/home/alexandre-costa/Documentos/Projetos/automacao_de_testes`
- **Remote configurado**: `git@gitlab.servicenet.com.br:automacao-de-testes.git`
- **Branch**: `main`
- **Commits prontos**: 2 commits
  - Initial commit
  - Documentação do GitLab

## 🎯 Checklist Final

- [ ] Projeto criado no GitLab
- [ ] Chave SSH adicionada ao GitLab
- [ ] Push realizado com sucesso
- [ ] Código visível no GitLab

