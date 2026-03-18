# 🚨 ERRO 500 - SOLUÇÃO RÁPIDA

## Problema: FUNCTION_INVOCATION_FAILED

O erro 500 indica que as variáveis de ambiente não estão configuradas no Vercel.

## 🔧 SOLUÇÃO IMEDIATA:

### 1. Acessar Painel Vercel
- Vá para: https://vercel.com
- Entre no projeto `rev-10`

### 2. Configurar Variáveis de Ambiente
- **Settings** → **Environment Variables**
- Adicione estas variáveis:

```
DATABASE_URL
postgresql://postgres.wqcdytvuwoagaqhdgkfl:node@VersionHhMAIN@aws-1-sa-east-1.pooler.supabase.com:6543/postgres
```

```
SECRET_KEY
sua-chave-super-secreta-aqui-mudar-necessario
```

```
ALGORITHM
HS256
```

```
ACCESS_TOKEN_EXPIRE_MINUTES
30
```

```
NODE_ENV
production
```

### 3. Redeploy Automático
- Após salvar, o Vercel fará redeploy automaticamente
- Aguarde 2-3 minutos

### 4. Testar
```bash
curl https://rev-10.vercel.app/api/test
```

## 🎯 Resultado Esperado:

**Antes (Erro 500):**
```json
{
  "msg": "erro na conexão",
  "status": "error",
  "database": "disconnected"
}
```

**Depois (Sucesso):**
```json
{
  "msg": "deploy funcionando", 
  "status": "ok",
  "database": "connected",
  "env": "production"
}
```

## 🌐 URLs para Testar:

- **API Test**: https://rev-10.vercel.app/api/test
- **Login**: https://rev-10.vercel.app/login
- **Dashboard**: https://rev-10.vercel.app/dashboard

## ⚠️ IMPORTANTE:

Sem as variáveis de ambiente, a aplicação NÃO FUNCIONA no Vercel.

**O erro 500 é normal quando as variáveis não estão configuradas!**

## 🚀 Após Configurar:

Seu app estará 100% funcional com:
- ✅ Banco de dados conectado
- ✅ Autenticação JWT funcionando
- ✅ Sistema completo online
