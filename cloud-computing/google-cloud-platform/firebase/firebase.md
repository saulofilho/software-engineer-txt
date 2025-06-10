# Guia Completo de Firebase

Este guia apresenta, de forma detalhada e avançada, o **Firebase**, a plataforma de desenvolvimento de aplicações móveis e web do Google, cobrindo seus principais produtos, arquitetura, SDKs, práticas recomendadas, segurança, CI/CD e exemplos práticos.

---

## 1. Visão Geral do Firebase

* **Firebase** é uma plataforma Backend-as-a-Service (BaaS) que oferece um conjunto integrado de serviços para acelerar o desenvolvimento de apps:

  * **Autenticação** (Auth)
  * **Banco de dados em tempo real** (Realtime Database)
  * **Firestore** (NoSQL de próxima geração)
  * **Cloud Functions** (Funções serverless)
  * **Hosting** (Hospedagem estática)
  * **Cloud Storage** (Armazenamento de arquivos)
  * **Cloud Messaging** (FCM para notificações)
  * **Analytics**, **Performance Monitoring**, **Crashlytics**
  * **Remote Config**, **A/B Testing**, **App Distribution**
* Integração nativa com Google Cloud Platform e escalabilidade automática.

---

## 2. Configuração Inicial

1. **Criar projeto no Firebase Console** ([https://console.firebase.google.com](https://console.firebase.google.com)).
2. **Registrar apps** (iOS, Android, Web) e obter credenciais (
   `google-services.json`, `GoogleService-Info.plist`, configuração JS).
3. **Instalar Firebase CLI**:

   ```bash
   npm install -g firebase-tools
   firebase login
   firebase init
   ```

   * Selecione produtos (Hosting, Firestore, Functions, Emulators).
   * Configure diretórios e regras de segurança.

---

## 3. Autenticação (Firebase Auth)

### 3.1 Métodos de Login Suportados

* **Email/Senha**
* **Provedores OAuth**: Google, Facebook, Twitter, GitHub
* **Telefone (SMS OTP)**
* **Login Anônino**
* **SAML / OpenID Connect** para identidade corporativa

### 3.2 Exemplo de Login com Email/Senha (Web)

```js
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from 'firebase/auth';
const auth = getAuth();

// Registrar
await createUserWithEmailAndPassword(auth, email, password);
// Logar
await signInWithEmailAndPassword(auth, email, password);
```

---

## 4. Realtime Database vs Firestore

| Aspecto        | Realtime Database              | Firestore                          |
| -------------- | ------------------------------ | ---------------------------------- |
| Modelo         | JSON tree                      | Coleções / Documentos (NoSQL)      |
| Escalabilidade | Vertical (shards via location) | Horizontal (multi-region, shards)  |
| Consultas      | Simples, em toda árvore        | Rich queries, índices compostos    |
| Offline        | Suporte básico                 | Suporte avançado, SDK completo     |
| Transações     | Limitadas                      | ACID multi-documento               |
| Preço          | GB/mês, download, conexões     | GB/mês, leituras/escritas por 100k |

---

## 5. Cloud Firestore

### 5.1 Operações Básicas (Web SDK)

```js
import { getFirestore, doc, setDoc, getDoc, collection, addDoc, query, where, getDocs } from 'firebase/firestore';
const db = getFirestore();

// Criar/Atualizar\await setDoc(doc(db, 'users', 'alice'), { age: 30 });
// Adicionar auto-ID
await addDoc(collection(db, 'posts'), { title: 'Olá', body: '...' });
// Ler documento
const snap = await getDoc(doc(db, 'users', 'alice'));
// Consultas
const q = query(collection(db, 'posts'), where('title', '==', 'Olá'));
const posts = await getDocs(q);
```

### 5.2 Regras de Segurança

```js
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // Usuário só lê/escreve seu próprio perfil
    match /users/{userId} {
      allow read, write: if request.auth.uid == userId;
    }

    // Coleção posts pública leitura, só autor pode escrever
    match /posts/{postId} {
      allow read: if true;
      allow write: if request.auth.uid == resource.data.authorId;
    }
  }
}
```

---

## 6. Realtime Database

### 6.1 Operações Básicas (Web SDK)

```js
import { getDatabase, ref, set, get, onValue } from 'firebase/database';
const rtdb = getDatabase();

// Escrever
await set(ref(rtdb, 'users/alice'), { age: 30 });
// Ler
const snap = await get(ref(rtdb, 'users/alice'));
// Escutar
onValue(ref(rtdb, 'posts'), snapshot => { console.log(snapshot.val()); });
```

### 6.2 Regras de Segurança

```json
{
  "rules": {
    "users": {
      "$uid": {
        ".read": "$uid === auth.uid",
        ".write": "$uid === auth.uid"
      }
    }
  }
}
```

---

## 7. Cloud Functions

* Execução serverless em Node.js/Typescript.
* **Triggers**:

  * **HTTP** (`onRequest`)
  * **Firestore** (`onCreate`, `onUpdate`)
  * **Auth** (`user().onCreate`)
  * **Pub/Sub**, **Storage**, **Analytics**

### 7.1 Exemplo HTTP Function (Typescript)

```ts
import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';
admin.initializeApp();

export const hello = functions.https.onRequest((req, res) => {
  res.send('Olá do Cloud Function!');
});
```

---

## 8. Hosting e Deploy

```bash
firebase deploy --only hosting                       # só hosting
firebase deploy --only firestore,functions           # só BD e funções
firebase deploy                                     # tudo
```

* **CLI** configura canal, targets e deploy preview.

---

## 9. Cloud Storage

### 9.1 Upload/Download (Web SDK)

```js
import { getStorage, ref as sref, uploadBytes, getDownloadURL } from 'firebase/storage';
const storage = getStorage();
const fileRef = sref(storage, 'uploads/image.png');
await uploadBytes(fileRef, file);
const url = await getDownloadURL(fileRef);
```

### 9.2 Regras de Segurança

```js
service firebase.storage {
  match /b/{bucket}/o {
    match /uploads/{userId}/{allPaths=**} {
      allow read;
      allow write: if request.auth.uid == userId;
    }
  }
}
```

---

## 10. Cloud Messaging (FCM)

* **Push notifications** para iOS, Android e Web.
* **Server SDK** (Node, Java, Python) para envio de mensagens.

```js
import * as admin from 'firebase-admin';
admin.messaging().send({
  token: deviceToken,
  notification: { title: 'Olá', body: 'Mensagem FCM' }
});
```

---

## 11. Analytics, Performance e Crashlytics

* **Analytics**: eventos customizados (`logEvent`).
* **Performance Monitoring**: traces, HTTP/S network tracing.
* **Crashlytics**: coleta e relatório de falhas em apps móveis.

---

## 12. Emuladores e Desenvolvimento Local

```bash
firebase emulators:start --only auth,firestore,functions,hosting
```

* Teste com SDK apontando para portas dos emuladores.

---

## 13. Integração CI/CD

* **GitHub Actions**:

  ```yaml
  - uses: w9jds/firebase-action@v2
    with:
      args: deploy --only hosting,firestore,functions
    env:
      FIREBASE_TOKEN: ${{ secrets.FIREBASE_TOKEN }}
  ```
* **Fastlane** para apps iOS/Android integrando Crashlytics e App Distribution.

---

## 14. Boas Práticas e Considerações

1. **Gerenciar Regras de Segurança**: versionar `firestore.rules` e `storage.rules`.
2. **Estratégia de Indexação** no Firestore: defina índices compostos em `firestore.indexes.json`.
3. **Limitar leituras e gravações**: paginar consultas e usar `limit()`, `where()`.
4. **Manter SDKs atualizados** para obter correções de segurança.
5. **Use Tokens Customizados** para controlar claims adicionais.
6. **Monitore Cotas** e orçamentos do projeto.
7. **Tenha estratégia de backup**: exportação periódica do Firestore.
8. **Use Cloud Functions com moderação**: planos pagos consideram invocações.

---

## 15. Conclusão

Firebase fornece um ecossistema completo para desenvolvimento rápido de apps escaláveis, integrando autenticação, banco de dados, funções serverless, hosting e observabilidade. Dominar seus serviços, segurança e pipelines CI/CD é essencial para construir produtos robustos e ágeis.
