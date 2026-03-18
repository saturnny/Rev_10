/**
 * Dashboard Routes
 * Main dashboard and user pages
 */
const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const { User, Lancamento, Atividade, Categoria } = require('../models/database');

const { authenticateToken } = require('./auth');

// Dashboard redirect or home
router.get('/', authenticateToken, (req, res) => {
  res.redirect('/dashboard');
});

// Dashboard Main View
router.get('/dashboard', authenticateToken, async (req, res) => {
  try {
    // req.user is already the full user object from middleware
    console.log('DEBUG DASHBOARD - req.user keys:', Object.keys(req.user));
    console.log('DEBUG DASHBOARD - req.user.id:', req.user.id);
    const user = req.user;
    
    // Get recent lancamentos
    const recentLancamentos = await Lancamento.findAll({
      where: { usuario_id: req.user.id },
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
        usuario_id: req.user.id,
        data: today
      }
    });
    
    res.render('dashboard_improved', {
      user: user,
      recentLancamentos: recentLancamentos.map(l => l.toJSON()),
      todayCount: todayLancamentos.length,
      atividades: await Atividade.findAll({ where: { ativo: true }, include: [Categoria] }),
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
    res.render('perfil_view', {
      user: req.user,
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

// Update Profile (Password)
const bcrypt = require('bcryptjs');
router.post('/perfil', authenticateToken, async (req, res) => {
  try {
    const { senha_atual, nova_senha, confirmar_senha } = req.body;
    
    if (nova_senha !== confirmar_senha) {
      return res.redirect('/perfil?error=passwords_dont_match');
    }
    
    // Fetch user with password
    const user = await User.findByPk(req.user.id);
    const isValid = await bcrypt.compare(senha_atual, user.senha);
    
    if (!isValid) {
      return res.redirect('/perfil?error=invalid_current_password');
    }
    
    const hashedNewPassword = await bcrypt.hash(nova_senha, 10);
    await user.update({ senha: hashedNewPassword });
    
    res.redirect('/perfil?success=1');
  } catch (error) {
    console.error('Update profile error:', error);
    res.redirect('/perfil?error=1');
  }
});

// Meus Lancamentos
router.get('/lancamentos', authenticateToken, async (req, res) => {
  try {
    const { data } = req.query;
    
    let whereClause = { usuario_id: req.user.id };
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
      title: 'Meus Lançamentos - Time Tracking',
      atividades: await Atividade.findAll({ where: { ativo: true }, include: [Categoria] })
    });
  } catch (error) {
    console.error('Lancamentos error:', error);
    res.status(500).render('error', { 
      error: 'Erro ao carregar lançamentos',
      title: 'Erro - Time Tracking'
    });
  }
});

// Create Lancamento
router.post('/novo-lancamento', authenticateToken, async (req, res) => {
  try {
    const { atividade_id, data, hora_inicio, hora_fim, descricao } = req.body;
    await Lancamento.create({
      usuario_id: req.user.id,
      atividade_id,
      data,
      hora_inicio,
      hora_fim,
      descricao
    });
    res.redirect(req.headers.referer || '/dashboard');
  } catch (error) {
    console.error('Create lancamento error:', error);
    res.redirect('/dashboard?error=create');
  }
});

// Edit Lancamento
router.post('/editar-lancamento/:id', authenticateToken, async (req, res) => {
  try {
    const { atividade_id, data, hora_inicio, hora_fim, descricao } = req.body;
    await Lancamento.update({
      atividade_id,
      data,
      hora_inicio,
      hora_fim,
      descricao
    }, {
      where: { 
        id: req.params.id,
        usuario_id: req.user.id
      }
    });
    res.redirect(req.headers.referer || '/dashboard');
  } catch (error) {
    console.error('Edit lancamento error:', error);
    res.redirect('/dashboard?error=edit');
  }
});

// Delete Lancamento
router.post('/excluir-lancamento/:id', authenticateToken, async (req, res) => {
  try {
    await Lancamento.destroy({
      where: { 
        id: req.params.id,
        usuario_id: req.user.id
      }
    });
    res.redirect(req.headers.referer || '/dashboard');
  } catch (error) {
    console.error('Delete lancamento error:', error);
    res.redirect('/dashboard?error=delete');
  }
});

module.exports = router;
