import asyncio
import os
import requests
import websockets
from datetime import datetime

AUTH_ENDPOINT = "https://www.theblock.pro/api-public/v1/users/auth"
ENDPOINT = "wss://www.theblock.pro/api-public/v1/news/live"
LAST_PING_TIMEOUT = 60000

credentials = {"email": "", "api_key": ""}


async def authenticate_and_get_token(email, api_key):
    try:
        response = requests.post(
            AUTH_ENDPOINT, json={"email": email, "apiKey": api_key}
        )
        if response.status_code == 200 and response.json()["data"]["token"]:
            return response.json()["data"]["token"]
        raise Exception("Authentication failed")
    except Exception as e:
        print(f"Error in authentication: {e}")
        exit(1)


async def read_api_key():
    try:
        with open("./ws-api-key.txt", "r") as file:
            key = file.read().strip()
            if not key:
                raise Exception("Empty key file")
            return key
    except Exception:
        email = input("Enter your email: ")
        api_key = input("Enter your API key: ")
        credentials["email"] = email
        credentials["api_key"] = api_key
        token = await authenticate_and_get_token(email, api_key)
        with open("./ws-api-key.txt", "w") as file:
            file.write(token)
        return token


def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


async def connect():
    last_ping = datetime.now().timestamp() * 1000
    key = await read_api_key()

    async with websockets.connect(ENDPOINT, extra_headers={"x-auth-token": key}) as ws:
        print("Connected to", ENDPOINT)
        while True:
            try:
                if datetime.now().timestamp() * 1000 - last_ping > LAST_PING_TIMEOUT:
                    print("Connection lost, reconnecting...")
                    await ws.close()
                    await connect()

                message = await ws.recv()
                print(f"[{current_time()}] PAYLOAD:", message)

            except websockets.exceptions.ConnectionClosed as e:
                print("ERROR:", e)
                if credentials["email"] and credentials["api_key"]:
                    print("Re-authenticating due to 401 Unauthorized error...")
                    new_token = await authenticate_and_get_token(
                        credentials["email"], credentials["api_key"]
                    )
                    with open("./ws-api-key.txt", "w") as file:
                        file.write(new_token)
                    await connect()
                else:
                    with open("./ws-api-key.txt", "w") as file:
                        file.write("")
                    print(f"Disconnected (code: {e.code}, reason: {e.reason})")
                    await connect()


asyncio.run(connect())
