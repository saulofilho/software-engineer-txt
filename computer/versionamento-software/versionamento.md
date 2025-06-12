# Guia Completo de Versionamento de Software

Este guia aborda, em nível avançado, as **práticas e padrões de versionamento de software**, incluindo esquemas, ferramentas, automação, controle de compatibilidade e boas práticas para projetos de todos os tamanhos.

---

## 1. Por que versionar?

* **Comunicação clara**: indica mudanças, compatibilidade e evolução.
* **Gerenciamento de dependências**: projetos consumidores sabem quais versões usar.
* **Reprodutibilidade**: permite reproduzir artefatos exatos no passado.
* **Automação de release**: pipelines de CI/CD trabalham com tags e números de versão.

---

## 2. Esquemas de Versionamento Comuns

| Esquema                                | Descrição                                           | Vantagens                                     | Desvantagens                     |
| -------------------------------------- | --------------------------------------------------- | --------------------------------------------- | -------------------------------- |
| **SemVer** (MAJOR.MINOR.PATCH)         | MAJOR: breaking; MINOR: features; PATCH: correções. | Compatibilidade semântica, amplamente adotado | Pode exigir disciplina rígida    |
| **Date-based** (YYYY.MM.DD or YYYY.MM) | Versão baseada em data de release.                  | Informação temporal, fácil de organizar       | Não indica magnitude de mudanças |
| **Sequential** (v1, v2, v3…)           | Incremento simples a cada release.                  | Simples de implementar                        | Não comunica tipo de mudança     |
| **CalVer** (YY.MM.REV ou YYYY.MM.REV)  | Combina data com revisão incremental.               | Contexto temporal + controle de release       | Pode ficar complexo              |
| **Commit SHA**                         | Usa hash de commit Git (ex: ab12cd34).              | Altíssima precisão, inambíguo                 | Pouca legibilidade               |

---

## 3. Versionamento Semântico (SemVer)

### 3.1 Formato

```text
MAJOR.MINOR.PATCH[-PRÉ-LANÇAMENTO][+METADADOS]
```

* **MAJOR**: alterações incompatíveis de API.
* **MINOR**: funcionalidades compatíveis adicionadas.
* **PATCH**: correções de bugs compatíveis.
* **Pré-lançamento**: `-alpha.1`, `-beta.2`, `-rc.1`.
* **Metadados**: `+build.123`, `+20250612` (não afeta precedência).

### 3.2 Regras de Precedência

1. Versão maior maior precedência.
2. Se MAJOR igual, MINOR maior precedência.
3. Se MINOR igual, PATCH maior precedência.
4. Pré-lançamentos têm precedência menor que release final.
5. Metadados são ignorados para precedência.

### 3.3 Exemplos

* `1.0.0` → primeira versão estável.
* `1.1.0` → adiciona recurso novo compatível.
* `1.1.1` → corrige bug sem alterar API.
* `2.0.0` → altera API de forma incompatível.
* `2.0.0-alpha.1` → versão alpha antes do 2.0.0.

---

## 4. Fluxo de Release Automatizado

1. Definir versão inicial no `CHANGELOG.md` e no manifest (`package.json`, `pom.xml`, etc.).
2. Desenvolver novos recursos em branches: `feature/...`, `bugfix/...`.
3. Criar Pull Request/Merge Request para `main`/`master`.
4. CI executa testes e valida lint antes de merge.
5. Ao merge, CI detecta tipo de mudança (semiautomático com convenções de commits ou ferramentas como Conventional Commits) e incrementa versão.
6. CI gera tag Git (`vMAJOR.MINOR.PATCH`) e publica artefato (npm, Docker, pacotes NuGet).
7. Atualizar `CHANGELOG.md` automaticamente (usando `standard-version`, `release-it`, `GitHub Releases`).

---

## 5. Convenções de Commit

* **Conventional Commits**:

  * `feat(scope): descrição breve` → incrementa MINOR.
  * `fix(scope): descrição breve` → incrementa PATCH.
  * `BREAKING CHANGE: descrição` ou `feat!: ...` → incrementa MAJOR.
* Ferramentas: `commitlint`, `husky` para validação local de commits.

---

## 6. Ferramentas e Integrações

| Ferramenta         | Finalidade                                 | Ecossistema     |
| ------------------ | ------------------------------------------ | --------------- |
| `semantic-release` | Automação completa de release SemVer       | Node.js         |
| `standard-version` | Gerenciamento de versionamento e changelog | Node.js         |
| `release-it`       | CLI genérica para versionamento & release  | Multiplataforma |
| `bump2version`     | Bump de versões em arquivos                | Python          |
| `cargo-release`    | Automatiza releases em Rust                | Rust            |
| GitHub Actions     | Workflows CI/CD para releases              | GitHub          |
| GitLab CI/CD       | Pipelines para publish e versionamento     | GitLab          |

---

## 7. Gerenciamento de Branches

* **GitFlow**:

  * Branches principais: `main`, `develop`.
  * Branches de suporte: `feature`, `release`, `hotfix`.
  * Integrações definem como e quando atualizar versões.

* **Trunk-Based Development**:

  * Branch única `main` ou `trunk`.
  * Releases feitos via tags e feature toggles.

---

## 8. Versionamento de API

* **URLs versionadas**: `/v1/users`, `/v2/users`.
* **Header versioning**: `Accept: application/vnd.myapp.v1+json`.
* **Query parameter**: `?version=1`.
* **Evolução da API**:

  * Adotar depreciação antes de remoção.
  * Manter compatibilidade por versão definida.

---

## 9. Boas Práticas

1. **Documentar claramente** o esquema de versionamento no README ou guia de contribuição.
2. **Manter CHANGELOG.md** atualizado com seções de `Added`, `Changed`, `Fixed`, `Removed`, `Deprecated`.
3. **Automatizar** o máximo possível (bump de versão, changelog, tags).
4. **Garantir compatibilidade** conforme as regras SemVer ou o esquema adotado.
5. **Comunicar** breaking changes de forma destacada.
6. **Testar pacotes** publicados em ambientes de staging antes do release final.

---

## 10. Conclusão

Adotar um esquema de versionamento consistente e automatizado é crucial para escalabilidade, colaboração e confiabilidade de projetos de software. Seja SemVer, CalVer ou outro, discipline-se em seguir regras claras, documentar mudanças e usar ferramentas adequadas para liberar software com confiança.
