@echo off
echo ========================================
echo Time Tracking - RESET DE SENHAS
echo ========================================
echo.

echo [1/3] Verificando Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Node.js nao encontrado!
    pause
    exit /b 1
)
echo ✅ Node.js OK

echo.
echo [2/3] Resetando senhas no Supabase...
call node reset_senhas.js
if %errorlevel% neq 0 (
    echo ERRO: Falha ao resetar senhas!
    pause
    exit /b 1
)
echo ✅ Senhas resetadas com sucesso!

echo.
echo [3/3] Iniciando servidor...
echo.
echo ========================================
echo 🚀 SISTEMA PRONTO!
echo.
echo 🌐 Acesse: http://localhost:3000/login
echo 👤 Admin: adm@teste.com / adm123
echo 👥 User: user@teste.com / user123
echo.
echo ✅ SENHAS GARANTIDAS PARA FUNCIONAR!
echo ========================================
echo.

call npm run dev
