/**
 * Seed Database - Node.js Version
 * Create initial data for testing
 */
const bcrypt = require('bcryptjs');
const { sequelize, User, Categoria, Atividade } = require('./models/database');

async function seedDatabase() {
  try {
    console.log('Connecting to database...');
    await sequelize.authenticate();
    console.log('Database connected successfully.');

    // Sync all models
    await sequelize.sync({ force: false });
    console.log('Database synced successfully.');

    // Check if users already exist
    const userCount = await User.count();
    if (userCount === 0) {
      console.log('Creating initial users...');

      // Create admin user
      const hashedAdminPassword = await bcrypt.hash('adm123', 10);
      await User.create({
        nome: 'Administrador',
        email: 'adm@teste.com',
        senha: hashedAdminPassword,
        tipo_usuario: 'Admin'
      });

      // Create regular user
      const hashedUserPassword = await bcrypt.hash('user123', 10);
      await User.create({
        nome: 'Usuário Teste',
        email: 'user@teste.com',
        senha: hashedUserPassword,
        tipo_usuario: 'Usuário'
      });

      console.log('Users created successfully.');
    }

    // Check if categories already exist
    const categoriaCount = await Categoria.count();
    if (categoriaCount === 0) {
      console.log('Creating initial categories...');

      await Categoria.bulkCreate([
        { nome: 'Trabalho', descricao: 'Atividades profissionais' },
        { nome: 'Estudo', descricao: 'Atividades de aprendizado' },
        { nome: 'Pessoal', descricao: 'Atividades pessoais' },
        { nome: 'Reunião', descricao: 'Reuniões e encontros' },
        { nome: 'Desenvolvimento', descricao: 'Atividades de desenvolvimento' }
      ]);

      console.log('Categories created successfully.');
    }

    // Check if activities already exist
    const atividadeCount = await Atividade.count();
    if (atividadeCount === 0) {
      console.log('Creating initial activities...');

      const categorias = await Categoria.findAll();
      
      await Atividade.bulkCreate([
        { nome: 'Reunião de equipe', categoria_id: categorias[0].id, descricao: 'Reunião semanal com a equipe' },
        { nome: 'Desenvolvimento de features', categoria_id: categorias[4].id, descricao: 'Implementação de novas funcionalidades' },
        { nome: 'Code review', categoria_id: categorias[0].id, descricao: 'Revisão de código da equipe' },
        { nome: 'Estudo de Node.js', categoria_id: categorias[1].id, descricao: 'Aprendizado de Node.js e Express' },
        { nome: 'Planejamento sprint', categoria_id: categorias[0].id, descricao: 'Planejamento da próxima sprint' }
      ]);

      console.log('Activities created successfully.');
    }

    console.log('Database seeded successfully!');
    
  } catch (error) {
    console.error('Error seeding database:', error);
  } finally {
    await sequelize.close();
  }
}

// Run if called directly
if (require.main === module) {
  seedDatabase();
}

module.exports = { seedDatabase };
