const { MongoClient } = require('mongodb');

async function generateToken(phone) {
    const length = 6;
    const characters = '0123456789';
    let token = '';
  
    for (let i = 0; i < length; i++) {
      const randomIndex = Math.floor(Math.random() * characters.length);
      token += characters[randomIndex];
    }

    // Salvar o token no MongoDB
    const client = new MongoClient('mongodb://localhost:27017');
    try {
        await client.connect();
        const db = client.db('smart-fish');
        const tokensCollection = db.collection('tokens_with_numbers');
        await tokensCollection.insertOne({ token, phone }); // Salva token e telefone
        console.log("Token gerado e armazenado no MongoDB:", token);
        return token;
    } catch (err) {
        console.error("Erro ao armazenar o token no MongoDB:", err);
        throw err;
    } finally {
        await client.close();
    }
}

module.exports = generateToken;
