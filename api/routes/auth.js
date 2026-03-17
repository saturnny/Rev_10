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

// Login page
router.get('/login', (req, res) => {
  res.render('login_new', { 
    error: req.query.error,
    title: 'Login - Time Tracking'
  });
});

// Login POST
router.post('/token', async (req, res) => {
  try {
    const { username, password } = req.body;
    
    // Find user
    const user = await User.findOne({ where: { email: username } });
    
    if (!user) {
      return res.redirect('/login?error=1');
    }
    
    // Check password
    const isValidPassword = await bcrypt.compare(password, user.senha);
    
    if (!isValidPassword) {
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
    
    // Set cookie
    res.cookie('access_token', token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      maxAge: 24 * 60 * 60 * 1000 // 24 hours
    });
    
    // Redirect to dashboard
    res.redirect('/dashboard');
    
  } catch (error) {
    console.error('Login error:', error);
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

module.exports = router;
