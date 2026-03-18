/**
 * Debug Login - Identificar problemas
 */
require('dotenv').config();

async function debugLogin() {
    console.log('🔍 DEBUG DO LOGIN');
    console.log('==================');
    
    try {
        // 1. Verificar variáveis de ambiente
        console.log('\n📋 Variáveis de Ambiente:');
        console.log('DATABASE_URL:', process.env.DATABASE_URL ? '✅ Configurada' : '❌ Não configurada');
        console.log('SECRET_KEY:', process.env.SECRET_KEY ? '✅ Configurada' : '❌ Não configurada');
        console.log('NODE_ENV:', process.env.NODE_ENV || 'development');
        
        // 2. Conectar ao banco
        console.log('\n🔗 Testando conexão com Supabase...');
        const { sequelize, User } = require('./api/models/database');
        
        await sequelize.authenticate();
        console.log('✅ Conexão com Supabase OK!');
        
        // 3. Verificar tabela usuarios
        console.log('\n📊 Verificando tabela usuarios...');
        const userCount = await User.count();
        console.log(`✅ Tabela usuarios existe com ${userCount} registros`);
        
        // 4. Listar usuários
        console.log('\n👥 Usuários encontrados:');
        const users = await User.findAll({
            attributes: ['id', 'nome', 'email', 'tipo_usuario', 'ativo']
        });
        
        if (users.length === 0) {
            console.log('❌ Nenhum usuário encontrado!');
            console.log('💡 Execute: node seed_database.js');
        } else {
            users.forEach(user => {
                console.log(`  📧 ${user.email} (${user.tipo_usuario}) - ${user.ativo ? 'Ativo' : 'Inativo'}`);
            });
        }
        
        // 5. Testar senhas
        console.log('\n🔐 Testando senhas:');
        const bcrypt = require('bcryptjs');
        
        for (const user of users) {
            if (user.email === 'adm@teste.com') {
                const testSenha = await bcrypt.compare('adm123', user.senha);
                console.log(`  👤 Admin (adm@teste.com): ${testSenha ? '✅ Senha OK' : '❌ Senha inválida'}`);
            }
            if (user.email === 'user@teste.com') {
                const testSenha = await bcrypt.compare('user123', user.senha);
                console.log(`  👥 User (user@teste.com): ${testSenha ? '✅ Senha OK' : '❌ Senha inválida'}`);
            }
        }
        
        console.log('\n🎯 Diagnóstico final:');
        if (users.length > 0) {
            console.log('✅ Sistema pronto para uso!');
            console.log('🌐 Acesse: http://localhost:3000/login');
        } else {
            console.log('❌ Execute: node seed_database.js para criar usuários');
        }
        
        await sequelize.close();
        
    } catch (error) {
        console.error('\n❌ ERRO NO DEBUG:', error.message);
        console.log('\n💡 Soluções possíveis:');
        console.log('1. Verifique a string DATABASE_URL no .env.local');
        console.log('2. Verifique se o Supabase está acessível');
        console.log('3. Execute: node seed_database.js');
    }
}

debugLogin();
