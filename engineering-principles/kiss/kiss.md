# Guia de Princípios DRY, KISS e YAGNI

Este guia aborda três princípios fundamentais para desenvolvimento de software eficaz: **DRY**, **KISS** e **YAGNI**, com definições, motivações, exemplos práticos e armadilhas comuns.

---

## 2. KISS (Keep It Simple, Stupid)

**Definição**: Mantenha o design e a implementação simples e diretos; evite complexidade desnecessária.

**Motivação**:

* Código simples é mais legível, testável e menos propenso a erros.
* Facilita onboarding de novos desenvolvedores.

**Práticas**:

1. Dividir problemas em passos menores.
2. Evitar padrões/pacotes complexos quando não são necessários.
3. Favor soluções óbvias antes de mais elegantes.

**Exemplo (Ruby)**:

```ruby
# Complexo: uso de metaprogramação desnecessária
def define_getter(name)
  define_method(name) { instance_variable_get("@#{name}") }
end

defining_fields = [:name, :email]
defining_fields.each { |f| define_getter(f) }

# Simples: attr_reader
attr_reader :name, :email
```

**Armadilhas comuns**:

* Overspecifying: pensar em casos extremos antes do necessário.
* Subestimar a complexidade futura e depois ter que refatorar.
