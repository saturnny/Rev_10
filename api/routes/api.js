/**
 * API Routes
 * JSON API endpoints
 */
const express = require('express');
const router = express.Router();
const { User, Lancamento, Atividade, Categoria } = require('../models/database');

// Health check
router.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    service: 'time-tracking',
    environment: process.env.NODE_ENV || 'development'
  });
});

// Get users
router.get('/users', async (req, res) => {
  try {
    const users = await User.findAll({
      attributes: ['id', 'nome', 'email', 'tipo_usuario', 'ativo'],
      order: [['nome', 'ASC']]
    });
    
    res.json({
      success: true,
      data: users.map(u => u.toJSON())
    });
    
  } catch (error) {
    console.error('API users error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Get categorias
router.get('/categorias', async (req, res) => {
  try {
    const categorias = await Categoria.findAll({
      where: { ativo: true },
      order: [['nome', 'ASC']]
    });
    
    res.json({
      success: true,
      data: categorias.map(c => c.toJSON())
    });
    
  } catch (error) {
    console.error('API categorias error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Get atividades
router.get('/atividades', async (req, res) => {
  try {
    const { categoria_id } = req.query;
    
    let whereClause = { ativo: true };
    if (categoria_id) {
      whereClause.categoria_id = categoria_id;
    }
    
    const atividades = await Atividade.findAll({
      where: whereClause,
      include: [{ model: Categoria }],
      order: [['nome', 'ASC']]
    });
    
    res.json({
      success: true,
      data: atividades.map(a => a.toJSON())
    });
    
  } catch (error) {
    console.error('API atividades error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Create lancamento
router.post('/lancamentos', async (req, res) => {
  try {
    const { usuario_id, atividade_id, data, hora_inicio, hora_fim, descricao } = req.body;
    
    const lancamento = await Lancamento.create({
      usuario_id,
      atividade_id,
      data,
      hora_inicio,
      hora_fim,
      descricao
    });
    
    res.json({
      success: true,
      data: lancamento.toJSON()
    });
    
  } catch (error) {
    console.error('API create lancamento error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Get lancamentos
router.get('/lancamentos', async (req, res) => {
  try {
    const { usuario_id, data, limit = 50 } = req.query;
    
    let whereClause = {};
    if (usuario_id) whereClause.usuario_id = usuario_id;
    if (data) whereClause.data = data;
    
    const lancamentos = await Lancamento.findAll({
      where: whereClause,
      include: [
        { model: User },
        { model: Atividade, include: [{ model: Categoria }] }
      ],
      order: [['data', 'DESC'], ['hora_inicio', 'DESC']],
      limit: parseInt(limit)
    });
    
    res.json({
      success: true,
      data: lancamentos.map(l => l.toJSON())
    });
    
  } catch (error) {
    console.error('API lancamentos error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

module.exports = router;
