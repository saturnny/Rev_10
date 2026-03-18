/**
 * Vercel Serverless Function - Node.js Entry Point
 * Time Tracking System - Node.js Version
 */
require('dotenv').config();
const express = require('express');
const cookieParser = require('cookie-parser');
const cors = require('cors');
const path = require('path');

// Import routes
const authRoutes = require('./routes/auth');
const dashboardRoutes = require('./routes/dashboard');
const adminRoutes = require('./routes/admin');
const apiRoutes = require('./routes/api');

// Create Express app
const app = express();

// Middleware
app.use(cors());
app.use(cookieParser());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Static files
app.use('/static', express.static(path.join(__dirname, '../static')));

// Set view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, '../templates'));

// Routes
app.use('/', authRoutes.router);
app.use('/', dashboardRoutes);
app.use('/admin', adminRoutes);
app.use('/api', apiRoutes);

// Health check endpoint
app.get('/api/test', async (req, res) => {
  try {
    // Testar conexão com banco
    const { sequelize } = require('./models/database');
    await sequelize.authenticate();
    
    res.json({ 
      msg: 'deploy funcionando', 
      status: 'ok',
      database: 'connected',
      env: process.env.NODE_ENV || 'development',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Health check error:', error);
    res.status(500).json({ 
      msg: 'erro na conexão', 
      status: 'error',
      database: 'disconnected',
      error: error.message,
      env: process.env.NODE_ENV || 'development',
      timestamp: new Date().toISOString()
    });
  }
});

// Root route handled by dashboardRoutes.get('/')

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Not Found', path: req.originalUrl });
});

// Error handler
app.use((err, req, res, next) => {
  console.error('Error:', err);
  
  // Em produção, não enviar stack trace
  const isDev = process.env.NODE_ENV === 'development';
  
  // Erro de conexão com banco
  if (err.name === 'SequelizeConnectionError' || err.name === 'SequelizeConnectionRefusedError') {
    return res.status(500).json({ 
      error: 'Database Connection Error', 
      message: 'Unable to connect to database. Please check DATABASE_URL environment variable.',
      ...(isDev && { stack: err.stack })
    });
  }
  
  // Erro de JWT
  if (err.name === 'JsonWebTokenError') {
    return res.status(401).json({ 
      error: 'Authentication Error', 
      message: 'Invalid token',
      ...(isDev && { stack: err.stack })
    });
  }
  
  // Erro genérico
  res.status(500).json({ 
    error: 'Internal Server Error', 
    message: err.message,
    ...(isDev && { stack: err.stack })
  });
});

// Start local server if run directly (e.g. node api/index.js)
if (require.main === module) {
  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => {
    console.log(`Development server running on port ${PORT}`);
  });
}

// Export for Vercel
module.exports = app;
