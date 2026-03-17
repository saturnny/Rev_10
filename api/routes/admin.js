/**
 * Admin Routes
 * Administrative functions
 */
const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs');
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
    
    // Check if user is admin
    if (req.user.tipoUsuario !== 'Admin' && req.user.tipoUsuario !== 'Administrador') {
      return res.redirect('/dashboard');
    }
    
    next();
  } catch (error) {
    res.clearCookie('access_token');
    res.redirect('/login');
  }
};

// Admin Users
router.get('/usuarios', authenticateToken, async (req, res) => {
  try {
    const users = await User.findAll({
      order: [['nome', 'ASC']]
    });
    
    res.render('admin/usuarios_bootstrap', {
      user: req.user,
      users: users.map(u => u.toJSON()),
      title: 'Admin Usuários - Time Tracking'
    });
    
  } catch (error) {
    console.error('Admin usuarios error:', error);
    res.status(500).render('error', { 
      error: 'Erro ao carregar usuários',
      title: 'Erro - Time Tracking'
    });
  }
});

// Create User
router.post('/usuarios', authenticateToken, async (req, res) => {
  try {
    const { nome, email, senha, tipo_usuario } = req.body;
    
    // Hash password
    const hashedPassword = await bcrypt.hash(senha, 10);
    
    // Create user
    await User.create({
      nome,
      email,
      senha: hashedPassword,
      tipo_usuario
    });
    
    res.redirect('/admin/usuarios');
    
  } catch (error) {
    console.error('Create user error:', error);
    res.redirect('/admin/usuarios?error=1');
  }
});

// Admin Categorias
router.get('/categorias', authenticateToken, async (req, res) => {
  try {
    const categorias = await Categoria.findAll({
      order: [['nome', 'ASC']]
    });
    
    res.render('admin/categorias_bootstrap', {
      user: req.user,
      categorias: categorias.map(c => c.toJSON()),
      title: 'Admin Categorias - Time Tracking'
    });
    
  } catch (error) {
    console.error('Admin categorias error:', error);
    res.status(500).render('error', { 
      error: 'Erro ao carregar categorias',
      title: 'Erro - Time Tracking'
    });
  }
});

// Create Categoria
router.post('/categorias', authenticateToken, async (req, res) => {
  try {
    const { nome, descricao } = req.body;
    
    await Categoria.create({
      nome,
      descricao
    });
    
    res.redirect('/admin/categorias');
    
  } catch (error) {
    console.error('Create categoria error:', error);
    res.redirect('/admin/categorias?error=1');
  }
});

// Delete Categoria
router.post('/categorias/:id/excluir', authenticateToken, async (req, res) => {
  try {
    await Categoria.destroy({
      where: { id: req.params.id }
    });
    
    res.redirect('/admin/categorias');
    
  } catch (error) {
    console.error('Delete categoria error:', error);
    res.redirect('/admin/categorias?error=1');
  }
});

// Admin Atividades
router.get('/atividades', authenticateToken, async (req, res) => {
  try {
    const atividades = await Atividade.findAll({
      include: [{ model: Categoria }],
      order: [['nome', 'ASC']]
    });
    
    const categorias = await Categoria.findAll({
      order: [['nome', 'ASC']]
    });
    
    res.render('admin/atividades_bootstrap', {
      user: req.user,
      atividades: atividades.map(a => a.toJSON()),
      categorias: categorias.map(c => c.toJSON()),
      title: 'Admin Atividades - Time Tracking'
    });
    
  } catch (error) {
    console.error('Admin atividades error:', error);
    res.status(500).render('error', { 
      error: 'Erro ao carregar atividades',
      title: 'Erro - Time Tracking'
    });
  }
});

// Admin Lancamentos
router.get('/lancamentos', authenticateToken, async (req, res) => {
  try {
    const { user_id, data } = req.query;
    
    let whereClause = {};
    if (user_id) whereClause.usuario_id = user_id;
    if (data) whereClause.data = data;
    
    const lancamentos = await Lancamento.findAll({
      where: whereClause,
      include: [
        { model: User },
        { model: Atividade, include: [{ model: Categoria }] }
      ],
      order: [['data', 'DESC'], ['hora_inicio', 'DESC']]
    });
    
    const usuarios = await User.findAll({
      order: [['nome', 'ASC']]
    });
    
    res.render('admin/lancamentos', {
      user: req.user,
      lancamentos: lancamentos.map(l => l.toJSON()),
      usuarios: usuarios.map(u => u.toJSON()),
      filtroUserId: user_id || '',
      filtroData: data || '',
      title: 'Admin Lançamentos - Time Tracking'
    });
    
  } catch (error) {
    console.error('Admin lancamentos error:', error);
    res.status(500).render('error', { 
      error: 'Erro ao carregar lançamentos',
      title: 'Erro - Time Tracking'
    });
  }
});

module.exports = router;
