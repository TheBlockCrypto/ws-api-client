const WebSocket = require('ws')
const fs = require('fs')

//const ENDPOINT = 'wss://www.theblock.pro/api-public/v1/news/live?tokens=btc,eth,aave,ada,algo,bnb,bch,eos,luna' //token filter
//const ENDPOINT = 'wss://www.theblock.pro/api-public/v1/news/live?priority=1,2,3' //priority filter
const ENDPOINT =  'wss://www.theblock.pro/api-public/v1/news/live' //no filter
const AUTH_ENDPOINT = 'https://www.theblock.pro/api-public/v1/auth'

const LAST_PING_TIMEOUT = 60000

// Read the key from the text file
const key = fs.readFileSync('./ws-api-key.txt', 'utf-8').trim()

function time() {
  const cliGreenCode = '\x1b[32m'
  return [cliGreenCode, new Date().toISOString().replace(/T/, ' ').replace(/\..+/, ''), '\x1b[0m'].join('')
}

// Connect to the WebSocket
function connect() {
  let lastPing = Date.now()

  const ws = new WebSocket(ENDPOINT, {
    headers: {
      'x-auth-token': key
    }
  })
  
  ws.on('open', function open() {
    console.log('Connected to', ENDPOINT)
  
    // Send a heartbeat every 30 seconds
    let lastSetInterval = setInterval(() => {
      if (ws.readyState !== WebSocket.OPEN || Date.now() - lastPing > LAST_PING_TIMEOUT) {
        console.log('Connection lost, reconnecting...')
        ws.terminate()
        clearInterval(lastSetInterval)
        connect()
      }
    }, 30000)
  })
  
  ws.on('ping', function incoming() {
    // Calculate the ping time
    const pingTime = Date.now() - lastPing;
    lastPing = Date.now()
    const datetimeStringwithMilliseconds = 

    console.log(`[${time()}] Ping:`, pingTime)
  })

  ws.on('message', function incoming(data) {
    console.log(`[${time()}] PAYLOAD:`, data.toString())
  })
  
  ws.on('close', function close(code, reason) {
    console.log(`Disconnected (code: ${code}, reason: ${reason})`)
  })
}

connect()