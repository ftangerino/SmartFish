import express from 'express';
import wa from '@open-wa/wa-automate';
import generateToken from './helpers/generateToken.js'; // Importe a função generateToken correta
import { MongoClient } from 'mongodb';

//const { MongoClient } = require('mongodb');

const app = express();
const args = process.argv;

const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds));
}

let client_wpp; // Variável global para armazenar o cliente WhatsApp

async function main() {
  try {
    // Tenta carregar os dados da sessão anterior
    const savedSession = await loadSession();
    client_wpp = await wa.create(savedSession); // Cria o cliente WhatsApp com a sessão carregada
  } catch (error) {
    // Se houver um erro ao carregar a sessão, cria uma nova sessão
    client_wpp = await wa.create({
      sessionId: `AquarioBot`,
      headless: true,
      authTimeout: 120,
      qrTimeout: 0,
      multiDevice: true,
      hostNotificationLang: 'PT_BR',
      logConsole: false,
    }).then(client => client_wpp.push(client))
  }

  // Define o endpoint da API para enviar tokens
  app.get('/sendToken', async (req, res) => {
    const phone = req.query.phone;
    const token = await generateToken(phone); // Passa o telefone para a função generateToken
  
    console.log(`Sending token to: ${phone}`);
  
    // Modifica esta parte para enviar o token via WhatsApp
    await client_wpp.sendText(`55${phone}@c.us`, `Your login token is: ${token}`);
  
    res.send({ success: true });
  });

  // Inicia o servidor Express
  app.listen(3000, () => {
    console.log("API running in port 3000");
  });
}

// Função para salvar os dados da sessão
async function saveSession() {
  const sessionData = await client_wpp.getSessionData();
  // Salvar sessionData em um banco de dados ou sistema de arquivos
}

// Função para carregar os dados da sessão
async function loadSession() {
  // Carregar sessionData de um banco de dados ou sistema de arquivos
  // Retornar sessionData
}

// Função para salvar o token no banco de dados MongoDB
async function saveToken(token) {
  const client = new MongoClient('mongodb://localhost:27017');

  try {
    await client.connect();
    const db = client.db('smart-fish');
    const tokensCollection = db.collection('tokens_with_numbers');
    await tokensCollection.insertOne({ token });
    console.log("Token gerado e armazenado no MongoDB:", token);
  } catch (err) {
    console.error("Erro ao armazenar o token no MongoDB:", err);
    throw err;
  } finally {
    await client.close();
  }
}

main();
