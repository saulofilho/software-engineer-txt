# Guia Completo de Flutter

Este guia aborda, em nível avançado, o **Flutter** e o ecossistema Dart para desenvolvimento de aplicações nativas multiplataforma (iOS, Android, web, desktop), cobrindo arquitetura, widgets, gerenciamento de estado, navegação, integração, testes, performance, deploy e boas práticas.

---

## 1. Visão Geral do Flutter

* **Flutter** é um SDK open source do Google para UI multiplataforma, escrito em **Dart**.
* Compila nativamente para ARM e x86, e para web via JavaScript.
* **Motor de renderização** próprio (Skia), permitindo interfaces declarativas e alta performance.

---

## 2. Fundamentos de Dart

### 2.1 Tipos e Null Safety

```dart
void main() {
  String name = 'Flutter';         // não nulo
  String? maybe;                   // pode ser nulo
  int count = 0;
  final double pi = 3.1415;        // imutável
}
```

### 2.2 Estruturas de Controle e Futures

```dart
Future<String> fetchData() async {
  await Future.delayed(Duration(seconds: 1));
  return 'data';
}

void example() async {
  try {
    var result = await fetchData();
  } catch (e) {
    print('Erro: \$e');
  }
}
```

---

## 3. Arquitetura Flutter

### 3.1 Widgets

* **StatelessWidget**: UI imutável.
* **StatefulWidget**: UI com estado mutável.

```dart
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Text('Olá, Flutter!');
  }
}
```

### 3.2 Árvore de Widgets

* Composição de widgets confere desempenho e reutilização.
* **Element Tree** e **Render Tree** internamente.

---

## 4. Gerenciamento de Estado

| Abordagem           | Descrição                                           | Quando usar                          |
| ------------------- | --------------------------------------------------- | ------------------------------------ |
| **setState**        | Estado local simples                                | Widgets pequenos                     |
| **InheritedWidget** | Pares de contexto descendente                       | Fluxo de dados legível               |
| **Provider**        | Abstração sobre InheritedWidget                     | App médio, fácil adoção              |
| **Riverpod**        | Provider reescrito, sem dependência de BuildContext | Escalável, testável                  |
| **Bloc / Cubit**    | Streams e eventos                                   | Arquitetura reativa, testes robustos |
| **GetX**            | Minimalista, reatividade automática                 | Prototipagem rápida                  |

---

## 5. Navegação e Rotas

### 5.1 Navigator 1.0

```dart
Navigator.pushNamed(context, '/details', arguments: id);
```

### 5.2 Navigator 2.0 (Router API)

* Para navegação declarativa e URLs sincronizadas.

```dart
final router = Router(
  routerDelegate: MyRouterDelegate(),
  routeInformationParser: MyRouteInformationParser(),
);
```

---

## 6. Persistência e Banco de Dados

| Solução           | Tipo                  | Biblioteca               |
| ----------------- | --------------------- | ------------------------ |
| SQLite            | Relacional embutido   | sqflite                  |
| Hive              | NoSQL leve em memória | hive, hive\_flutter      |
| Drift / Moor      | ORM para SQLite       | drift                    |
| SharedPreferences | Key-Value             | shared\_preferences      |
| Secure Storage    | Key-Value seguro      | flutter\_secure\_storage |

---

## 7. Integração com Backend

* **HTTP / REST**: `http`, `dio`.
* **gRPC**: suporte via `grpc` e `grpc_google`.
* **GraphQL**: `graphql_flutter`.
* **WebSockets**: `web_socket_channel` ou `socket_io_client`.

---

## 8. Firebase & Serviços de Nuvem

* **Autenticação, Firestore, Storage, Functions**: `firebase_auth`, `cloud_firestore`, `firebase_storage`, `cloud_functions`.
* **Configuração**: `flutterfire configure` para adicionar Firebase a todos targets.

---

## 9. Testes e Qualidade

| Nível          | Framework             | Ação                                      |
| -------------- | --------------------- | ----------------------------------------- |
| **Unitário**   | `flutter_test`        | `testWidgets`, `test`                     |
| **Widget**     | `flutter_test`        | Testar UI em isolamento                   |
| **Integração** | `integration_test`    | Testes end-to-end em dispositivo/emulador |
| **Mocking**    | `mockito`, `mocktail` | Simular dependências                      |

---

## 10. Performance e Otimizações

1. **Evitar rebuilds**: use `const` widgets.
2. **Profiling**: Flutter DevTools (CPU, memória, rendering).
3. **Imagens**: compressão e lazy loading com `cached_network_image`.
4. **Listas longas**: `ListView.builder`, `ReorderableListView`.
5. **Isolates**: processar tarefas pesadas fora do thread principal.

---

## 11. Internacionalização (i18n)

* **Flutter Intl** ou `flutter_localizations`.
* Arquivos ARB em `lib/l10n/`, gerados pelo `intl_utils`.

```yaml
# pubspec.yaml
flutter:
  generate: true
  localization:
    arb-dir: lib/l10n
    template-arb-file: app_en.arb
```

---

## 12. CI/CD e Deploy

* **Codemagic**, **GitHub Actions**, **Bitrise**.
* **Comandos**:

  ```bash
  flutter build apk --release
  flutter build ios --release
  flutter build web --release
  ```
* **Distribuição**: Play Store, App Store, Firebase App Distribution.

---

## 13. Boas Práticas

1. **Arquitetura limpa**: Layers (Presentation, Domain, Data).
2. **Dependency Injection**: `get_it`, `injectable`.
3. **Modularização**: Flutter Modules ou Packages.
4. **Linter e Formatador**: `flutter analyze`, `dartfmt`, `flutter format`.
5. **BLoC / Cubit** para lógica de negócio.
6. **Documentar Widgets** e APIs internas.
7. **Atualizar dependências** com `flutter pub outdated`.
8. **Segurança**: validar e sanitizar entradas, HTTPS obrigatório.

---

## 14. Conclusão

O Flutter permite desenvolver interfaces ricas e de alta performance para múltiplas plataformas a partir de uma única codebase. Compreender seu ciclo de vida de widgets, gerenciamento de estado, integrações e pipelines garante a entrega de aplicações robustas e escaláveis.
