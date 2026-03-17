/**
 * Dashboard Routes
 * Main dashboard and user pages
 */
const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const { User, Lancamento, Atividade, Categoria } = require('../models/database');

// JWT Secret
const JWT_SECRET = process.env.SECRET_KEY || 'your-secret-key';

// Authentication middleware
const authenticateToken = (req, res, next) => {
  const token = req.cookies.access_token;
  
  if (!token) {
    return res.redirect('/login');
  }
  
  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.clearCookie('access_token');
    res.redirect('/login');
  }
};

// Dashboard
router.get('/', authenticateToken, async (req, res) => {
  try {
    // Get user info
    const user = await User.findByPk(req.user.userId);
    
    // Get recent lancamentos
    const recentLancamentos = await Lancamento.findAll({
      where: { usuario_id: req.user.userId },
      include: [
        { model: Atividade, include: [{ model: Categoria }] }
      ],
      order: [['data', 'DESC'], ['hora_inicio', 'DESC']],
      limit: 10
    });
    
    // Get statistics
    const today = new Date().toISOString().split('T')[0];
    const todayLancamentos = await Lancamento.findAll({
      where: { 
        usuario_id: req.user.userId,
        data: today
      }
    });
    
    res.render('dashboard_improved', {
      user: user.toJSON(),
      recentLancamentos: recentLancamentos.map(l => l.toJSON()),
      todayCount: todayLancamentos.length,
      title: 'Dashboard - Time Tracking'
    });
    
  } catch (error) {
    console.error('Dashboard error:', error);
    res.status(500).render('error', { 
      error: 'Erro ao carregar dashboard',
      title: 'Erro - Time Tracking'
    });
  }
});

// Perfil
router.get('/perfil', authenticateToken, async (req, res) => {
  try {
    const user = await User.findByPk(req.user.userId);
    
    res.render('perfil_view', {
      user: user.toJSON(),
      title: 'Meu Perfil - Time Tracking'
    });
    
  } catch (error) {
    console.error('Perfil error:', error);
    res.status(500).render('error', { 
      error: 'Erro ao carregar perfil',
      title: 'Erro - Time Tracking'
    });
  }
});

// Meus Lancamentos
router.get('/lancamentos', authenticateToken, async (req, res) => {
  try {
    const { data } = req.query;
    
    let whereClause = { usuario_id: req.user.userId };
    if (data) {
      whereClause.data = data;
    }
    
    const lancamentos = await Lancamento.findAll({
      where: whereClause,
      include: [
        { model: Atividade, include: [{ model: Categoria }] }
      ],
      order: [['data', 'DESC'], ['hora_inicio', 'DESC']]
    });
    
    res.render('lancamentos', {
      user: req.user,
      lancamentos: lancamentos.map(l => l.toJSON()),
      filtroData: data || '',
      title: 'Meus Lançamentos - Time Tracking'
    });
    
  } catch (error) {
    console.error('Lancamentos error:', error);
    res.status(500).render('error', { 
      error: 'Erro ao carregar lançamentos',
      title: 'Erro - Time Tracking'
    });
  }
});

module.exports = router;
