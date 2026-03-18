/**
 * Login Simplificado - Sem dependências complexas
 */
require('dotenv').config();
const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.set('view engine', 'ejs');

// Usuários hardcoded para teste (fallback)
const USERS = [
    {
        id: 1,
        nome: 'Administrador',
        email: 'adm@teste.com',
        senha: '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcflJHPF2eBmcVxa5w0d1w7a', // adm123
        tipo_usuario: 'Admin'
    },
    {
        id: 2,
        nome: 'Usuário Teste',
        email: 'user@teste.com',
        senha: '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcflJHPF2eBmcVxa5w0d1w7a', // user123
        tipo_usuario: 'Usuário'
    }
];

// Login page
app.get('/login', (req, res) => {
    const errorMap = {
        '1': 'Email ou senha incorretos',
        '2': 'Erro no servidor'
    };
    
    res.render('login_simple', { 
        error: errorMap[req.query.error] || null,
        title: 'Login - Time Tracking'
    });
});

// Login POST
app.post('/token', async (req, res) => {
    try {
        const { username, password } = req.body;
        console.log('🔐 Tentativa de login:', username);
        
        // Procurar usuário
        let user = USERS.find(u => u.email === username);
        
        // Se não encontrar nos hardcoded, tentar do banco
        if (!user) {
            try {
                const { User } = require('./api/models/database');
                user = await User.findOne({ where: { email: username } });
                if (user) {
                    user = user.toJSON();
                }
            } catch (error) {
                console.log('⚠️ Usando fallback hardcoded - erro no banco:', error.message);
            }
        }
        
        if (!user) {
            console.log('❌ Usuário não encontrado:', username);
            return res.redirect('/login?error=1');
        }
        
        // Verificar senha
        const isValidPassword = await bcrypt.compare(password, user.senha);
        
        if (!isValidPassword) {
            console.log('❌ Senha inválida para:', username);
            return res.redirect('/login?error=1');
        }
        
        // Criar token
        const token = jwt.sign(
            { 
                userId: user.id, 
                email: user.email, 
                tipoUsuario: user.tipo_usuario 
            },
            process.env.SECRET_KEY || 'fallback-secret',
            { expiresIn: '24h' }
        );
        
        // Set cookie
        res.cookie('access_token', token, {
            httpOnly: true,
            secure: false, // Para desenvolvimento local
            maxAge: 24 * 60 * 60 * 1000
        });
        
        console.log('✅ Login bem-sucedido:', username);
        res.redirect('/dashboard');
        
    } catch (error) {
        console.error('❌ Erro no login:', error);
        res.redirect('/login?error=2');
    }
});

// Health check
app.get('/api/test', (req, res) => {
    res.json({ msg: 'deploy funcionando', status: 'ok' });
});

// Dashboard (básico)
app.get('/dashboard', (req, res) => {
    const token = req.cookies.access_token;
    
    if (!token) {
        return res.redirect('/login');
    }
    
    try {
        const decoded = jwt.verify(token, process.env.SECRET_KEY || 'fallback-secret');
        res.send(`
            <h1>🎉 LOGIN FUNCIONOU!</h1>
            <h2>Bem-vindo ${decoded.email}!</h2>
            <p>Tipo: ${decoded.tipoUsuario}</p>
            <p><a href="/logout">Sair</a></p>
            <p><a href="/api/test">Testar API</a></p>
        `);
    } catch (error) {
        res.redirect('/login');
    }
});

// Logout
app.get('/logout', (req, res) => {
    res.clearCookie('access_token');
    res.redirect('/login');
});

// Root redirect
app.get('/', (req, res) => {
    res.redirect('/login');
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`🚀 Servidor rodando em http://localhost:${PORT}`);
    console.log(`🌐 Login: http://localhost:${PORT}/login`);
    console.log(`🧪 Teste: http://localhost:${PORT}/api/test`);
});
