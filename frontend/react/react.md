**Fundamentos do React**

📌 **JSX**: 

Sintaxe que parece HTML, mas é convertida para JavaScript pelo Babel antes de ser interpretada pelo React.

📌 **Componentes**: 

Funcionais são leves e usam hooks, enquanto de classe possuem métodos de ciclo de vida. Prefira funcionais.

📌 **Props vs. State**: 

Props são imutáveis e passadas de pai para filho. 

State é local e gerenciado pelo próprio componente.

📌 **Ciclo de vida**: 

`useEffect` substitui métodos antigos (`componentDidMount`, `componentDidUpdate`, `componentWillUnmount`).

📌 **Event Handling**: 

React usa Synthetic Events para padronizar eventos entre navegadores e otimizar performance.

---

🔹 **Hooks (Profundamente)**

📌 **useState**: 

Gerencia estados locais reativos, evitando mutações diretas para preservar imutabilidade.

📌 **useEffect**: 

Executa efeitos colaterais. Dependências ajudam a controlar re-renders desnecessários.

📌 **useContext**: 

Substitui prop drilling, permitindo acesso global a estados sem Redux.

📌 **useReducer**: 

Gerencia estados complexos como uma versão simplificada do Redux.

📌 **useRef**: 

Mantém referências ao DOM ou valores persistentes sem re-renderizar o componente.

📌 **Custom Hooks**: 

Encapsula lógica reutilizável para evitar duplicação de código.

---

🔹 **Gerenciamento de Estado**

📌 **Context API**: 

Boa para estados globais pequenos, mas pode causar re-renders excessivos.

📌 **Redux**: 

Centraliza estado global com Actions, Reducers e Middlewares como `redux-thunk` e `redux-saga`.

📌 **Recoil/Zustand/Jotai**: 

Alternativas leves ao Redux, mais simples e eficientes.

---

🔹 **Renderização e Performance**

📌 **Virtual DOM**: 

Minimiza manipulação real do DOM, melhorando a performance da UI.

📌 **Otimização**: 

Use `React.memo`, `useMemo` e `useCallback` para evitar re-renders desnecessários.

📌 **Lazy Loading & Code Splitting**: 

`React.lazy` e `Suspense` carregam componentes sob demanda, reduzindo carga inicial.

📌 **Keys em listas**: 

Evitam re-renderizações erradas, garantindo identificação única dos itens.

---

🔹 **Arquitetura e Padrões de Projeto**

📌 **Componentização**: 

Atomic Design organiza componentes em átomos, moléculas, organismos, templates e páginas.

📌 **HOCs & Render Props**: 

Padrões para compartilhar lógica entre componentes sem duplicação de código.

📌 **Estrutura de código**: 

Feature-based e Domain-driven facilitam escalabilidade e manutenção.

---

🔹 **Integração com APIs**

📌 **Fetch vs. Axios**: 

Axios tem melhor suporte a interceptors e resposta automática em JSON, mas Fetch é nativo.

📌 **GraphQL**: 

Reduz overfetching e underfetching, permitindo obter apenas os dados necessários.

📌 **WebSockets**: 

Comunicação bidirecional em tempo real, útil para chats e notificações.

📌 **SWC (Server Components)**: 

Renderiza no servidor para melhor performance no Next.js.

---

🔹 **Testes no React**

📌 **Jest & Testing Library**: 

Testes unitários e de integração focados na experiência do usuário.

📌 **Cypress & Playwright**: 

Testes E2E para garantir funcionamento completo da aplicação.

📌 **Mocking de APIs**: 

Simula requisições para evitar dependências externas nos testes.

---

🔹 **Next.js (se aplicável)**

📌 **SSR vs. SSG vs. ISR**: 

SSR gera páginas no servidor, SSG pré-renderiza estáticas, ISR combina ambos.

📌 **Middleware & API Routes**: 

Permitem lógica backend dentro do Next.js sem precisar de um servidor separado.

