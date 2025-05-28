# Guia de Princípios DRY, KISS e YAGNI

Este guia aborda três princípios fundamentais para desenvolvimento de software eficaz: **DRY**, **KISS** e **YAGNI**, com definições, motivações, exemplos práticos e armadilhas comuns.

---

## 1. DRY (Don't Repeat Yourself)

**Definição**: Evite duplicação de conhecimento; cada parte do sistema deve ter uma única representação.

**Motivação**:

* Facilita manutenção: mudanças em um único lugar.
* Reduz inconsistências e bugs.

**Técnicas de aplicação**:

1. Refatoração para métodos/funções comuns.
2. Utilização de abstrações (classes, módulos, bibliotecas).
3. Templates e componentes reutilizáveis.

**Exemplo (JavaScript)**:

```js
// DUPLICADO: validações semelhantes em dois lugares
function validateUser(user) {
  if (!user.name) throw Error('Nome é obrigatório');
  if (!user.email) throw Error('Email é obrigatório');
}

function validateAdmin(admin) {
  if (!admin.name) throw Error('Nome é obrigatório');
  if (!admin.email) throw Error('Email é obrigatório');
  if (!admin.role) throw Error('Role é obrigatório');
}

// DRY: extrair validação genérica
function validateEntity(entity, fields) {
  fields.forEach(f => {
    if (!entity[f]) throw Error(`${f} é obrigatório`);
  });
}

validateEntity(user, ['name', 'email']);
validateEntity(admin, ['name', 'email', 'role']);
```

**Arm imprintas comuns**:

* Extrair abstrações cedo demais (YAGNI).
* Criar utilitários genéricos que se tornam difíceis de entender.
