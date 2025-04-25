import asyncio
import json
import os
import requests
import websockets
from datetime import datetime, timezone

AUTH_ENDPOINT = "https://www.theblock.pro/api-public/v1/users/auth"
#ENDPOINT = 'wss://www.theblock.pro/api-public/v1/news/live'
#ENDPOINT = "ws://priority-api.theblockpro.localhost/api-public/v1/news/live"
ENDPOINT = "wss://priority-api.theblock.pro/api-public/v1/news/live?channel=news_published,news_stream,echo"

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
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


async def connect():
    last_ping = datetime.now(timezone.utc).timestamp() * 1000
    key = await read_api_key()

    async with websockets.connect(ENDPOINT, extra_headers={"x-auth-token": key}, ping_interval=20, ping_timeout=10) as ws:
        print("Connected to", ENDPOINT)

        # Setup ping handler
        async def ping_handler():
            nonlocal last_ping
            while True:
                try:
                    last_ping = datetime.now(timezone.utc).timestamp() * 1000
                    # Send ping and wait for pong
                    pong_waiter = await ws.ping()
                    await pong_waiter
                    ping_time = datetime.now(timezone.utc).timestamp() * 1000 - last_ping
                    print(f"[{current_time()}] Ping: {ping_time:.2f}ms")
                    await asyncio.sleep(30)  # Send ping every 30 seconds
                except Exception as e:
                    print(f"Ping error: {e}")
                    break

        # Start ping handler in background
        ping_task = asyncio.create_task(ping_handler())
        
        while True:
            try:
                # Check for ping timeout
                if datetime.now(timezone.utc).timestamp() * 1000 - last_ping > LAST_PING_TIMEOUT:
                    print("Connection lost due to ping timeout, reconnecting...")
                    ping_task.cancel()
                    await ws.close()
                    await asyncio.sleep(5)
                    await connect()
                    return

                message_str = await ws.recv()
                try:
                    message_data = json.loads(message_str)
                    
                    elapsed_time_str = "N/A"
                    if 'payload' in message_data and 'published' in message_data['payload']:
                        try:
                            published_str = message_data['payload']['published']
                            published_dt = datetime.fromisoformat(published_str)
                            now_utc = datetime.now(timezone.utc)
                            elapsed_time = now_utc - published_dt
                            elapsed_time_str = str(elapsed_time)
                        except ValueError as e:
                            print(f"Error parsing published timestamp: {e}")
                        except KeyError as e:
                            print(f"Missing key in payload: {e}")
                    
                    print(f"[{current_time()}] Elapsed: {elapsed_time_str} | PAYLOAD:", message_str)
                except json.JSONDecodeError:
                    # Handle non-JSON messages
                    print(f"[{current_time()}] Non-JSON message received: {message_str}")

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
                    return
                else:
                    with open("./ws-api-key.txt", "w") as file:
                        file.write("")
                    print(f"Disconnected (code: {e.code}, reason: {e.reason})")
                    await asyncio.sleep(5)
                    await connect()
                    return


asyncio.run(connect())
