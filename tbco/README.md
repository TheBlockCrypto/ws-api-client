# theblock.co API WebSocket Client

## Python Version

### Requirements

- Python 3.x
- Included dependencies
- websockets library

### Installation

1. Install Python 3.x if not already installed: [Python Downloads](https://www.python.org/downloads/)
2. Install required libraries using pip:

### Usage

1. Obtain the WebSocket API key from your provider and save it in a file named `ws-api-key.txt` in the same directory as the Python script.
2. Run the Python script using the following command:

```bash
python ws-api-client.py
```

## JavaScript Version

## Requirements [ Node ]

- Node.js (16+)
- Included dependencies
- Filesystem access (`fs` package)

### Installation

1. Install Node.js if not already installed: [Node.js Downloads](https://nodejs.org/en/download/)
2. Create a new directory for your project and navigate to it in your terminal.
3. Initialize a new Node.js project and install required packages using yarn or npm (yarn):

### Usage

1. Obtain the WebSocket API key from your provider and save it in a file named `ws-api-key.txt` in the root directory of your project.
2. Save the JavaScript code in a file named `ws-api-client.js` in the root directory of your project.
3. Run the JavaScript script using Node.js:

> Note you must manually send the keepalive (ping) event in the nodejs version, this is not necessary in the python version.

```bash
yarn start
```
