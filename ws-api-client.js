const fs = require('fs')
const readline = require('readline')
const axios = require('axios')
const WebSocket = require('ws')

const AUTH_ENDPOINT = 'https://www.theblock.pro/api-public/v1/users/auth'
//const ENDPOINT = 'wss://www.theblock.pro/api-public/v1/news/live?tokens=btc,eth,aave,ada,algo,bnb,bch,eos,luna' //token filter
//const ENDPOINT = 'wss://www.theblock.pro/api-public/v1/news/live?priority=1,2,3' //priority filter
const ENDPOINT = 'wss://www.theblock.pro/api-public/v1/news/live'
const LAST_PING_TIMEOUT = 60000

const read = readline.createInterface({
  input: process.stdin,
  output: process.stdout
})

let credentials = { email: '', apiKey: '' }

// Function to authenticate and get token
async function authenticateAndGetToken(email, apiKey) {
  try {
    const response = await axios.post(AUTH_ENDPOINT, { email, apiKey })
    if (response.status === 200 && response.data.data.token) {
      return response.data.data.token
    }
    throw new Error('Authentication failed')
  } catch (error) {
    console.error('Error in authentication:', error.message)
    process.exit(1)
  }
}

// Function to read the API key from file or get it from the user
async function readApiKey() {
  try {
    const key = fs.readFileSync('./ws-api-key.txt', 'utf-8').trim()
    if (!key) throw new Error('Empty key file')
    return key
  } catch (error) {
    return new Promise((resolve) => {
      read.question('Enter your email: ', email => {
        read.question('Enter your API key: ', apiKey => {
          credentials = { email, apiKey }
          authenticateAndGetToken(email, apiKey)
            .then(token => {
              fs.writeFileSync('./ws-api-key.txt', token)
              resolve(token)
            })
        })
      })
    })
  }
}




function time() {
  return `\x1b[32m${new Date().toISOString().replace(/T/, ' ').replace(/\..+/, '')}\x1b[0m`
}

async function connect() {
  let lastPing = Date.now()
  const key = await readApiKey()

  const ws = new WebSocket(ENDPOINT, {
    headers: {
      'x-auth-token': key
    }
  })

  ws.on('open', function open() {
    console.log('Connected to', ENDPOINT)
    setInterval(() => {
      if (ws.readyState !== WebSocket.OPEN || Date.now() - lastPing > LAST_PING_TIMEOUT) {
        console.log('Connection lost, reconnecting...')
        ws.terminate()
        connect()
      }
    }, 30000)
  })

  ws.on('ping', function incoming() {
    const pingTime = Date.now() - lastPing
    lastPing = Date.now()
    console.log(`[${time()}] Ping:`, pingTime)
  })

  ws.on('message', function incoming(data) {
    console.log(`[${time()}] PAYLOAD:`, data.toString())
  })

  ws.on('error', function error(error) {
    console.log('ERROR:', arguments)
  })

  ws.on('close', async function close(code, reason) {
    console.log('the code', code, 'the reason', reason.toString())

    if (credentials.email && credentials.apiKey) {
      console.log('Re-authenticating due to 401 Unauthorized error...')
      const newToken = await authenticateAndGetToken(credentials.email, credentials.apiKey)
      fs.writeFileSync('./ws-api-key.txt', newToken)
      connect()
    } else {
      fs.writeFileSync('./ws-api-key.txt', '')
      console.log(`Disconnected (code: ${code}, reason: ${reason})`)
      connect()
    }
  })
}

connect()
