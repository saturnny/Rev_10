@echo off
echo ========================================
echo Time Tracking - BOOTSTRAP COMPLETO
echo ========================================
echo.

echo [1/5] Verificando Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Node.js nao encontrado!
    pause
    exit /b 1
)
echo ✅ Node.js OK

echo.
echo [2/5] Instalando dependências...
call npm install
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar!
    pause
    exit /b 1
)
echo ✅ Dependências OK

echo.
echo [3/5] Configurando ambiente...
if not exist .env.local (
    echo DATABASE_URL=postgresql://postgres.gxqowlxuyyyfukyfsifn:Qualidados2026%%2A@aws-1-sa-east-1.pooler.supabase.com:6543/postgres > .env.local
    echo SECRET_KEY=your-secret-key-change-this >> .env.local
    echo NODE_ENV=development >> .env.local
    echo PORT=3000 >> .env.local
)
echo ✅ Ambiente configurado

echo.
echo [4/5] Atualizando Bootstrap...
call node atualizar_bootstrap.js
if %errorlevel% neq 0 (
    echo ERRO: Falha na atualização!
    pause
    exit /b 1
)
echo ✅ Bootstrap atualizado

echo.
echo [5/5] Resetando senhas e iniciando...
call node reset_senhas.js
if %errorlevel% neq 0 (
    echo ERRO: Falha ao resetar senhas!
    pause
    exit /b 1
)
echo ✅ Senhas resetadas

echo.
echo ========================================
echo 🎨 SISTEMA COMPLETO!
echo.
echo 🌐 Acesse: http://localhost:3000/login
echo 👤 Admin: adm@teste.com / adm123
echo 👥 User: user@teste.com / user123
echo.
echo ✅ BOOTSTRAP RESTAURADO!
echo ✅ ESTILIZAÇÃO COMPLETA!
echo ✅ LAYOUT RESPONSIVO!
echo ========================================
echo.

call npm run dev
