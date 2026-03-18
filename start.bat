@echo off
echo ========================================
echo Time Tracking System - Setup Local
echo ========================================
echo.

echo [1/5] Verificando Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Node.js nao encontrado!
    echo Por favor, instale Node.js em: https://nodejs.org
    pause
    exit /b 1
)
echo OK: Node.js encontrado

echo.
echo [2/5] Instalando dependencias...
call npm install
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar dependencias!
    pause
    exit /b 1
)
echo OK: Dependencias instaladas

echo.
echo [3/5] Configurando ambiente...
if not exist .env.local (
    echo Criando .env.local com configuracoes padrao...
    copy .env.example .env.local >nul
)
echo OK: Ambiente configurado

echo.
echo [4/5] Criando banco de dados...
call node seed_database.js
if %errorlevel% neq 0 (
    echo AVISO: Erro ao criar banco, mas continuando...
)
echo OK: Banco configurado

echo.
echo [5/5] Iniciando servidor...
echo.
echo Servidor rodando em: http://localhost:3000
echo.
echo Para parar: Pressione CTRL+C
echo.
echo ========================================
echo.

call npm run dev
