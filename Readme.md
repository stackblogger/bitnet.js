# BitNet.js

BitNet.js is the Node.js implementation of Microsoft's [bitnet.cpp](https://github.com/microsoft/BitNet) inference framework. This repository facilitates real-time interaction between a Node.js frontend and the bitnet 1-bit LLM model using **Socket.IO**. The app allows users to send queries to the BitNet LLM (Large Language Model) and receive responses line by line via a web interface.

## Working Example

Web app will display the results in real-time.

### Docker App Run

![bitnet js-docker-run](https://github.com/user-attachments/assets/8c439904-fec7-4465-ac7d-5ebfc29d2442)

### Web Interface Interaction

![bitnet js-llm](https://github.com/user-attachments/assets/83882cf5-0fb4-4fe4-9068-6447e26c4283)


## Features

- **Web-based interface**: A simple frontend built with HTML and JavaScript to interact with the BitNet model.
- **Real-time communication**: Uses **Socket.IO** for bi-directional communication between the Node.js app and the Python-based BitNet model.
- **Dockerized environment**: Both the Node.js app and BitNet model run in separate Docker containers managed by **docker compose**.

## Directory Structure

```bash
bitnet.js/
├── apps/
│   ├── llm/
│   │   ├── Dockerfile              # Dockerfile for the BitNet model
│   │   ├── requirements-local.txt  # List of packages that are used in Local Server
│   │   ├── run_model.py            # Local Python Server to start Socket
│   ├── web/
│   │   ├── Dockerfile              # Dockerfile for the Node.js application
│   │   ├── app.js                  # Node.js app (Socket.IO client)
│   │   ├── index.html              # Frontend (textarea for input, display for output)
├── docker-compose.yml              # Compose file to run both containers together
├── README.md                       # Documentation
```

## Prerequisites

- **Docker**: Ensure Docker is installed. [Install Docker](https://docs.docker.com/get-docker/)

## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/stackblogger/bitnet.js.git
cd bitnet.js
```

### Step 2: Build and Run Containers

To build and start both the Node.js app and the BitNet model, use:

```bash
docker compose up --build -d
```

This command will build the Docker images for both the **web** (Node.js) and **llm** (Python) containers, and run the services defined in the `docker-compose.yml` file.

### Step 3: Access the Web Application

After starting the containers, access the web interface by navigating to:

`http://localhost:3000`

You'll see a textarea where you can input your queries and send them to the BitNet model.

### Step 4: Interact with the BitNet Model

1. **Enter a query** in the provided textarea (e.g., "Why is the sky blue?").
2. **Click Send**. Your query is transmitted to the BitNet model via Socket.IO.
3. The response will be returned **line by line** in real-time.

## How it Works

- The **Node.js application** (in `apps/web`) serves a simple web interface where users can input their queries. The application connects to the **Python backend** using Socket.IO.
- The **Python app** (in `apps/llm`) runs the BitNet model, processes the queries, and streams the response back to the Node.js client, word by word.
- Both applications are containerized and communicate through **docker compose**.

### Node.js Frontend (app.js)

The Node.js frontend sends user queries to the backend via a Socket.IO connection. Here's the simplified workflow:

1. **User Input**: The user enters a query and clicks "Send."
2. **Socket Emission**: The query is sent to the backend using Socket.IO.
3. **Receive Data**: The response is received word by word and displayed on the page.

### Python Backend (BitNet Integration)

The Python backend runs the BitNet model and returns the response:

1. **Receive Query**: The Python app receives a query from the Node.js frontend.
2. **Model Inference**: The query is processed by the BitNet model.
3. **Stream Results**: The model's response is streamed word by word back to the Node.js client.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