📌 **App Router & Server Actions**: 

Novo modelo de React Server Components melhora renderização e eficiência.

---

🔹 **Acessibilidade e UI**

📌 **ARIA Attributes**: 

Melhoram acessibilidade para leitores de tela e navegação por teclado.

📌 **Lighthouse & Web Vitals**: 

Avaliam performance, acessibilidade e SEO da aplicação.

📌 **Animações**: 

`Framer Motion` e `React Spring` criam animações fluidas e performáticas.

---

🔹 **Segurança e Boas Práticas**

📌 **XSS & CSRF**: 

Use `dangerouslySetInnerHTML` com cuidado e proteja endpoints contra requisições maliciosas.

📌 **Vazamento de estado**: 

Evite armazenar tokens e informações sensíveis no frontend.

📌 **Autenticação segura**: 

JWT para autenticação stateless, OAuth para login em serviços externos.

📌 **Proteção de rotas**: 

Use Guards ou Higher-Order Components para restringir acesso a páginas.

---

## **Fundamentos do React**

📌 **JSX** (Transpilado pelo Babel para JavaScript)

```jsx
jsx
CopiarEditar
const element = <h1>Hello, React!</h1>; // JSX
ReactDOM.createRoot(document.getElementById("root")).render(element);

```

📌 **Componentes** (Funcionais vs. Classe)

```jsx
jsx
CopiarEditar
// Componente Funcional (Recomendado)
const Welcome = ({ name }) => <h1>Olá, {name}!</h1>;

// Componente de Classe (Desencorajado)
class WelcomeClass extends React.Component {
  render() {
    return <h1>Olá, {this.props.name}!</h1>;
  }
}

```

📌 **Props vs. State**

```jsx
jsx
CopiarEditar
const Counter = () => {
  const [count, setCount] = React.useState(0);
  return <button onClick={() => setCount(count + 1)}>Contador: {count}</button>;
};

```

📌 **Ciclo de Vida vs. useEffect**

```jsx
// Classe
class LifeCycle extends React.Component {
  componentDidMount() { console.log("Montado"); }
  componentDidUpdate() { console.log("Atualizado"); }
  componentWillUnmount() { console.log("Desmontado"); }
}

// Hook
const EffectExample = () => {
  React.useEffect(() => {
    console.log("Montado ou Atualizado");
    return () => console.log("Desmontado");
  }, []);
};

```

📌 **Event Handling**

```jsx
jsx
CopiarEditar
const Button = () => {
  const handleClick = (event) => console.log("Clicado!", event);
  return <button onClick={handleClick}>Clique aqui</button>;
};

```

---

## 🔹 **Hooks (Profundamente)**

📌 **useState**

```jsx
jsx
CopiarEditar
const Counter = () => {
  const [count, setCount] = React.useState(0);
  return <button onClick={() => setCount(count + 1)}>Contador: {count}</button>;
};

```

📌 **useEffect**

```jsx
jsx
CopiarEditar
const Timer = () => {
  React.useEffect(() => {
    const interval = setInterval(() => console.log("Rodando..."), 1000);
    return () => clearInterval(interval); // Cleanup
  }, []);
};

```

📌 **useContext**

```jsx
jsx
CopiarEditar
const ThemeContext = React.createContext("light");
const ThemedButton = () => {
  const theme = React.useContext(ThemeContext);
  return <button className={theme}>Botão {theme}</button>;
};

```

📌 **useReducer**

```jsx
jsx
CopiarEditar
const reducer = (state, action) => (action.type === "increment" ? state + 1 : state);
const Counter = () => {
  const [count, dispatch] = React.useReducer(reducer, 0);
  return <button onClick={() => dispatch({ type: "increment" })}>Contador: {count}</button>;
};

```

📌 **useRef**

```jsx
jsx
CopiarEditar
const InputFocus = () => {
  const inputRef = React.useRef(null);
  return <input ref={inputRef} onClick={() => inputRef.current.focus()} />;
};

```

