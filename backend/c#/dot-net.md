# Guia Completo de .NET

Este guia aborda, em nível avançado, o ecossistema **.NET** da Microsoft, cobrindo desde conceitos essenciais da plataforma até aspectos avançados de desenvolvimento com **C#**, **ASP.NET Core**, **Entity Framework Core**, **Design Patterns**, **Testes**, **Deploy** e **Boas Práticas**.

---

## 1. Visão Geral do .NET

* **O que é .NET?**

  * Plataforma open source, cross-platform, para desenvolvimento de aplicações web, desktop, mobile, serviços de nuvem, microserviços, IoT e jogos.
  * Composta por:

    * **Runtime (CLR / CoreCLR / Mono)**: ambiente de execução que gerencia garbage collection, tipos, segurança.
    * **Base Class Library (BCL)**: biblioteca padrão com tipos fundamentais (collections, I/O, redes, criptografia etc.).
    * **SDK / CLI**: ferramentas de linha de comando (`dotnet`) para compilação, execução, testes e publicação.
    * **Linguagens**: C#, F#, Visual Basic (VB).
    * **ASP.NET Core**: framework web para APIs, sites MVC, Razor Pages.
    * **Entity Framework Core**: ORM para acesso a bancos relacionais.
    * **Xamarin / MAUI**: desenvolvimento mobile e desktop multiplataforma.

* **Edições**:

  * **.NET Framework**: versão Windows Legacy (4.x), não cross-platform.
  * **.NET Core / .NET 5+**: unificação da plataforma, cross-platform (Windows, Linux, macOS).
  * **.NET Standard**: especificação de APIs comuns para librarias compatíveis.

---

## 2. Instalação e Ferramentas

### 2.1 .NET SDK

