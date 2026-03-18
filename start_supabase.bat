@echo off
echo ========================================
echo Time Tracking System - Supabase Version
echo ========================================
echo.

echo [1/3] Verificando Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Node.js nao encontrado!
    echo Instale Node.js em: https://nodejs.org
    pause
    exit /b 1
)
echo ✅ Node.js encontrado

echo.
echo [2/3] Instalando dependencias...
call npm install
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar dependencias!
    pause
    exit /b 1
)
echo ✅ Dependencias instaladas

echo.
echo [3/3] Configurando ambiente...
if not exist .env.local (
    echo Criando .env.local com Supabase...
    (
        echo DATABASE_URL=postgresql://postgres.gxqowlxuyyyfukyfsifn:Qualidados2026%%2A@aws-1-sa-east-1.pooler.supabase.com:6543/postgres
        echo SECRET_KEY=your-secret-key-change-this
        echo NODE_ENV=development
        echo PORT=3000
    ) > .env.local
)
echo ✅ Ambiente configurado com Supabase

echo.
echo ========================================
echo 🚀 INICIANDO SERVIDOR...
echo.
echo 🌐 Acesse: http://localhost:3000/login
echo 👤 Admin: adm@teste.com / adm123
echo 👥 User: user@teste.com / user123
echo.
echo Para parar: Pressione CTRL+C
echo ========================================
echo.

call npm run dev