📌 **Custom Hook**

```jsx
jsx
CopiarEditar
const useToggle = (initialState = false) => {
  const [state, setState] = React.useState(initialState);
  const toggle = () => setState(!state);
  return [state, toggle];
};

const ToggleComponent = () => {
  const [isOn, toggle] = useToggle();
  return <button onClick={toggle}>{isOn ? "ON" : "OFF"}</button>;
};

```

---

## 🔹 **Gerenciamento de Estado**

📌 **Context API**

```jsx
jsx
CopiarEditar
const ThemeContext = React.createContext("light");
const App = () => (
  <ThemeContext.Provider value="dark">
    <ThemedButton />
  </ThemeContext.Provider>
);

```

📌 **Redux (Redux Toolkit)**

```jsx
jsx
CopiarEditar
import { configureStore, createSlice } from "@reduxjs/toolkit";
const counterSlice = createSlice({
  name: "counter",
  initialState: 0,
  reducers: { increment: (state) => state + 1 },
});
export const { increment } = counterSlice.actions;
export const store = configureStore({ reducer: counterSlice.reducer });

```

---

## 🔹 **Renderização e Performance**

📌 **React.memo**

```jsx
jsx
CopiarEditar
const MemoizedComponent = React.memo(({ count }) => {
  console.log("Renderizou");
  return <div>{count}</div>;
});

```

📌 **Lazy Loading e Suspense**

```jsx
jsx
CopiarEditar
const LazyComponent = React.lazy(() => import("./LazyComponent"));
const App = () => (
  <React.Suspense fallback={<div>Carregando...</div>}>
    <LazyComponent />
  </React.Suspense>
);

```

---

## 🔹 **Arquitetura e Padrões de Projeto**

📌 **HOC (High Order Component)**

```jsx
jsx
CopiarEditar
const withLogger = (Component) => (props) => {
  console.log("Renderizando", props);
  return <Component {...props} />;
};

```

---

## 🔹 **Integração com APIs**

📌 **Fetch vs. Axios**

```jsx
jsx
CopiarEditar
const fetchData = async () => {
  const response = await fetch("https://jsonplaceholder.typicode.com/todos/1");
  const data = await response.json();
  console.log(data);
};

```

📌 **GraphQL com Apollo**

```jsx
jsx
CopiarEditar
import { useQuery, gql } from "@apollo/client";
const GET_DATA = gql`{ user(id: 1) { name } }`;
const User = () => {
  const { data } = useQuery(GET_DATA);
  return <div>{data?.user.name}</div>;
};

```

---

## 🔹 **Testes no React**

📌 **Jest & Testing Library**

```jsx
jsx
CopiarEditar
import { render, screen } from "@testing-library/react";
test("Renderiza botão", () => {
  render(<button>Click</button>);
  expect(screen.getByText("Click")).toBeInTheDocument();
});

```

---

## 🔹 **Next.js (se aplicável)**

📌 **SSR vs. SSG**

```jsx
jsx
CopiarEditar
export async function getServerSideProps() {
  const res = await fetch("https://jsonplaceholder.typicode.com/todos/1");
  const data = await res.json();
  return { props: { data } };
}
const Page = ({ data }) => <div>{data.title}</div>;

```

---

## 🔹 **Segurança e Boas Práticas**

📌 **Evitar XSS**

```jsx
jsx
CopiarEditar
const sanitize = (html) => ({ __html: DOMPurify.sanitize(html) });
const SafeComponent = ({ unsafeHtml }) => <div dangerouslySetInnerHTML={sanitize(unsafeHtml)} />;

```

📌 **JWT Auth**

```jsx
jsx
CopiarEditar
const login = async (credentials) => {
  const response = await fetch("/api/login", {
    method: "POST",
    body: JSON.stringify(credentials),
  });
  const { token } = await response.json();
  localStorage.setItem("jwt", token);
};
```