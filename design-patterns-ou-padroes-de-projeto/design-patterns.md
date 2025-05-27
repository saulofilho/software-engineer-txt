# Guia Completo de Design Patterns (Padrões de Projetos)

Este guia aborda, em nível avançado, os principais **Design Patterns** de software, categorizados em **Criacionais**, **Estruturais** e **Comportamentais**, trazendo descrição, uso, vantagens e exemplos de código em C#.

---

## 1. Introdução

Design Patterns são soluções reutilizáveis para problemas recorrentes no desenvolvimento de software. Definidos por Gamma, Helm, Johnson e Vlissides (GoF), eles promovem **coesão**, **baixo acoplamento**, **flexibilidade** e **manutenibilidade**.

### Benefícios

* Comunicam arquiteturas complexas de forma padronizada.
* Auxiliam na escalabilidade e extensão do sistema.
* Facilitam testes automatizados e refatoração.

---

## 2. Padrões Criacionais

### 2.1 Singleton

Garante uma única instância de uma classe.

```csharp
public sealed class Singleton {
    private static readonly Lazy<Singleton> instance =
        new Lazy<Singleton>(() => new Singleton());

    public static Singleton Instance => instance.Value;
    private Singleton() { /* inicialização */ }
}
```

**Uso**: gerenciadores de configuração, fábricas de recursos.

### 2.2 Factory Method

Define uma interface para criar objeto, adiando a instanciação para subclasses.

```csharp
// Produto
public interface IConnection { void Connect(); }
public class SqlConnection : IConnection { public void Connect() {/*...*/} }
public class OracleConnection : IConnection { public void Connect() {/*...*/} }

// Creator
public abstract class DbFactory {
    public abstract IConnection CreateConnection();
}
public class SqlFactory : DbFactory {
    public override IConnection CreateConnection() => new SqlConnection();
}
public class OracleFactory : DbFactory {
    public override IConnection CreateConnection() => new OracleConnection();
}
```

**Uso**: sistemas de plugins, drivers de banco de dados.

### 2.3 Abstract Factory

Agrupa fábricas relacionadas sem expor classes concretas.

```csharp
public interface IGUIFactory {
    IButton CreateButton();
    ICheckbox CreateCheckbox();
}
public class WinFactory : IGUIFactory {
    public IButton CreateButton() => new WinButton();
    public ICheckbox CreateCheckbox() => new WinCheckbox();
}
public class MacFactory : IGUIFactory {
    public IButton CreateButton() => new MacButton();
    public ICheckbox CreateCheckbox() => new MacCheckbox();
}
```

**Uso**: interfaces multiplataforma, temas de UI.

### 2.4 Builder

Separa a construção de um objeto complexo de sua representação.

```csharp
public class Car { /* propriedades como Engine, Wheels etc. */ }
public interface ICarBuilder {
    void BuildEngine();
    void BuildWheels();
    Car GetResult();
}
public class SportsCarBuilder : ICarBuilder {
    private Car car = new Car();
    public void BuildEngine() => car.Engine = "V8";
    public void BuildWheels() => car.Wheels = "Sport";
    public Car GetResult() => car;
}

// Diretor
public class Director {
    public Car Construct(ICarBuilder builder) {
        builder.BuildEngine();
        builder.BuildWheels();
        return builder.GetResult();
    }
}
```

**Uso**: criação de relatórios, objetos com múltiplas configurações.

### 2.5 Prototype

Clona objetos existentes sem depender de suas classes concretas.

```csharp
public abstract class Prototype {
    public abstract Prototype Clone();
}
public class ConcretePrototype : Prototype {
    public int Data;
    public override Prototype Clone() => (Prototype)MemberwiseClone();
}
```

**Uso**: criação dinâmica de objetos, redução de overhead de inicialização.

---

## 3. Padrões Estruturais

### 3.1 Adapter

Converte a interface de uma classe em outra interface esperada pelo cliente.

```csharp
// Cliente espera ILogger
public interface ILogger { void Log(string msg); }
public class LegacyLogger { public void WriteLog(string m) {/*...*/} }

// Adapter
public class LoggerAdapter : ILogger {
    private readonly LegacyLogger legacy;
    public LoggerAdapter(LegacyLogger legacy) { this.legacy = legacy; }
    public void Log(string msg) => legacy.WriteLog(msg);
}
```

**Uso**: integração com bibliotecas legadas.

### 3.2 Decorator

