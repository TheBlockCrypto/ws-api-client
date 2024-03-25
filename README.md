# TheBlock Priority API WebSocket Client

This project is a WebSocket client for the TheBlock Priority API service. It provides real-time updates on various cryptocurrencies and blockchain-related news.

## Features

- Real-time news updates via WebSocket.
- Automatic reconnection and authentication handling.
- Stores authentication token for persistent connections.
- Optional filtering for specific tokens or priority levels in news updates.

## Requirements [ Node ]

- Node.js (16+)
- WebSocket (`ws` package)
- Filesystem access (`fs` package)

## Requirements [ Python ]

- Python
- WebSocket (`websockets` package)
- Request (`requests` package)

### API Key Generation

- An API key is necessary to access TheBlock's news feed.
- You can generate this key by visiting [TheBlock API Key Generation](https://www.theblock.pro/api-public/).
- Follow the instructions on the website to create and retrieve your API key.

## Installation

Clone the repository and install dependencies:

```bash
git clone [repository-url]
cd [repository-name]
```

### Node

```bash
yarn install
```

### Pythion

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Node

```bash
yarn start
```

### Python

```bash
python ws-api-client.py

```

> On first run, the script will prompt for an email and API key. These credentials are used to authenticate with TheBlock Pro API service and receive an authentication token.

## Configuration

### API Key and Email

- The script requires an API key and email for authentication.
- If the `ws-api-key.txt` file is empty, the script will prompt you to enter these details.
- The script will then automatically authenticate with TheBlock's auth endpoint and store the token for future use.

### WebSocket Endpoint

- The default WebSocket endpoint is set to receive all news without filters.
- You can modify the endpoint in the script to apply filters for specific tokens or priority levels.

### Connection Handling

- The script includes automatic reconnection logic.
- A heartbeat is sent every 30 seconds to keep the connection alive.
- If the connection is lost, the script attempts to reconnect.

## Events

### Open Event

- Triggered when the WebSocket connection is successfully established.
- Logs a confirmation message with the connected endpoint.

### Ping Event

- Handles incoming pings from the server.
- Logs the ping time for monitoring latency.

### Message Event

- Triggered on receiving a new message (news update).
- Logs the received payload for real-time updates.

### Close Event

- Triggered when the WebSocket connection is closed.
- Logs the closure code and reason.

## Error Handling

- The script includes error handling for WebSocket events.
- If a `401` status code is encountered, the script re-authenticates using the last used email and API key.

## Troubleshooting

- **Connection Issues**: If you face connection issues, check your internet connection and the WebSocket endpoint URL.
- **Authentication Failure**: If authentication fails, ensure your API key and email are correct. The script will re-authenticate automatically on a `401` error.
- **WebSocket Errors**: For errors related to WebSocket, refer to the [WebSocket documentation](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) for troubleshooting.

## Contributing

- Contributions to improve the script or documentation are welcome.
- Please follow the project's coding standards and submit pull requests for review.

## License

- This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).

For more information or assistance, feel free to open an issue in the project repository.
