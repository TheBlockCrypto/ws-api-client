import asyncio
import requests
import websockets
from datetime import datetime

ENDPOINT = "wss://www.theblock.co/ws"
# ENDPOINT = "ws://localhost:4000/ws"

LAST_PING_TIMEOUT = 60000


async def read_api_key():
    try:
        with open("./ws-api-key.txt", "r") as file:
            key = file.read().strip()
            if not key:
                raise Exception("Empty key file")
            return key
    except Exception:
        raise Exception("API key file not found or empty")


def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


async def connect():
    last_ping = datetime.now().timestamp() * 1000

    key = await read_api_key()

    async with websockets.connect(ENDPOINT, extra_headers={"x-auth-token": key}) as ws:
        print("Connected to", ENDPOINT)
        while True:
            try:
                message = await ws.recv()
                print(f"[{current_time()}] PAYLOAD:", message)

            except websockets.exceptions.ConnectionClosed as e:
                print("ERROR:", e)
                await asyncio.sleep(10)
                await connect()


asyncio.run(connect())
