/**
 * Authentication Routes
 * Login, Logout, and JWT handling
 */
const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { User } = require('../models/database');

// JWT Secret
const JWT_SECRET = process.env.SECRET_KEY || 'your-secret-key';

/**
 * Authentication Middleware
 * Verifies JWT and fetches full user data
 */
const authenticateToken = async (req, res, next) => {
  const token = req.cookies.access_token;
  
  if (!token) {
    return res.redirect('/login');
  }
  
  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    console.log('DEBUG AUTH - decoded:', decoded);
    
    // Fetch full user and toJSON to avoid proxy issues in templates
    const user = await User.findByPk(decoded.userId);
    console.log('DEBUG AUTH - user found:', user ? 'YES' : 'NO');
    if (user) console.log('DEBUG AUTH - user.id:', user.id);
    
    if (!user || !user.ativo) {
      res.clearCookie('access_token');
      return res.redirect('/login');
    }
    
    req.user = user.toJSON();
    // Ensure nome exists to avoid substring errors in templates
    if (!req.user.nome) req.user.nome = req.user.email || 'Usuário';
    
    next();
  } catch (error) {
    console.error('Auth middleware error:', error);
    res.clearCookie('access_token');
    res.redirect('/login');
  }
};

// Login page
router.get('/login', (req, res) => {
  const errorMap = {
    '1': 'Email ou senha incorretos',
    '2': 'Erro no servidor, tente novamente'
  };
  
  res.render('login_new', { 
    error: errorMap[req.query.error] || null,
    title: 'Login - Time Tracking'
  });
});

// Login POST
router.post('/token', async (req, res) => {
  try {
    const { username, password } = req.body;
    
    console.log('🔐 Tentativa de login:', { username, passwordLength: password ? password.length : 0 });
    
    // Find user
    const user = await User.findOne({ where: { email: username } });
    
    console.log('👤 Usuário encontrado:', user ? 'SIM' : 'NÃO');
    
    if (!user) {
      console.log('❌ Redirecionando para erro=1 (usuário não encontrado)');
      return res.redirect('/login?error=1');
    }
    
    // Check password
    const isValidPassword = await bcrypt.compare(password, user.senha);
    
    console.log('🔑 Senha válida:', isValidPassword ? 'SIM' : 'NÃO');
    
    if (!isValidPassword) {
      console.log('❌ Redirecionando para erro=1 (senha inválida)');
      return res.redirect('/login?error=1');
    }
    
    // Create JWT token
    const token = jwt.sign(
      { 
        userId: user.id, 
        email: user.email, 
        tipoUsuario: user.tipo_usuario 
      },
      JWT_SECRET,
      { expiresIn: '24h' }
    );
    
    console.log('🎫 Token criado com sucesso');
    
    // Set cookie
    res.cookie('access_token', token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      maxAge: 24 * 60 * 60 * 1000 // 24 hours
    });
    
    console.log('🍪 Cookie definido, redirecionando para dashboard');
    
    // Redirect to dashboard
    res.redirect('/dashboard');
    
  } catch (error) {
    console.error('❌ Erro no login:', error);
    console.error('Stack:', error.stack);
    res.redirect('/login?error=2');
  }
});

// Logout
router.post('/logout', (req, res) => {
  res.clearCookie('access_token');
  res.redirect('/login');
});

router.get('/logout', (req, res) => {
  res.clearCookie('access_token');
  res.redirect('/login');
});

module.exports = { 
  router,
  authenticateToken
};
