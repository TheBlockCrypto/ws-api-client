const WebSocket = require("ws");
const fs = require("fs");
const { DateTime } = require("luxon");

const ENDPOINT = "wss://www.theblock.co/ws";
// const ENDPOINT = 'ws://localhost:4000/ws';

const LAST_PING_TIMEOUT = 60000;
const PING_INTERVAL = 25000; // 25 seconds

async function readApiKey() {
  try {
    const key = fs.readFileSync("./ws-api-key.txt", "utf8").trim();
    if (!key) {
      throw new Error("Empty key file");
    }
    return key;
  } catch (error) {
    throw new Error("API key file not found or empty");
  }
}

function currentTime() {
  return DateTime.now().toFormat("yyyy-MM-dd HH:mm:ss");
}

async function connect() {
  let lastPing = DateTime.local().toMillis();

  const key = await readApiKey();

  const ws = new WebSocket(ENDPOINT, {
    headers: {
      "x-auth-token": key,
    },
  });

  ws.on("open", () => {
    console.log("Connected to", ENDPOINT);
    // Start the ping interval
    setInterval(() => {
      if (DateTime.local().toMillis() - lastPing > LAST_PING_TIMEOUT) {
        console.log("Ping timeout, reconnecting...");
        ws.terminate(); // Close the connection
        connect(); // Reconnect
      } else {
        ws.ping(); // Send ping
      }
    }, PING_INTERVAL);
  });

  ws.on("message", (message) => {
    console.log(`[${currentTime()}] PAYLOAD:`, message.toString());
  });

  ws.on("close", function close() {
    console.log("Connection closed");
    setTimeout(connect, 10000);
  });

  ws.on("error", function error(err) {
    console.error("ERROR:", err.message);
    setTimeout(connect, 10000);
  });

  ws.on("pong", function pong() {
    lastPing = DateTime.local().toMillis();
    console.log(`[${currentTime()}] pong`);
  });
}

connect();