* **Download**: acesse [https://dotnet.microsoft.com/download](https://dotnet.microsoft.com/download) para obter o SDK mais recente (e.g., .NET 6, .NET 7).
* **Instalação** (Windows, Linux, macOS): siga instruções específicas para cada sistema.
* **Verificar instalação**:

  ```bash
  dotnet --version
  dotnet --info
  ```

### 2.2 .NET CLI (Command Line Interface)

* **Comandos principais**:

  * `dotnet new <template>`: cria novo projeto (ex.: `console`, `webapi`, `mvc`, `classlib`, `xunit`).
  * `dotnet build`: compila a solução/projeto.
  * `dotnet run`: compila e executa (apenas para projetos executáveis).
  * `dotnet test`: executa testes automatizados.
  * `dotnet publish`: empacota para deploy (gera artefatos otimizados).
  * `dotnet add package <PackageName>`: adiciona pacote NuGet.
  * `dotnet restore`: restaura dependências via NuGet.
  * `dotnet tool`: gerencia ferramentas globais ou locais.

### 2.3 IDEs e Editores

* **Visual Studio 2022 (Windows/macOS)**: IDE completo com designers, depuração, profiling.
* **Visual Studio Code**: editor leve, extensões C# (OmniSharp), debugging, IntelliSense.
* **JetBrains Rider**: IDE cross-platform, suportando .NET e Unity.
* **dotnet watch**: ferramenta CLI para recompilar/reiniciar automaticamente.

---

## 3. C# Avançado

### 3.1 Sintaxe e Recursos Modernos

* **Type Inference**:

  ```csharp
  var texto = "Hello .NET";
  var numero = 42;
  ```
* **Nullable Reference Types** (`string?` vs `string`): ajuda a evitar NullReferenceException.
* **Record Types** (C# 9+): classes imutáveis com suporte a igualdade por valor.

  ```csharp
  public record Pessoa(string Nome, int Idade);
  ```
* **Pattern Matching** aprimorado:

  ```csharp
  if (obj is Pessoa { Idade: >=18 } adult) { /*...*/ }
  ```
* **Expressions Bodied Members**:

  ```csharp
  public string Nome { get; init; }
  public int Idade { get; init; }
  public override string ToString() => $"{Nome}, {Idade}";
  ```
* **Top-level Statements** (C# 9+): simplifica programas console.

  ```csharp
  using System;
  Console.WriteLine("Olá .NET");
  ```

### 3.2 Assemblies, Namespaces e Reflection

* **Assembly**: unidade compilada (.dll ou .exe) carregada pelo CLR.
* **Namespace**: agrupa tipos de forma hierárquica.
* **Reflection**: inspecionar metadados em tempo de execução.

  ```csharp
  var type = typeof(Cliente);
  var props = type.GetProperties();
  foreach (var prop in props) Console.WriteLine(prop.Name);
  ```

### 3.3 Programação Assíncrona

* **async/await**:

  ```csharp
  public async Task<string> GetDataAsync(string url)
  {
      using var http = new HttpClient();
      var response = await http.GetAsync(url);
      return await response.Content.ReadAsStringAsync();
  }
  ```
* **Task Parallel Library (TPL)**: `Task.Run`, `Task.WhenAll`, `Parallel.ForEach`.
* **IAsyncEnumerable<T>** (C# 8+): streams assíncronos.

  ```csharp
  public async IAsyncEnumerable<int> ObterNumerosAsync()
  {
    for (int i = 0; i < 10; i++)
    {
      await Task.Delay(100);
      yield return i;
    }
  }
  ```

### 3.4 Generics e Constraints

* **Definição Genérica**:

  ```csharp
  public class Repositorio<T> where T : EntityBase
  {
    public void Adicionar(T item) { /*...*/ }
  }
  ```
* **Constraints**: `where T : class`, `where T : struct`, `where T : new()`, `where T : U`.

### 3.5 Delegates, Events e Lambda

* **Delegate**: tipo que referencia métodos.

  ```csharp
  public delegate int Operacao(int x, int y);
  ```
* **Action e Func**:

  ```csharp
  Action<string> acao = msg => Console.WriteLine(msg);
  Func<int, int, int> soma = (a, b) => a + b;
  ```
* **Events**:

  ```csharp
  public event EventHandler<PedidoEventArgs> PedidoCriado;
  protected virtual void OnPedidoCriado(PedidoEventArgs e) => PedidoCriado?.Invoke(this, e);
  ```

### 3.6 LINQ (Language Integrated Query)

* **Consultas em coleções**:

  ```csharp
  var adultos = listaPessoas.Where(p => p.Idade >= 18)
                             .OrderBy(p => p.Nome)
                             .Select(p => new { p.Nome, p.Idade });
  ```
* **Operators**: `Where`, `Select`, `OrderBy`, `GroupBy`, `Join`, `Distinct`, `Skip`, `Take`.
* **LINQ to Objects** vs **LINQ to Entities** (EF Core) vs **LINQ to XML**.

---

## 4. ASP.NET Core: Desenvolvimento Web

### 4.1 Estrutura de um Projeto ASP.NET Core

* **Templates Comuns**:

  * `webapi`: API RESTful sem Views.
  * `mvc`: MVC com Controllers e Views Razor.
  * `razor`: Razor Pages.
  * `blazor`: aplicações SPA em C# (Blazor Server, Blazor WebAssembly).

* **Gerar Projeto**:

  ```bash
  dotnet new webapi -o MinhaApi
  cd MinhaApi
  ```

* **Estrutura de Diretórios**:

  ```text
  MinhaApi/
  ├── Controllers/     # Controllers de API
  ├── Models/          # Modelos de domínio / DTOs
  ├── Data/            # Contexto do EF Core, Migrations
  ├── Services/        # Serviços de negócio, interfaces
  ├── Properties/      # launchSettings.json
  ├── appsettings.json # configurações gerais (ex.: ConnectionStrings)
  ├── Program.cs       # ponto de entrada, configuração de host
  └── Startup.cs       # configuração de serviços e pipeline HTTP
  ```

### 4.2 Configuração de Startup

* **Program.cs / Startup.cs (ASP.NET Core 6+ minimal hosting)**:

  ```csharp
  var builder = WebApplication.CreateBuilder(args);

  // Configurar serviços (DI)
  builder.Services.AddControllers();
  builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("Default")));
  builder.Services.AddScoped<IClienteService, ClienteService>();

  var app = builder.Build();

  // Configurar pipeline de requisição
  if (app.Environment.IsDevelopment())
  {
      app.UseDeveloperExceptionPage();
  }
  app.UseHttpsRedirection();
  app.UseRouting();
  app.UseAuthentication();
  app.UseAuthorization();

  app.MapControllers();
  app.Run();
  ```

* **appsettings.json**:

  ```json
  {
    "ConnectionStrings": {
      "Default": "Server=.;Database=MinhaDb;Trusted_Connection=True;"
    },
    "Logging": {
      "LogLevel": {
        "Default": "Information",
        "Microsoft.AspNetCore": "Warning"
      }
    },
    "AllowedHosts": "*"
  }
  ```

### 4.3 Controllers e Endpoints

* **Exemplo de Controller**:

  ```csharp
  [ApiController]
  [Route("api/[controller]")]
  public class ClientesController : ControllerBase
  {
    private readonly IClienteService _service;
    public ClientesController(IClienteService service) => _service = service;

    [HttpGet]
    public async Task<IActionResult> GetAll()
    {
      var clientes = await _service.ObterTodosAsync();
      return Ok(clientes);
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetById(int id)
    {
      var cliente = await _service.ObterPorIdAsync(id);
      if (cliente == null) return NotFound();
      return Ok(cliente);
    }

    [HttpPost]
    public async Task<IActionResult> Create([FromBody] ClienteDto dto)
    {
      if (!ModelState.IsValid) return BadRequest(ModelState);
      var criado = await _service.CriarAsync(dto);
      return CreatedAtAction(nameof(GetById), new { id = criado.Id }, criado);
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> Update(int id, [FromBody] ClienteDto dto)
    {
      if (id != dto.Id) return BadRequest();
      var atualizado = await _service.AtualizarAsync(dto);
      if (!atualizado) return NotFound();
      return NoContent();
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
      var removido = await _service.RemoverAsync(id);
      if (!removido) return NotFound();
      return NoContent();
    }
  }
  ```

* **Model Validation**: Data Annotations (`[Required]`, `[StringLength]`, `[Range]`, `[EmailAddress]`).

* **Response Types**: `[ProducesResponseType(StatusCodes.Status200OK)]` para documentação.

### 4.4 Middleware Personalizado

* **Definição**:

  ```csharp
  public class LogMiddleware
  {
    private readonly RequestDelegate _next;
    private readonly ILogger<LogMiddleware> _logger;

    public LogMiddleware(RequestDelegate next, ILogger<LogMiddleware> logger)
    {
      _next = next;
      _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
      _logger.LogInformation($"Request: {context.Request.Method} {context.Request.Path}");
      await _next(context);
      _logger.LogInformation($"Response: {context.Response.StatusCode}");
    }
  }
  ```
* **Registro no Pipeline** (`Startup.cs` ou `Program.cs`):

  ```csharp
  app.UseMiddleware<LogMiddleware>();
  ```

---

## 5. Entity Framework Core (EF Core)

### 5.1 Configuração do DbContext

* **Definir DbContext**:

  ```csharp
  public class AppDbContext : DbContext
  {
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    public DbSet<Cliente> Clientes { get; set; }
    public DbSet<Pedido> Pedidos { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
      modelBuilder.Entity<Cliente>(entity =>
      {
        entity.HasKey(c => c.Id);
        entity.Property(c => c.Nome).IsRequired().HasMaxLength(100);
      });

      modelBuilder.Entity<Pedido>(entity =>
      {
        entity.HasKey(p => p.Id);
        entity.Property(p => p.ValorTotal).HasColumnType("decimal(18,2)");
        entity.HasOne(p => p.Cliente)
              .WithMany(c => c.Pedidos)
              .HasForeignKey(p => p.ClienteId);
      });
    }
  }
  ```
* **Injeção de Dependência** (`Startup.cs`):

  ```csharp
  services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(Configuration.GetConnectionString("Default")));
  ```

### 5.2 Migrations e Atualização de Banco

* **Adicionar Migration**:

  ```bash
  dotnet ef migrations add InitialCreate
  ```
* **Atualizar Banco**:

  ```bash
  dotnet ef database update
  ```
* **Ferramentas**: instalar `Microsoft.EntityFrameworkCore.Tools` e `dotnet-ef`.

### 5.3 Tipos de Carregamento (Loading)

* **Eager Loading**: `Include` para relacionamentos.

  ```csharp
  var pedidos = context.Pedidos.Include(p => p.Cliente).ToList();
  ```
* **Lazy Loading**: habilitado via proxies (pacote `Microsoft.EntityFrameworkCore.Proxies`) e configuração `UseLazyLoadingProxies()`.
* **Explicit Loading**: chamar `context.Entry(cliente).Collection(c => c.Pedidos).Load()`.

### 5.4 Consultas Avançadas (LINQ + EF Core)

* **Filtros e Projeções**:

  ```csharp
  var clientesAtivos = context.Clientes
      .Where(c => c.Ativo)
      .Select(c => new { c.Id, c.Nome })
      .ToList();
  ```
* **Consultas Assíncronas**: `ToListAsync()`, `FirstOrDefaultAsync()`, `SingleAsync()`.
* **Stored Procedures / Raw SQL**:

  ```csharp
  var resultados = context.Clientes
      .FromSqlRaw("EXECUTE dbo.ObterClientesAtivos")
      .ToList();
  ```
* **Query Types (EF Core 2.x) / Keyless Entities (EF Core 3+)** para views e consultas sem chave primária.

### 5.5 Transações e Concurrency

* **Transação Explícita**:

  ```csharp
  using var transaction = await context.Database.BeginTransactionAsync();
  try
  {
    // operações de CRUD
    await context.SaveChangesAsync();
    await transaction.CommitAsync();
  }
  catch
  {
    await transaction.RollbackAsync();
    throw;
  }
  ```
* **Controle de Concorrência** (Concurrency Tokens):

  * Adicionar propriedade `[Timestamp] public byte[] RowVersion { get; set; }`.
  * Lidar com `DbUpdateConcurrencyException` ao salvar.

---

## 6. Arquitetura de Aplicações e Design Patterns

### 6.1 Camadas Comuns

* **Domain (Entidades e Regras de Negócio)**
* **Data / Persistence (EF Core, Migrations)**
* **Service / Business Logic**
* **API / Presentation (Controllers, Razor, Blazor)**
* **Shared (DTOs, ViewModels, Utilitários)**

### 6.2 Injeção de Dependência (DI)

* **Built-in DI Container** (Microsoft.Extensions.DependencyInjection)
* **Escopo**:

  * `AddTransient<T>`: nova instância a cada solicitação.
  * `AddScoped<T>`: instância por escopo HTTP (por requisição).
  * `AddSingleton<T>`: instância única durante toda a aplicação.
* **Exemplo**:

  ```csharp
  services.AddScoped<ICustomerRepository, CustomerRepository>();
  services.AddScoped<ICustomerService, CustomerService>();
  ```

### 6.3 Repository e Unit of Work

* **Repository Pattern**: abstrai acesso a dados. Exemplo:

  ```csharp
  public interface IGenericRepository<T> where T : class
  {
    Task<T> GetByIdAsync(int id);
    Task<IEnumerable<T>> GetAllAsync();
    Task AddAsync(T entity);
    void Update(T entity);
    void Delete(T entity);
  }

  public class GenericRepository<T> : IGenericRepository<T> where T : class
  {
    protected readonly AppDbContext _context;
    public GenericRepository(AppDbContext context) => _context = context;

    public async Task<T> GetByIdAsync(int id) => await _context.Set<T>().FindAsync(id);
    public async Task<IEnumerable<T>> GetAllAsync() => await _context.Set<T>().ToListAsync();
    public async Task AddAsync(T entity) => await _context.Set<T>().AddAsync(entity);
    public void Update(T entity) => _context.Set<T>().Update(entity);
    public void Delete(T entity) => _context.Set<T>().Remove(entity);
  }
  ```

* **Unit of Work**: agrupa múltiplos repositórios em uma única transação.

  ```csharp
  public interface IUnitOfWork : IDisposable
  {
    ICustomerRepository Customers { get; }
    IPedidoRepository Pedidos { get; }
    Task<int> CommitAsync();
  }

  public class UnitOfWork : IUnitOfWork
  {
    private readonly AppDbContext _context;
    public ICustomerRepository Customers { get; }
    public IPedidoRepository Pedidos { get; }

    public UnitOfWork(AppDbContext context,
                      ICustomerRepository customers,
                      IPedidoRepository pedidos)
    {
      _context = context;
      Customers = customers;
      Pedidos = pedidos;
    }

    public async Task<int> CommitAsync() => await _context.SaveChangesAsync();
    public void Dispose() => _context.Dispose();
  }
  ```

### 6.4 Service Layer e DTOs

* **Service Layer** encapsula lógica de negócio e orquestra repositórios.

* **DTOs (Data Transfer Objects)**: objetos simples para transferência de dados entre camadas/API.

  ```csharp
  public class ClienteDto
  {
    public int Id { get; set; }
    public string Nome { get; set; }
    public string Email { get; set; }
  }
  ```

* **AutoMapper**: mapeamento automático entre Entidades e DTOs.

  ```csharp
  services.AddAutoMapper(typeof(MappingProfile));

  public class MappingProfile : Profile
  {
    public MappingProfile()
    {
      CreateMap<Cliente, ClienteDto>();
      CreateMap<ClienteDto, Cliente>();
    }
  }
  ```

### 6.5 Design Patterns Comuns

* **Dependency Injection**: desacoplamento e testabilidade.
* **Factory Method / Abstract Factory**: criação de objetos sem expor lógica concreta.
* **Builder**: construção passo a passo de objetos complexos.
* **Decorator**: estender funcionalidade de objetos em tempo de execução.
* **Strategy**: encapsular algoritmos intercambiáveis.
* **Mediator**: comunicação entre objetos via objeto intermediário.
* **Observer**: notificar múltiplos observadores sobre eventos (EventAggregator, IObservable).
* **CQRS e MediatR**: separação de comandos (Writes) e consultas (Reads), extensão de mediator pattern.

  ```csharp
  // Exemplo de Request/Handler com MediatR
  public class ObterClienteQuery : IRequest<ClienteDto> { public int Id { get; set; } }

  public class ObterClienteHandler : IRequestHandler<ObterClienteQuery, ClienteDto>
  {
    private readonly IClienteRepository _repo;
    private readonly IMapper _mapper;
    public ObterClienteHandler(IClienteRepository repo, IMapper mapper) { _repo = repo; _mapper = mapper; }
    public async Task<ClienteDto> Handle(ObterClienteQuery request, CancellationToken token)
    {
      var cliente = await _repo.ObterPorIdAsync(request.Id);
      return _mapper.Map<ClienteDto>(cliente);
    }
  }
  ```

---

## 7. Testes Automatizados

### 7.1 xUnit

* **Instalação**:

  ```bash
  dotnet new xunit -o MinhaApi.Tests
  dotnet add MinhaApi.Tests reference MinhaApi.csproj
  ```

* **Estrutura de Projeto de Teste**:

  ```text
  MinhaApi.Tests/
  ├── Controllers/
  ├── Services/
  ├── Repositories/
  └── MinhaApi.Tests.csproj
  ```

* **Exemplo de Teste de Service**:

  ```csharp
  public class ClienteServiceTests : IClassFixture<DatabaseFixture>
  {
    private readonly IClienteService _service;
    public ClienteServiceTests(DatabaseFixture fixture)
    {
      _service = fixture.ServiceProvider.GetRequiredService<IClienteService>();
    }

    [Fact]
    public async Task CriarCliente_DeveRetornarClienteCriado()
    {
      var dto = new ClienteDto { Nome = "Teste", Email = "teste@exemplo.com" };
      var resultado = await _service.CriarAsync(dto);
      Assert.NotNull(resultado);
      Assert.Equal(dto.Nome, resultado.Nome);
    }
  }
  ```

* **Helpers / Fixtures**:

  * **DatabaseFixture**: configura contexto em memória (InMemoryDatabase) para testes.

  ```csharp
  public class DatabaseFixture : IDisposable
  {
    public ServiceProvider ServiceProvider { get; }
    public DatabaseFixture()
    {
      var services = new ServiceCollection();
      services.AddDbContext<AppDbContext>(options =>
        options.UseInMemoryDatabase("TestDb"));
      services.AddScoped<IClienteRepository, ClienteRepository>();
      services.AddScoped<IClienteService, ClienteService>();
      services.AddAutoMapper(typeof(MappingProfile));
      ServiceProvider = services.BuildServiceProvider();

      // Inicializar dados de teste
      using var scope = ServiceProvider.CreateScope();
      var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();
      context.Clientes.Add(new Cliente { Nome = "Existente", Email = "ex@exemplo.com" });
      context.SaveChanges();
    }

    public void Dispose() => ServiceProvider.Dispose();
  }
  ```

### 7.2 Testes de Integração e Insomnia/Postman

* **Testes de Integração**: usar `WebApplicationFactory<TEntryPoint>` do pacote `Microsoft.AspNetCore.Mvc.Testing`.

  ```csharp
  public class ClientesApiTests : IClassFixture<WebApplicationFactory<Program>>
  {
    private readonly HttpClient _client;
    public ClientesApiTests(WebApplicationFactory<Program> factory)
    {
      _client = factory.CreateClient();
    }

    [Fact]
    public async Task GetAllClientes_DeveRetornar200ELista()
    {
      var response = await _client.GetAsync("/api/clientes");
      response.EnsureSuccessStatusCode();
      var json = await response.Content.ReadAsStringAsync();
      Assert.Contains("[]", json);
    }
  }
  ```

---

## 8. Autenticação e Autorização

### 8.1 Identity e JWT

* **ASP.NET Core Identity**: provê gerenciamento de usuários, roles, cookies de autenticação.

  ```bash
  dotnet add package Microsoft.AspNetCore.Identity.EntityFrameworkCore
  ```

  ```csharp
  services.AddIdentity<Usuario, IdentityRole>()
          .AddEntityFrameworkStores<AppDbContext>()
          .AddDefaultTokenProviders();
  ```

* **JWT Bearer Auth**:

  ```bash
  dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
  ```

  ```csharp
  var key = Encoding.ASCII.GetBytes(Configuration["Jwt:Secret"]);
  services.AddAuthentication(options =>
  {
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
  })
  .AddJwtBearer(options =>
  {
    options.RequireHttpsMetadata = true;
    options.SaveToken = true;
    options.TokenValidationParameters = new TokenValidationParameters
    {
      ValidateIssuer = true,
      ValidateAudience = true,
      ValidateLifetime = true,
      ValidateIssuerSigningKey = true,
      ValidIssuer = Configuration["Jwt:Issuer"],
      ValidAudience = Configuration["Jwt:Audience"],
      IssuerSigningKey = new SymmetricSecurityKey(key)
    };
  });
  ```

* **Gerar Token JWT**:

  ```csharp
  public class AuthService : IAuthService
  {
    private readonly IConfiguration _config;
    public AuthService(IConfiguration config) => _config = config;

    public string GenerateJwtToken(Usuario user)
    {
      var tokenHandler = new JwtSecurityTokenHandler();
      var key = Encoding.ASCII.GetBytes(_config["Jwt:Secret"]);
      var tokenDescriptor = new SecurityTokenDescriptor
      {
        Subject = new ClaimsIdentity(new[]
        {
          new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
          new Claim(ClaimTypes.Email, user.Email)
        }),
        Expires = DateTime.UtcNow.AddHours(2),
        SigningCredentials = new SigningCredentials(new SymmetricSecurityKey(key), SecurityAlgorithms.HmacSha256Signature),
        Issuer = _config["Jwt:Issuer"],
        Audience = _config["Jwt:Audience"]
      };
      var token = tokenHandler.CreateToken(tokenDescriptor);
      return tokenHandler.WriteToken(token);
    }
  }
  ```

### 8.2 Políticas de Autorização (

* **Autorizar por Role**:

  ```csharp
  [Authorize(Roles = "Admin,Gerente")]
  public IActionResult GetAdminData() { /*...*/ }
  ```
* **Políticas Customizadas**:

  ```csharp
  services.AddAuthorization(options =>
  {
    options.AddPolicy("PodeEditarCliente", policy =>
      policy.RequireAssertion(context =>
        context.User.HasClaim("EditCustomer", "True") || context.User.IsInRole("Admin")
      ));
  });
  ```

  ```csharp
  [Authorize(Policy = "PodeEditarCliente")]
  public async Task<IActionResult> Edit(int id) { /*...*/ }
  ```

---

## 9. Logging, Monitoramento e Telemetria

### 9.1 Logging com ILogger

* **Injeção de ILogger<T>**:

  ```csharp
  public class ClienteService : IClienteService
  {
    private readonly ILogger<ClienteService> _logger;
    public ClienteService(ILogger<ClienteService> logger) => _logger = logger;

    public async Task<ClienteDto> ObterPorIdAsync(int id)
    {
      _logger.LogInformation("Obtendo cliente com ID {Id}", id);
      // ...
    }
  }
  ```
* **Configuração de Níveis** em `appsettings.json`:

  ```json
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning",
      "Microsoft.Hosting.Lifetime": "Information"
    }
  }
  ```

### 9.2 Application Insights (Azure)

* **Instalação**:

  ```bash
  dotnet add package Microsoft.ApplicationInsights.AspNetCore
  ```
* **Configuração** em `Program.cs`:

  ```csharp
  builder.Services.AddApplicationInsightsTelemetry(Configuration["APPINSIGHTS_CONNECTIONSTRING"]);
  ```
* Coleta automática de métricas (requests, dependências, exceções).

### 9.3 Prometheus e Grafana

* **Prometheus-net** library para expor métricas:

  ```bash
  dotnet add package prometheus-net.AspNetCore
  ```

  ```csharp
  app.UseRouting();
  app.UseHttpMetrics();
  app.UseEndpoints(endpoints =>
  {
    endpoints.MapControllers();
    endpoints.MapMetrics(); // expõe /metrics
  });
  ```
* **Grafana**: dashboards customizados para visualizar métricas Prometheus.

---

## 10. Deploy e Publicação

### 10.1 Publicação via CLI

* **Publicar para Pasta**:

  ```bash
  dotnet publish -c Release -o ./publish
  ```
* **OPções**:

  * `--self-contained` para gerar executável standalone.
  * `-r <runtime>` para publicar para runtime específico (ex.: `win-x64`, `linux-arm64`).

### 10.2 Dockerização

* **Dockerfile Básico**:

  ```dockerfile
  FROM mcr.microsoft.com/dotnet/aspnet:7.0 AS base
  WORKDIR /app
  EXPOSE 80

  FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build
  WORKDIR /src
  COPY ["MinhaApi/MinhaApi.csproj", "MinhaApi/"]
  RUN dotnet restore "MinhaApi/MinhaApi.csproj"
  COPY . .
  WORKDIR "/src/MinhaApi"
  RUN dotnet build "MinhaApi.csproj" -c Release -o /app/build

  FROM build AS publish
  RUN dotnet publish "MinhaApi.csproj" -c Release -o /app/publish

  FROM base AS final
  WORKDIR /app
  COPY --from=publish /app/publish .
  ENTRYPOINT ["dotnet", "MinhaApi.dll"]
  ```
* **Construir e Executar**:

  ```bash
  docker build -t minhaapi:latest .
  docker run -d -p 8080:80 minhaapi:latest
  ```

### 10.3 Deploy em Azure App Service

* **Configurar Azure CLI**:

  ```bash
  az login
  az group create --name MeuResourceGroup --location "EastUS"
  az appservice plan create --name MeuPlano --resource-group MeuResourceGroup --sku B1 --is-linux
  az webapp create --resource-group MeuResourceGroup --plan MeuPlano --name MinhaApiApp --runtime "DOTNET|7.0"
  ```
* **Deploy via ZIP ou Git**:

  ```bash
  dotnet publish -c Release -o publish
  cd publish
  zip -r ../deploy.zip *
  cd ..
  az webapp deployment source config-zip --resource-group MeuResourceGroup --name MinhaApiApp --src deploy.zip
  ```

### 10.4 CI/CD com GitHub Actions

* **Workflow Exemplo** (`.github/workflows/dotnet.yml`):

  ```yaml
  name: CI/CD
  on:
    push:
      branches: [ main ]
  jobs:
    build_and_deploy:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: Setup .NET
          uses: actions/setup-dotnet@v3
          with:
            dotnet-version: '7.0.x'
        - name: Restore dependencies
          run: dotnet restore
        - name: Build
          run: dotnet build --no-restore --configuration Release
        - name: Test
          run: dotnet test --no-build --verbosity normal
        - name: Publish
          run: dotnet publish --configuration Release --output publish
        - name: Deploy to Azure WebApp
          uses: azure/webapps-deploy@v2
          with:
            app-name: MinhaApiApp
            slot-name: production
            publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
            package: publish
  ```

---

## 11. Segurança e Boas Práticas

1. **Configuration Secrets**: use Azure Key Vault, AWS Secrets Manager ou `dotnet user-secrets` em desenvolvimento.
2. **HTTPS Sempre**: configurar redirecionamento para HTTPS (`app.UseHttpsRedirection()`).
3. **Política de CORS**:

```csharp
builder.Services.AddCors(options =>
{
  options.AddPolicy("CorsPolicy", policy =>
  {
    policy.AllowAnyOrigin()
          .AllowAnyMethod()
          .AllowAnyHeader();
  });
});
app.UseCors("CorsPolicy");
```

4. **Validação de Entrada**: Data Annotations, FluentValidation.
5. **Proteção contra CSRF**: em APIs REST, usar tokens JWT; em MVC, usar `ValidateAntiForgeryToken`.
6. **Proteção contra SQL Injection**: usar parâmetros em queries, evitar string concatenation.
7. **Proteção contra XSS e CORS**: validar e sanitizar dados, definir corretamente cabeçalhos de segurança.
8. **Rate Limiting**: usar `AspNetCoreRateLimit` ou middleware customizado.
9. **Log e Monitoramento**: não logar informações sensíveis (senhas, tokens).
10. **Atualizar Dependências**: use `dotnet outdated` ou ferramentas de scanning de vulnerabilidades (OSSIndex).

---

## 12. Performance e Otimizações

### 12.1 Caching

* **In-Memory Cache**:

  ```csharp
  builder.Services.AddMemoryCache();
  app.UseResponseCaching();

  [ResponseCache(Duration = 60)]
  public IActionResult Get() { /*...*/ }
  ```
* **Distributed Cache (Redis)**:

  ```bash
  dotnet add package Microsoft.Extensions.Caching.StackExchangeRedis
  ```

  ```csharp
  builder.Services.AddStackExchangeRedisCache(options =>
  {
    options.Configuration = Configuration.GetConnectionString("Redis");
    options.InstanceName = "MinhaApiCache_";
  });
  ```

### 12.2 Compilação e Publicação Otimizadas

* **ReadyToRun** (pré-compilação): gera binários otimizados:

  ```bash
  dotnet publish -c Release -p:PublishReadyToRun=true
  ```
* **Trimming**: remove código não utilizado (Linker):

  ```bash
  dotnet publish -c Release -p:PublishTrimmed=true -p:TrimMode=Link
  ```

### 12.3 Pool de Conexões

* **Configurar** `MaxPoolSize` na string de conexão:

  ```json
  "ConnectionStrings": {
    "Default": "Server=.;Database=MinhaDb;User Id=sa;Password=senha;Max Pool Size=100;"
  }
  ```

### 12.4 Profiling e Diagnóstico

* **dotnet trace** e **dotnet-counters** para coletar métricas em tempo real.
* **Visual Studio Profiler**: profiling de CPU, memória.
* **JetBrains dotTrace / dotMemory**: profiling avançado.

---

## 13. Boas Práticas de Código e Arquitetura

1. **Seguir SOLID**: Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion.
2. **Manter Controllers Finos**: delegar lógica de negócio a Services.
3. **Usar DTOs e AutoMapper**: evitar retornar entidades diretamente.
4. **Implementar Health Checks**: usar `Microsoft.Extensions.Diagnostics.HealthChecks`.

```csharp
builder.Services.AddHealthChecks()
  .AddDbContextCheck<AppDbContext>()
  .AddUrlGroup(new Uri("https://google.com"), name: "google");
app.MapHealthChecks("/health");
```

5. **Configurar Logging Estruturado**: usar `Serilog` ou `NLog` para logs estruturados em JSON.
6. **Manter Configurações por Ambiente**: `appsettings.Development.json`, `appsettings.Production.json`, variáveis de ambiente.
7. **Versionamento de API**: usar `AddApiVersioning` e rotas versionadas (`api/v1/clients` vs `api/v2/clients`).
8. **Documentar API**: usar `Swashbuckle.AspNetCore` (Swagger) para gerar docs interativos.

```csharp
builder.Services.AddSwaggerGen(c =>
{
  c.SwaggerDoc("v1", new OpenApiInfo { Title = "Minha API", Version = "v1" });
  var xmlFile = "$\{Assembly.GetExecutingAssembly().GetName().Name}.xml";
  var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
  c.IncludeXmlComments(xmlPath);
});
app.UseSwagger();
app.UseSwaggerUI(c => { c.SwaggerEndpoint("/swagger/v1/swagger.json", "Minha API v1"); });
```

9. **Testes Automáticos**: cobrir Controllers, Services, Repositories e Testes de Integração.
10. **Revisão de Código e CI/CD**: integrar análise estática (`SonarQube`, `Roslyn Analyzers`), testes automatizados e deploy contínuo.

---

## 14. Recursos e Comunidade

* **Documentação Oficial**: [https://docs.microsoft.com/dotnet](https://docs.microsoft.com/dotnet)
* **Repositório GitHub**: [https://github.com/dotnet](https://github.com/dotnet)
* **Pacotes NuGet**: [https://www.nuget.org](https://www.nuget.org)
* **Comunidade**: StackOverflow, GitHub Discussions, Reddit (/r/dotnet), Microsoft Q\&A
* **Conferências**: .NET Conf, Ignite, Build, e meetups locais.

---

## 15. Conclusão

O ecossistema .NET oferece um conjunto robusto de ferramentas, bibliotecas e frameworks para construir aplicações modernas, escaláveis e seguras. Com C#, ASP.NET Core e EF Core, é possível desenvolver desde microserviços e APIs até aplicações web completas e multiplataforma. Seguindo boas práticas, design patterns e utilizando as ferramentas de diagnóstico e testes, você garantirá qualidade, performance e manutenibilidade às suas soluções.
