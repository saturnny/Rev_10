/**
 * Teste de Login com Supabase
 */
require('dotenv').config();

async function testSupabaseLogin() {
    console.log('🧪 TESTE DE LOGIN COM SUPABASE');
    console.log('====================================');
    
    try {
        // 1. Conectar ao Supabase
        console.log('\n🔗 Conectando ao Supabase...');
        const { sequelize, User } = require('./api/models/database');
        
        await sequelize.authenticate();
        console.log('✅ Conexão com Supabase OK!');
        
        // 2. Verificar se tabela existe
        console.log('\n📊 Verificando tabela usuarios...');
        const userCount = await User.count();
        console.log(`✅ Tabela usuarios: ${userCount} registros`);
        
        // 3. Listar usuários
        console.log('\n👥 Usuários no Supabase:');
        const users = await User.findAll({
            attributes: ['id', 'nome', 'email', 'tipo_usuario', 'ativo', 'senha']
        });
        
        if (users.length === 0) {
            console.log('❌ Nenhum usuário encontrado!');
            console.log('💡 Execute: node seed_database.js');
            return;
        }
        
        users.forEach(user => {
            console.log(`  📧 ${user.email} (${user.tipo_usuario}) - ${user.ativo ? 'Ativo' : 'Inativo'}`);
            console.log(`     ID: ${user.id}`);
            console.log(`     Senha: ${user.senha ? 'Hashed' : 'NULL'}`);
        });
        
        // 4. Testar senhas
        console.log('\n🔐 Testando senhas:');
        const bcrypt = require('bcryptjs');
        
        const testUsers = [
            { email: 'adm@teste.com', password: 'adm123' },
            { email: 'user@teste.com', password: 'user123' }
        ];
        
        for (const testUser of testUsers) {
            const user = users.find(u => u.email === testUser.email);
            if (user) {
                try {
                    const isValid = await bcrypt.compare(testUser.password, user.senha);
                    console.log(`  ${isValid ? '✅' : '❌'} ${testUser.email}: ${testUser.password} -> ${isValid ? 'VÁLIDA' : 'INVÁLIDA'}`);
                } catch (error) {
                    console.log(`  ❌ ${testUser.email}: ERRO ao testar senha - ${error.message}`);
                }
            } else {
                console.log(`  ❌ ${testUser.email}: USUÁRIO NÃO ENCONTRADO`);
            }
        }
        
        // 5. Testar requisição POST simulada
        console.log('\n🌐 Testando requisição POST simulada:');
        const express = require('express');
        const app = express();
        app.use(express.urlencoded({ extended: true }));
        
        // Simular POST /token
        const req = {
            body: {
                username: 'adm@teste.com',
                password: 'adm123'
            }
        };
        
        console.log('  📤 Dados enviados:', req.body);
        
        const user = await User.findOne({ where: { email: req.body.username } });
        console.log('  📥 Usuário encontrado:', user ? 'SIM' : 'NÃO');
        
        if (user) {
            const isValidPassword = await bcrypt.compare(req.body.password, user.senha);
            console.log('  🔑 Senha válida:', isValidPassword ? 'SIM' : 'NÃO');
            
            if (isValidPassword) {
                console.log('  🎉 LOGIN DEVERIA FUNCIONAR!');
            } else {
                console.log('  ❌ SENHA INVÁLIDA - Erro na senha');
            }
        } else {
            console.log('  ❌ USUÁRIO NÃO ENCONTRADO');
        }
        
        await sequelize.close();
        
    } catch (error) {
        console.error('\n❌ ERRO NO TESTE:', error.message);
        console.error('Stack:', error.stack);
        console.log('\n💡 Soluções:');
        console.log('1. Verifique DATABASE_URL no .env.local');
        console.log('2. Verifique se Supabase está acessível');
        console.log('3. Execute: node seed_database.js');
    }
}

testSupabaseLogin();
