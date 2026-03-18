/**
 * Correção de Login - Problemas Comuns
 */
require('dotenv').config();

async function fixLogin() {
    console.log('🔧 CORREÇÃO DE LOGIN - SUPABASE');
    console.log('==================================');
    
    try {
        const { sequelize, User } = require('./api/models/database');
        const bcrypt = require('bcryptjs');
        
        // 1. Conectar
        await sequelize.authenticate();
        console.log('✅ Conectado ao Supabase');
        
        // 2. Verificar se tabela existe
        await sequelize.sync({ alter: true });
        console.log('✅ Tabela sincronizada');
        
        // 3. Verificar usuários
        const users = await User.findAll();
        console.log(`📊 Usuários encontrados: ${users.length}`);
        
        // 4. Criar/atualizar usuários de teste
        const testUsers = [
            {
                nome: 'Administrador',
                email: 'adm@teste.com',
                senha: 'adm123',
                tipo_usuario: 'Admin',
                ativo: true
            },
            {
                nome: 'Usuário Teste',
                email: 'user@teste.com',
                senha: 'user123',
                tipo_usuario: 'Usuário',
                ativo: true
            }
        ];
        
        for (const testUser of testUsers) {
            const [user, created] = await User.findOrCreate({
                where: { email: testUser.email },
                defaults: {
                    ...testUser,
                    senha: await bcrypt.hash(testUser.senha, 10)
                }
            });
            
            if (created) {
                console.log(`✅ Usuário criado: ${testUser.email}`);
            } else {
                // Atualizar senha se necessário
                const isValid = await bcrypt.compare(testUser.senha, user.senha);
                if (!isValid) {
                    await user.update({ 
                        senha: await bcrypt.hash(testUser.senha, 10) 
                    });
                    console.log(`🔄 Senha atualizada: ${testUser.email}`);
                } else {
                    console.log(`✅ Usuário OK: ${testUser.email}`);
                }
            }
        }
        
        // 5. Testar login final
        console.log('\n🧪 Teste final de login:');
        const adminUser = await User.findOne({ where: { email: 'adm@teste.com' } });
        
        if (adminUser) {
            const isValid = await bcrypt.compare('adm123', adminUser.senha);
            console.log(`🔐 Admin login: ${isValid ? '✅ FUNCIONA' : '❌ FALHA'}`);
        }
        
        const userUser = await User.findOne({ where: { email: 'user@teste.com' } });
        if (userUser) {
            const isValid = await bcrypt.compare('user123', userUser.senha);
            console.log(`🔐 User login: ${isValid ? '✅ FUNCIONA' : '❌ FALHA'}`);
        }
        
        console.log('\n🎉 CORREÇÃO CONCLUÍDA!');
        console.log('🌐 Teste: http://localhost:3000/login');
        console.log('👤 Admin: adm@teste.com / adm123');
        console.log('👥 User: user@teste.com / user123');
        
        await sequelize.close();
        
    } catch (error) {
        console.error('❌ Erro na correção:', error.message);
        console.log('\n💡 Verifique:');
        console.log('1. DATABASE_URL no .env.local');
        console.log('2. Conexão com Supabase');
        console.log('3. Permissões no Supabase');
    }
}

fixLogin();
