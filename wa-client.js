const { create, Client } = require('@open-wa/wa-automate');

async function createWaClient() {
    const client = await create({ sessionId: 'session' }); // Pode ser qualquer string única
    return client;
}

module.exports = createWaClient;