Adiciona responsabilidades a um objeto dinamicamente.

```csharp
public interface IComponent { void Operation(); }
public class ConcreteComponent : IComponent { public void Operation() {/*...*/} }
public abstract class Decorator : IComponent {
    protected IComponent component;
    protected Decorator(IComponent c) { component = c; }
    public virtual void Operation() => component.Operation();
}
public class LoggingDecorator : Decorator {
    public LoggingDecorator(IComponent c) : base(c) {}
    public override void Operation() {
        Console.WriteLine("Before");
        base.Operation();
        Console.WriteLine("After");
    }
}
```

**Uso**: logging, compressão, segurança.

### 3.3 Facade

Oferece interface simplificada para subsistemas complexos.

```csharp
public class Mortgage { /* subsistema */ }
public class Loan { /* subsistema */ }
public class Credit { /* subsistema */ }

public class BankFacade {
    private readonly Mortgage m = new Mortgage();
    private readonly Loan l = new Loan();
    private readonly Credit c = new Credit();
    public bool IsEligible(Customer cust, int amount) {
        return m.Check(cust, amount) && l.Check(cust) && c.Check(cust);
    }
}
```

**Uso**: APIs de alto nível, gateways.

### 3.4 Composite

Trata objetos individuais e composições de forma uniforme.

```csharp
public interface IGraphic { void Draw(); }
public class Dot : IGraphic { public void Draw() => Console.WriteLine("Dot"); }
public class CompositeGraphic : IGraphic {
    private readonly List<IGraphic> children = new();
    public void Add(IGraphic g) => children.Add(g);
    public void Draw() => children.ForEach(c => c.Draw());
}
```

**Uso**: árvores, elementos de UI.

### 3.5 Proxy

Fornece um substituto ou placeholder para outro objeto.

```csharp
public interface IService { void Request(); }
public class RealService : IService { public void Request() {/*...*/} }

public class ProxyService : IService {
    private RealService real;
    public void Request() {
        if (real == null) real = new RealService();
        // controle de acesso, logging etc.
        real.Request();
    }
}
```

**Uso**: lazy loading, controle de acesso.

---

## 4. Padrões Comportamentais

### 4.1 Strategy

Define família de algoritmos, encapsula cada um e os torna intercambiáveis.

```csharp
public interface IStrategy { void Execute(); }
public class ConcreteStrategyA : IStrategy { public void Execute() {/*...*/} }
public class Context {
    private IStrategy strategy;
    public Context(IStrategy s) { strategy = s; }
    public void DoBusiness() => strategy.Execute();
}
```

**Uso**: validações, ordenações.

### 4.2 Observer

Define dependência um-para-muitos para notificar objetos automaticamente.

```csharp
public interface IObserver { void Update(); }
public interface ISubject {
    void Attach(IObserver o);
    void Detach(IObserver o);
    void Notify();
}
public class ConcreteSubject : ISubject {
    private List<IObserver> observers = new();
    public void Attach(IObserver o) => observers.Add(o);
    public void Detach(IObserver o) => observers.Remove(o);
    public void Notify() => observers.ForEach(o => o.Update());
}
```

**Uso**: eventos, UI reativa.

### 4.3 Command

Encapsula requisições em objetos, permitindo parametrização e enfileiramento.

```csharp
public interface ICommand { void Execute(); }
public class LightOnCommand : ICommand {
    private Light light;
    public LightOnCommand(Light l) { light = l; }
    public void Execute() => light.On();
}
public class Invoker {
    private ICommand command;
    public void SetCommand(ICommand c) => command = c;
    public void Invoke() => command.Execute();
}
```

**Uso**: undo/redo, filas de tarefas.

### 4.4 Chain of Responsibility

Evita acoplamento entre remetente e receptor, passando a requisição por cadeia.

```csharp
public abstract class Handler {
    protected Handler next;
    public void SetNext(Handler h) => next = h;
    public abstract void Handle(Request req);
}
public class ConcreteHandlerA : Handler {
    public override void Handle(Request req) {
        if (req.Type == A) {/* trata */}
        else next?.Handle(req);
    }
}
```

**Uso**: processamento de eventos, filtros.

---

## 5. Conclusão

O domínio de Design Patterns facilita a criação de software robusto e escalável. Use-os como ferramenta de comunicação e guia arquitetural, adaptando cada padrão ao contexto do projeto e evitando sobreengenharia.
