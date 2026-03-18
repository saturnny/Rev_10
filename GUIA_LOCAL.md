# 🚀 GUIA RÁPIDO - RODAR LOCALMENTE

## 📋 PRÉ-REQUISITOS
- Node.js instalado (https://nodejs.org)
- Terminal/CMD aberto na pasta do projeto

## 🎯 PASSO ÚNICO: EXECUTAR O SCRIPT

### **Windows (Recomendado):**
```cmd
start.bat
```

### **Manual (se start.bat falhar):**
```bash
# 1. Instalar dependências
npm install

# 2. Iniciar servidor
npm run dev
```

## 🌐 ACESSAR APLICAÇÃO

### **URLs:**
- **Principal**: http://localhost:3000
- **Login**: http://localhost:3000/login
- **Dashboard**: http://localhost:3000/dashboard
- **Health Check**: http://localhost:3000/api/test

### **Credenciais de Teste:**
| Tipo | Email | Senha |
|------|-------|-------|
| Admin | adm@teste.com | adm123 |
| Usuário | user@teste.com | user123 |

## 🛠️ COMANDOS ÚTEIS

```bash
# Instalar dependências
npm install

# Rodar desenvolvimento (com auto-reload)
npm run dev

# Rodar produção
npm start

# Popular banco de dados
npm run seed

# Instalar tudo em um comando
npm run install-deps
```

## 🔧 ARQUIVOS CRIADOS

- ✅ `.env.local` - Variáveis ambiente local
- ✅ `.gitignore` - Ignorar arquivos sensíveis
- ✅ `start.bat` - Script automático Windows
- ✅ `package.json` - Dependências atualizadas

## 📱 TESTE RÁPIDO

1. **Execute**: `start.bat`
2. **Aguarde**: Instalação das dependências
3. **Acesse**: http://localhost:3000
4. **Faça login**: adm@teste.com / adm123
5. **Teste o dashboard**

## 🚀 DEPLOY NO VERCEL

1. **Teste local**: Confirme que tudo funciona
2. **Commit**: `git add . && git commit -m "Ready for deploy"`
3. **Push**: `git push origin main`
4. **Aguarde**: Deploy automático no Vercel

## 🎯 RESULTADO ESPERADO

### **Health Check:**
```json
{"msg": "deploy funcionando", "status": "ok"}
```

### **Após Login:**
- Dashboard com estatísticas
- Menu de navegação
- Funcionalidades completas

## 🆘️ SOLUÇÃO DE PROBLEMAS

### **Se `start.bat` não funcionar:**
```bash
# Manualmente
npm install
npm run dev
```

### **Se der erro de Node.js:**
1. Instale Node.js: https://nodejs.org
2. Reinicie o terminal
3. Tente novamente

### **Se der erro de porta:**
```bash
# Mudar porta (no .env.local)
PORT=3001
```

### **Se der erro de banco:**
1. Configure Supabase local
2. Use banco em memória para teste
3. Ignore erros de banco inicialmente

## 🎉 PRONTO PARA DEPLOY!

Quando tudo funcionar localmente:
1. ✅ **Teste completo** OK
2. ✅ **Funcionalidades** OK  
3. ✅ **Deploy Vercel** GARANTIDO

**Sua aplicação está pronta para produção!** 🚀
