---
tags:
  - firebase
  - storage
  - arquivos
fonte: CLAUDE.md
gerado_em: 2026-05-11
secoes:
  - "25.5 Estrutura de arquivos do sistema"
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **firebase** (plugin) — Storage rules, deploy, buckets
> 2. MCP **fabrica-apps** — `rag_buscar("firebase storage")` + `buscar_historico("storage")`

---

### 25.5 Estrutura de arquivos do sistema

```
app/
├── (tabs)/
│   ├── agendamentos.tsx      ← REFATORAR — adicionar funcionária + serviço
│   ├── funcionarias.tsx      ← NOVO — cadastro de funcionárias
│   └── servicos.tsx          ← NOVO — cadastro de serviços com duração
│
└── agendar/
    └── index.tsx             ← NOVO — página pública sem login

functions/SRC/index.ts        ← adicionar enviarConfirmacaoAgendamento
```

---

## Upload de foto de perfil — padrão da fábrica

Erro comum: `storage/unknown`

Causas:
1. Storage não inicializado no Firebase Console (clique em **Get started** em Storage)
2. Regras de Storage **nunca deployadas** (`firebase_get_security_rules` retorna vazio)
3. Bucket URL errada no `.env` (`.appspot.com` vs `.firebasestorage.app`)
4. URI local (`file://`) não convertida para blob (usar `expo-file-system` `File` → `arrayBuffer` → `Blob`)
5. Upload sem `auth.currentUser` ou sem `contentType: image/jpeg`

Solução:
- Sempre converter URI → `File(uri).arrayBuffer()` → `Blob` → `uploadBytes` com metadata
- Bucket: `setmatch-app-fabrica.firebasestorage.app` (projetos 2024+)
- `getStorage(app, 'gs://' + EXPO_PUBLIC_FIREBASE_STORAGE_BUCKET)`
- Regras (`storage.rules`):

```javascript
match /usuarios/{uid}/{allPaths=**} {
  allow read: if request.auth != null;
  allow write: if request.auth != null
    && request.auth.uid == uid
    && request.resource.size < 5 * 1024 * 1024
    && request.resource.contentType.matches('image/.*');
}
```

- Deploy: `firebase_deploy` com `only: storage`

```typescript
// utils/uploadFoto.ts
import { File } from 'expo-file-system';
import { ref, uploadBytes, getDownloadURL } from 'firebase/storage';
import { auth, storage } from './firebaseConfig';

export async function uploadFotoPerfil(uri: string): Promise<string> {
  const user = auth.currentUser;
  if (!user) throw new Error('Não autenticado');

  const file = new File(uri);
  const blob = new Blob([await file.arrayBuffer()], { type: 'image/jpeg' });

  const storageRef = ref(storage, `usuarios/${user.uid}/perfil_${Date.now()}.jpg`);
  await uploadBytes(storageRef, blob, { contentType: 'image/jpeg' });
  return getDownloadURL(storageRef);
}
```