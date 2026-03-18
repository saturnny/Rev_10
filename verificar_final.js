/**
 * Verificação Final - Login Supabase
 * Verifica se tudo está 100% funcionando
 */
require('dotenv').config();

async function verificarFinal() {
    console.log('🔍 VERIFICAÇÃO FINAL - SUPABASE');
    console.log('====================================');
    
    try {
        const { sequelize, User } = require('./api/models/database');
        const bcrypt = require('bcryptjs');
        
        // 1. Conectar
        await sequelize.authenticate();
        console.log('✅ Conexão Supabase OK');
        
        // 2. Verificar usuários
        const users = await User.findAll();
        console.log(`📊 Total usuários: ${users.length}`);
        
        // 3. Testar logins
        const testLogins = [
            { email: 'adm@teste.com', senha: 'adm123' },
            { email: 'user@teste.com', senha: 'user123' }
        ];
        
        console.log('\n🧪 Teste de Logins:');
        let todosOK = true;
        
        for (const test of testLogins) {
            const user = await User.findOne({ where: { email: test.email } });
            
            if (!user) {
                console.log(`❌ ${test.email}: USUÁRIO NÃO ENCONTRADO`);
                todosOK = false;
                continue;
            }
            
            const isValid = await bcrypt.compare(test.senha, user.senha);
            console.log(`${isValid ? '✅' : '❌'} ${test.email}: ${test.senha} -> ${isValid ? 'FUNCIONA' : 'FALHA'}`);
            
            if (!isValid) todosOK = false;
        }
        
        // 4. Resultado final
        console.log('\n🎯 RESULTADO FINAL:');
        if (todosOK) {
            console.log('🎉 TODOS OS LOGINS ESTÃO FUNCIONANDO!');
            console.log('🌐 Acesse: http://localhost:3000/login');
            console.log('👤 Admin: adm@teste.com / adm123');
            console.log('👥 User: user@teste.com / user123');
            console.log('\n✅ SISTEMA PRONTO PARA USO E DEPLOY!');
        } else {
            console.log('❌ ALGUNS LOGINS ESTÃO COM PROBLEMAS!');
            console.log('\n💡 Execute: .\start_reset.bat');
        }
        
        await sequelize.close();
        
    } catch (error) {
        console.error('❌ Erro na verificação:', error.message);
    }
}

verificarFinal();
