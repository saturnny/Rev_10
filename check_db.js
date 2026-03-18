const { User } = require('./api/models/database');
(async () => {
    try {
        const users = await User.findAll({ attributes: ['id', 'email', 'tipo_usuario'] });
        console.log('--- USERS ---');
        console.log(JSON.stringify(users, null, 2));
        process.exit(0);
    } catch (err) {
        console.error('ERROR:', err);
        process.exit(1);
    }
})();
