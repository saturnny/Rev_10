@echo off
echo ========================================
echo Time Tracking - Login Simplificado
echo ========================================
echo.

echo [1/3] Verificando Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Node.js nao encontrado!
    echo Instale em: https://nodejs.org
    pause
    exit /b 1
)
echo ✅ Node.js OK

echo.
echo [2/3] Instalando dependências mínimas...
call npm install express bcryptjs jsonwebtoken ejs dotenv
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar!
    pause
    exit /b 1
)
echo ✅ Dependências OK

echo.
echo [3/3] Iniciando servidor simplificado...
echo.
echo 🚀 SERVIDOR RODANDO!
echo 🌐 Login: http://localhost:3000/login
echo 👤 Admin: adm@teste.com / adm123
echo 👥 User: user@teste.com / user123
echo 🧪 Teste: http://localhost:3000/api/test
echo.
echo 🔓 Este servidor usa usuários hardcoded (garantido funcionar)
echo.
echo Para parar: Pressione CTRL+C
echo ========================================
echo.

node login_simple_server.js
