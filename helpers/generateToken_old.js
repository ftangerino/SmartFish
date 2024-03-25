// generateToken.js

// Função para gerar um token aleatório
function generateToken() {
    const length = 6; // Defina o comprimento do token
    const characters = '0123456789'; // Caracteres permitidos no token
    let token = '';
  
    for (let i = 0; i < length; i++) {
      const randomIndex = Math.floor(Math.random() * characters.length);
      token += characters[randomIndex];
    }
  
    return token;
  }
  
  module.exports = generateToken;
  