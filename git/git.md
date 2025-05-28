# Guia Completo de Git

Este guia cobre, em nível avançado, tudo sobre Git: conceitos, arquitetura interna, comandos essenciais e avançados, workflows, boas práticas e manutenção.

---

## 1. O que é Git?

Git é um sistema de controle de versão distribuído criado por Linus Torvalds em 2005. Ele armazena snapshots do repositório, permitindo ramificações leves, histórico imutável e colaboração offline.

---

## 2. Arquitetura Interna

Git organiza dados em **objetos** imutáveis:

* **Blob**: conteúdo de arquivos.
* **Tree**: diretórios, mapeamento de nomes para blobs/trees.
* **Commit**: ponteiro para uma tree, metadados (autor, mensagem, pais).
* **Tag**: ponteiro anotado para um commit (opcional).

Cada objeto é armazenado em `.git/objects`, nomeado pelo hash SHA-1 (ou SHA-256 em versões recentes).

---

## 3. Configuração Inicial e Metadados

```bash
# Configurações globais
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
# Editor e merge tool
git config --global core.editor vim
git config --global merge.tool meld
```

---

## 4. Fluxo de Trabalho Básico

```bash
git init                # inicializa repositório vazio
git clone <url>         # clona repositório remoto
# Modificações
git add <arquivo>       # etapa de staging
git commit -m "msg"    # cria novo commit
git push origin main    # envia commits ao remoto
git pull                # atualiza branch local
```

---

## 5. Branching e Tags

### Criar, listar e alternar branches

```bash
git branch             # lista branches locais
git branch feature/X   # cria branch
git checkout feature/X # muda para branch
# ou
git switch -c feature/X
```

### Mesclar e reconciliar

```bash
git merge feature/X    # merge direto
# conflito? editar arquivos, depois:
git add <resolvido>
git commit
```

### Tags

```bash
git tag v1.0          # tag leve
git tag -a v1.0 -m "Release 1.0"  # tag anotada
git push origin v1.0  # envia tag
```

---

## 6. Rebase e Cherry-Pick

### Rebase interactivo

```bash
git rebase -i HEAD~5  # reescreve últimos 5 commits: squash, edit, reword
```

### Cherry-pick

```bash
git cherry-pick <commit>  # traz commit específico para o branch atual
```

---

## 7. Stash e Reflog

* **Stash**: guarda mudanças não commitadas

```bash
git stash save "WIP"
git stash list
git stash pop
```

* **Reflog**: histórico de HEAD, mesmo em rebases e resets

```bash
git reflog
git checkout HEAD@{3}
```

---

## 8. Submódulos e Subtree

### Submódulos

```bash
git submodule add <url> path/to/sub
git submodule update --init --recursive
```

### Subtree (alternativa)

```bash
git subtree add --prefix=dir <url> main --squash
```

---

## 9. Hooks

Localizados em `.git/hooks`, permitem scripts em eventos:

* `pre-commit`: validações antes de commit.
* `pre-push`: testes antes de push.
* `post-merge`: ações após merge.

Exemplo `pre-commit` em bash:

```bash
#!/bin/sh
npm test || exit 1
```

---

## 10. Workflows Populares

* **Gitflow**: branches principais (`main`, `develop`) + feature/release/hotfix.
* **GitHub Flow**: `main` sempre pronta, PRs curtas em branches.
* **Trunk-Based Development**: branches curtas, trunk único, flags de recurso.

---

## 11. Comandos Avançados

* `git bisect`: busca binária para encontrar commit que introduziu bug.
* `git blame`: mostra autor e linha de código.
* `git archive`: empacota versões.
* `git gc --aggressive`: limpa e compacta objetos.

---

## 12. Manutenção e Performance

* **Repacking**: `git repack -a -d --depth=250 --window=250`.
* **Shallow clone**: `git clone --depth 1`.
* **Prune**: `git remote prune origin` remove refs obsoletos.

---

## 13. Segurança e Acesso

* **Chaves SSH**: autenticação sem senha.
* **HTTPS com token**: usar Git credential manager.
* **Signed commits/tags**: `git commit -S`, `git tag -s`.

---

## 14. Integração com CI/CD

* **GitHub Actions**, **GitLab CI**, **Jenkins**: gatilhos em push, PR, tags.
* Exemplo de pipeline simples (GitHub Actions):

```yaml
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install
      - run: npm test
```

---

## 15. Boas Práticas

1. Commits pequenos e atômicos.
2. Mensagens claras (Imperative mood).
3. Revisão de código via PR.
4. Proteção de branches principais (status checks).
5. Uso criterioso de force-push (somente em branches de feature).

---

## Conclusão

Dominar Git envolve entender suas estruturas internas e fluxos de trabalho, além de boas práticas que garantem histórico limpo e colaboração eficaz.
