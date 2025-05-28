# Guia de Princípios DRY, KISS e YAGNI

Este guia aborda três princípios fundamentais para desenvolvimento de software eficaz: **DRY**, **KISS** e **YAGNI**, com definições, motivações, exemplos práticos e armadilhas comuns.

---

## 3. YAGNI (You Aren't Gonna Need It)

**Definição**: Não implemente funcionalidades até que sejam realmente necessárias.

**Motivação**:

* Evita desperdício de tempo e esforço em recursos nunca usados.
* Mantém o código focado e reduz dívidas técnicas.

**Como aplicar**:

1. Priorizar requisitos reais do cliente.
2. Escrever testes apenas para casos atuais.
3. Refatorar quando surgir demanda nova, não antes.

**Exemplo (C#)**:

```csharp
// NÃO YAGNI: planejar recursos futuros sem necessidade
public class Report {
  public void GeneratePdf() { /* ... */ }
  public void GenerateExcel() { /* ainda não usado */ }
  public void GenerateWord()  { /* ainda não usado */ }
}

// YAGNI: implementar somente o que é requisitado
public class Report {
  public void GeneratePdf() { /* ... */ }
}
```

**Cuidado**:

* Reavaliar periodicamente: às vezes antecipação mínima reduz retrabalho.
