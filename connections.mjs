import express from 'express'
import wa from '@open-wa/wa-automate'

const app = express()
const args = process.argv

const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds))
}

const clients_wpp = []
const qt_wpps = 0

for(let i = 0; i <= qt_wpps; i++) {
  await wa.create({
    sessionId: `AquaT${i}`,
    headless: true,
    authTimeout: 120,
    qrTimeout: 0,
    multiDevice: true,
    hostNotificationLang: 'PT_BR',
    logConsole: false,
  }).then(client => clients_wpp.push(client))

  // await sleep (3000)
}

async function main() {
  while(clients_wpp.length < qt_wpps) {
    await sleep(15000)

    console.log("Waiting all clientes connect")
  }

  app.get('/sendToken', async (req, res) => {
    const phone = req.query.phone
    const token = generateToken(); // You need to implement this function to generate the token

    console.log(`Sending token to: ${phone}`)

    // Modify this part to send the token via WhatsApp
    await clients_wpp[0].sendText(`55${phone}@c.us`, `Your login token is: ${token}`)

    res.send({ success: true })
  })

  app.listen(3000, () => {
    console.log("API running in port 3000")
  })
}

main()
