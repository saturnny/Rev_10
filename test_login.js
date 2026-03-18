/**
 * Test Script - Login Functionality
 * Testa se o sistema de login está funcionando
 */
require('dotenv').config();

const express = require('express');
const bcrypt = require('bcryptjs');
const { User } = require('./api/models/database');

async function testLogin() {
    console.log('🧪 Testando sistema de login...');
    
    try {
        // Conectar ao banco
        const { sequelize } = require('./api/models/database');
        await sequelize.authenticate();
        console.log('✅ Banco conectado com sucesso!');
        
        // Verificar usuários
        const users = await User.findAll();
        console.log(`📋 Usuários encontrados: ${users.length}`);
        
        if (users.length === 0) {
            console.log('⚠️ Nenhum usuário encontrado. Execute: node seed_database.js');
            return;
        }
        
        // Testar senhas
        for (const user of users) {
            console.log(`\n👤 Testando usuário: ${user.email}`);
            
            // Testar senha admin
            if (user.email === 'adm@teste.com') {
                const isValid = await bcrypt.compare('adm123', user.senha);
                console.log(`🔐 Senha 'adm123': ${isValid ? '✅ Válida' : '❌ Inválida'}`);
            }
            
            // Testar senha user
            if (user.email === 'user@teste.com') {
                const isValid = await bcrypt.compare('user123', user.senha);
                console.log(`🔐 Senha 'user123': ${isValid ? '✅ Válida' : '❌ Inválida'}`);
            }
        }
        
        console.log('\n🎉 Teste concluído! Sistema pronto para uso.');
        console.log('🌐 Acesse: http://localhost:3000/login');
        
        await sequelize.close();
        
    } catch (error) {
        console.error('❌ Erro no teste:', error.message);
        console.log('\n💡 Soluções:');
        console.log('1. Verifique se o banco PostgreSQL está rodando');
        console.log('2. Verifique a string DATABASE_URL no .env.local');
        console.log('3. Execute: node seed_database.js');
    }
}

// Executar teste
testLogin();
