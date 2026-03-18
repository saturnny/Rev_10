@echo off
echo ========================================
echo Time Tracking - CORREÇÃO DE LOGIN
echo ========================================
echo.

echo [1/4] Verificando Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Node.js nao encontrado!
    pause
    exit /b 1
)
echo ✅ Node.js OK

echo.
echo [2/4] Instalando dependências...
call npm install
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar!
    pause
    exit /b 1
)
echo ✅ Dependências OK

echo.
echo [3/4] Configurando ambiente...
if not exist .env.local (
    echo DATABASE_URL=postgresql://postgres.gxqowlxuyyyfukyfsifn:Qualidados2026%%2A@aws-1-sa-east-1.pooler.supabase.com:6543/postgres > .env.local
    echo SECRET_KEY=your-secret-key-change-this >> .env.local
    echo NODE_ENV=development >> .env.local
    echo PORT=3000 >> .env.local
)
echo ✅ Ambiente configurado

echo.
echo [4/4] Corrigindo login do Supabase...
call node fix_login.js
if %errorlevel% neq 0 (
    echo ERRO: Falha na correção!
    pause
    exit /b 1
)
echo ✅ Login corrigido!

echo.
echo ========================================
echo 🚀 INICIANDO SERVIDOR...
echo.
echo 🌐 Acesse: http://localhost:3000/login
echo 👤 Admin: adm@teste.com / adm123
echo 👥 User: user@teste.com / user123
echo.
echo ✅ LOGIN GARANTIDO PARA FUNCIONAR!
echo ========================================
echo.

call npm run dev
