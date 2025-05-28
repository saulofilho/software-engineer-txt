# Guia Completo de Princípios SOLID

Este guia detalha os cinco princípios SOLID, fundamentais para design de software orientado a objetos, promovendo código coeso, flexível e de fácil manutenção. Inclui definição, motivação, exemplos de aplicação e armadilhas comuns.

---

## 1. Single Responsibility Principle (SRP)

**Definição**: Uma classe deve ter apenas uma única razão para mudar — ou seja, uma única responsabilidade.

**Motivação**:

* Evita acoplamentos desnecessários.
* Facilita testes e refatoração.

**Exemplo (C#)**:

```csharp
// Violação: classe faz leitura de arquivo e formatação de relatório
class ReportManager {
  public string ReadData(string path) { /* ... */ }
  public string FormatCsv(string data) { /* ... */ }
  public string FormatHtml(string data) { /* ... */ }
}

// Correto: separar responsabilidades
class FileReader {
  public string Read(string path) { /* ... */ }
}
class CsvFormatter {
  public string Format(string data) { /* ... */ }
}
class HtmlFormatter {
  public string Format(string data) { /* ... */ }
}
```

**Cuidados**:

* Não extrair classes demais que fragmentem lógica relacionada.

---

## 2. Open/Closed Principle (OCP)

**Definição**: Entidades de software (classes, módulos, funções) devem estar **abertas** para extensão, mas **fechadas** para modificação.

**Motivação**:

* Evitar regressões.
* Suportar novos comportamentos sem alterar código existente.

**Técnica**: usar abstrações (interfaces, herança ou composição).

**Exemplo (C#)**:

```csharp
// Violação: precisa modificar o cálculo para cada novo tipo de desconto
class Order {
  public decimal CalculateTotal(bool isSummer) {
    if (isSummer) return /* desconto */;
    else return /* sem desconto */;
  }
}

// Correto: extensão via novas classes
interface IDiscount {
  decimal Apply(decimal amount);
}
class SummerDiscount : IDiscount { /* ... */ }
class NoDiscount : IDiscount { /* ... */ }

class Order {
  private readonly IDiscount discount;
  public Order(IDiscount discount) { this.discount = discount; }
  public decimal CalculateTotal(decimal amount) {
    return discount.Apply(amount);
  }
}
```

**Cuidados**:

* Excesso de abstrações pode introduzir complexidade desnecessária.

---

## 3. Liskov Substitution Principle (LSP)

**Definição**: Subtipos devem ser substituíveis pelos seus tipos base sem alterar o comportamento do programa.

**Motivação**:

* Garante correta herança e polimorfismo.
* Evita que subclasses contrariem expectativas.

**Exemplo (C#)**:

```csharp
// Violação: Rectangle e Square
class Rectangle {
  public virtual int Width { get; set; }
  public virtual int Height { get; set; }
}
class Square : Rectangle {
  public override int Width { set { base.Width = base.Height = value; } }
  public override int Height { set { base.Width = base.Height = value; } }
}

// Código cliente assume comportamento de Rectangle
void Resize(Rectangle r) {
  r.Width = 5;
  r.Height = 10;
  Debug.Assert(r.Width * r.Height == 50); // falha para Square
}

// Correto: modelar via composição ou hierarquia distinta
interface IShape { int Area(); }
class Rectangle : IShape { /* ... */ }
class Square : IShape { /* ... */ }
```

**Cuidados**:

* Revisar invariantes da classe base ao criar subtipo.

---

## 4. Interface Segregation Principle (ISP)

**Definição**: Muitas interfaces específicas são melhores do que uma única interface geral.

**Motivação**:

* Clientes não devem ser forçados a depender de métodos que não usam.
* Reduz acoplamento.

**Exemplo (C#)**:

```csharp
// Violação: interface grande demais
interface IMultiFunctionDevice {
  void Print(Document d);
  void Scan(Document d);
  void Fax(Document d);
}

// Correto: interfaces segregadas
interface IPrinter { void Print(Document d); }
interface IScanner { void Scan(Document d); }
interface IFax { void Fax(Document d); }

class AllInOnePrinter : IPrinter, IScanner, IFax { /* ... */ }
class SimplePrinter : IPrinter { /* ... */ }
```

**Cuidados**:

* Não criar interfaces tão pequenas que percam coesão.

---

## 5. Dependency Inversion Principle (DIP)

**Definição**:

1. Módulos de alto nível não devem depender de módulos de baixo nível: ambos devem depender de abstrações.
2. Abstrações não devem depender de detalhes; detalhes devem depender de abstrações.

**Motivação**:

* Inverter dependências melhora flexibilidade e teste.

**Exemplo (C#)**:

```csharp
// Violação: classe de alto nível depende de implementação concreta
class EmailNotifier {
  private SmtpClient client = new SmtpClient();
  public void Notify(string msg) { client.Send(msg); }
}

// Correto: depender de abstração
interface INotificationService { void Send(string msg); }
class EmailNotificationService : INotificationService { /* usa SmtpClient */ }
class SmsNotificationService : INotificationService { /* ... */ }

class OrderProcessor {
  private readonly INotificationService notifier;
  public OrderProcessor(INotificationService notifier) {
    this.notifier = notifier;
  }
  public void Process() {
    // lógica...
    notifier.Send("Pedido concluído");
  }
}
```

**Cuidados**:

* Gerenciamento de dependências pode requerer container IoC/DI.

---

## 6. Aplicação Conjunta e Boas Práticas

1. **Equilíbrio**: não introduza abstrações sem necessidade.
2. **Refatoração contínua**: aplique SOLID durante o ciclo verde-refactor em TDD.
3. **Revisões de código**: verificar violações dos princípios.

---

## 7. Armadilhas Comuns

* SRP exagerado: classes demais (anemia de domínio).
* OCP sem limites: excesso de subclasses.
* Violação LSP: herança incorreta para "forçar" reuso.
* ISP: interfaces minúsculas demais (processo pesado na implementação).
* DIP sem DI container: `new` espalhado, difícil teste.

---

## Conclusão

SOLID é um guia poderoso para design de sistemas orientados a objetos. A aplicação equilibrada desses princípios resulta em código mais robusto, fácil de estender e manter.
