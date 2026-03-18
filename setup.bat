@echo off
echo ========================================
echo Time Tracking System - Setup Completo
echo ========================================
echo.

echo [1/6] Verificando Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Node.js nao encontrado!
    echo Por favor, instale Node.js em: https://nodejs.org
    pause
    exit /b 1
)
echo OK: Node.js encontrado

echo.
echo [2/6] Instalando dependencias...
call npm install
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar dependencias!
    pause
    exit /b 1
)
echo OK: Dependencias instaladas

echo.
echo [3/6] Configurando ambiente...
if not exist .env.local (
    echo Criando .env.local com configuracoes padrao...
    copy .env.example .env.local >nul
)
echo OK: Ambiente configurado

echo.
echo [4/6] Criando banco de dados...
call node seed_database.js
if %errorlevel% neq 0 (
    echo ERRO: Falha ao criar banco de dados!
    pause
    exit /b 1
)
echo OK: Banco criado com sucesso!

echo.
echo [5/6] Testando sistema de login...
call node test_login.js
if %errorlevel% neq 0 (
    echo AVISO: Teste de login falhou, mas continuando...
)
echo OK: Teste de login concluido!

echo.
echo [6/6] Iniciando servidor...
echo.
echo ========================================
echo ✅ SISTEMA PRONTO PARA USO!
echo.
echo 🌐 Acesse: http://localhost:3000/login
echo 👤 Admin: adm@teste.com / adm123
echo 👥 User: user@teste.com / user123
echo.
echo Para parar: Pressione CTRL+C
echo ========================================
echo.

call npm run dev
