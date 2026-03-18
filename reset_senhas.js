/**
 * Reset de Senhas - Supabase
 * Reseta todas as senhas para os valores corretos
 */
require('dotenv').config();

async function resetPasswords() {
    console.log('🔄 RESET DE SENHAS - SUPABASE');
    console.log('================================');
    
    try {
        const { sequelize, User } = require('./api/models/database');
        const bcrypt = require('bcryptjs');
        
        // 1. Conectar
        await sequelize.authenticate();
        console.log('✅ Conectado ao Supabase');
        
        // 2. Listar usuários atuais
        const users = await User.findAll();
        console.log(`📊 Usuários encontrados: ${users.length}`);
        
        // 3. Resetar senhas para todos
        const resetUsers = [
            {
                email: 'adm@teste.com',
                nome: 'Administrador',
                senha: 'adm123',
                tipo_usuario: 'Admin',
                ativo: true
            },
            {
                email: 'user@teste.com', 
                nome: 'Usuário Teste',
                senha: 'user123',
                tipo_usuario: 'Usuário',
                ativo: true
            }
        ];
        
        for (const resetUser of resetUsers) {
            // Hash da senha correta
            const hashedPassword = await bcrypt.hash(resetUser.senha, 10);
            
            // Procurar usuário existente
            const [user, created] = await User.findOrCreate({
                where: { email: resetUser.email },
                defaults: {
                    ...resetUser,
                    senha: hashedPassword
                }
            });
            
            if (created) {
                console.log(`✅ Usuário criado: ${resetUser.email}`);
            } else {
                // Atualizar senha
                await user.update({
                    nome: resetUser.nome,
                    senha: hashedPassword,
                    tipo_usuario: resetUser.tipo_usuario,
                    ativo: resetUser.ativo
                });
                console.log(`🔄 Senha resetada: ${resetUser.email}`);
            }
        }
        
        // 4. Testar todos os logins
        console.log('\n🧪 Testando logins:');
        
        for (const resetUser of resetUsers) {
            const user = await User.findOne({ where: { email: resetUser.email } });
            const isValid = await bcrypt.compare(resetUser.senha, user.senha);
            console.log(`${isValid ? '✅' : '❌'} ${resetUser.email}: ${resetUser.senha} -> ${isValid ? 'VÁLIDA' : 'INVÁLIDA'}`);
        }
        
        // 5. Listar usuários finais
        console.log('\n👥 Usuários finais no Supabase:');
        const finalUsers = await User.findAll({
            attributes: ['id', 'nome', 'email', 'tipo_usuario', 'ativo']
        });
        
        finalUsers.forEach(user => {
            console.log(`  📧 ${user.email} (${user.tipo_usuario}) - ${user.ativo ? 'Ativo' : 'Inativo'}`);
        });
        
        console.log('\n🎉 SENHAS RESETADAS COM SUCESSO!');
        console.log('🌐 Teste: http://localhost:3000/login');
        console.log('👤 Admin: adm@teste.com / adm123');
        console.log('👥 User: user@teste.com / user123');
        
        await sequelize.close();
        
    } catch (error) {
        console.error('❌ Erro no reset:', error.message);
        console.log('\n💡 Verifique:');
        console.log('1. Conexão com Supabase');
        console.log('2. Permissões no banco');
        console.log('3. DATABASE_URL no .env.local');
    }
}

resetPasswords();
