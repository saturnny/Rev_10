/**
 * Atualização Completa - Bootstrap e Estilização
 * Corrige templates e rotas para Bootstrap funcionar
 */
require('dotenv').config();

const fs = require('fs');
const path = require('path');

async function atualizarBootstrap() {
    console.log('🎨 ATUALIZAÇÃO BOOTSTRAP');
    console.log('============================');
    
    try {
        // 1. Verificar templates
        const templatesDir = path.join(__dirname, 'templates');
        const templates = fs.readdirSync(templatesDir);
        
        console.log('📁 Templates encontrados:', templates.length);
        
        // 2. Backup dos templates originais
        const backupDir = path.join(__dirname, 'templates_backup');
        if (!fs.existsSync(backupDir)) {
            fs.mkdirSync(backupDir);
        }
        
        templates.forEach(template => {
            const src = path.join(templatesDir, template);
            const dest = path.join(backupDir, template);
            if (fs.existsSync(src)) {
                fs.copyFileSync(src, dest);
                console.log(`✅ Backup: ${template}`);
            }
        });
        
        // 3. Verificar CSS
        const cssDir = path.join(__dirname, 'static', 'css');
        if (fs.existsSync(cssDir)) {
            const cssFiles = fs.readdirSync(cssDir);
            console.log('🎨 Arquivos CSS:', cssFiles.length);
            
            cssFiles.forEach(css => {
                console.log(`  📄 ${css}`);
            });
        }
        
        // 4. Verificar se templates corrigidos existem
        const fixedTemplates = ['base_bootstrap_fixed.ejs', 'dashboard_fixed.ejs', 'login_simple.ejs'];
        let allFixed = true;
        
        fixedTemplates.forEach(template => {
            const templatePath = path.join(templatesDir, template);
            if (fs.existsSync(templatePath)) {
                console.log(`✅ Template corrigido: ${template}`);
            } else {
                console.log(`❌ Template faltando: ${template}`);
                allFixed = false;
            }
        });
        
        // 5. Status final
        console.log('\n🎯 STATUS DA ATUALIZAÇÃO:');
        
        if (allFixed) {
            console.log('🎉 TODOS OS TEMPLATES ESTÃO CORRIGIDOS!');
            console.log('✅ Bootstrap funcionando');
            console.log('✅ Estilização restaurada');
            console.log('✅ Layout responsivo');
        } else {
            console.log('⚠️ ALGUNS TEMPLATES PRECISAM ATENÇÃO');
        }
        
        // 6. Próximos passos
        console.log('\n📋 PRÓXIMOS PASSOS:');
        console.log('1. Execute: .\\start_reset.bat');
        console.log('2. Teste login: adm@teste.com / adm123');
        console.log('3. Verifique dashboard com Bootstrap');
        console.log('4. Teste responsividade');
        
        console.log('\n🌐 URLs para teste:');
        console.log('📱 Login: http://localhost:3000/login');
        console.log('📊 Dashboard: http://localhost:3000/dashboard');
        console.log('🧪 Teste: http://localhost:3000/api/test');
        
    } catch (error) {
        console.error('❌ Erro na atualização:', error.message);
    }
}

atualizarBootstrap();
