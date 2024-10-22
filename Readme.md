# BitNet.js

BitNet.js is the unofficial Node.js implementation of Microsoft's [BitNet](https://github.com/microsoft/BitNet) project. This repository facilitates real-time interaction between a Node.js frontend and the BitNet Python model using **Socket.IO**. The app allows users to send queries to the BitNet LLM (Large Language Model) and receive responses line by line via a web interface.

## Working Example

Web app will display the results in real-time.

### Docker App Run

![bitnet js-docker-run](https://github.com/user-attachments/assets/8c439904-fec7-4465-ac7d-5ebfc29d2442)

### Web Interface Interaction

![bitnet js-llm](https://github.com/user-attachments/assets/4c266ff4-bc69-4935-9922-81816216166b)

## Features

- **Web-based interface**: A simple frontend built with HTML and JavaScript to interact with the BitNet model.
- **Real-time communication**: Uses **Socket.IO** for bi-directional communication between the Node.js app and the Python-based BitNet model.
- **Dockerized environment**: Both the Node.js app and BitNet model run in separate Docker containers managed by **docker compose**.

## Directory Structure

```bash
bitnet.js/
├── apps/
│   ├── llm/
│   │   └── Dockerfile              # Dockerfile for the BitNet model
│   │   └── requirements-local.txt  # List of packages that are used in Local Server
│   │   └── run_model.py            # Local Python Server to start Socket
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
3. The response will be returned **word by word** in real-time.

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

## Docker Configuration

### apps/llm/Dockerfile (Python LLM)

This Dockerfile sets up the environment for running the BitNet model. It includes the necessary dependencies and commands to launch the model server.

```dockerfile
FROM python:3.9-alpine

# Install necessary dependencies and tools
RUN apk add --no-cache build-base cmake clang git && \
    rm -rf /var/cache/apk/*

# Clone the BitNet repository without history
RUN git clone --recursive --depth 1 https://github.com/microsoft/BitNet.git && \
    rm -rf BitNet/.git

WORKDIR /BitNet

# Install Python dependencies
RUN pip install -r requirements.txt && \
    pip cache purge

# Copy the local requirements.txt for additional dependencies
COPY requirements-local.txt .

# Install additional dependencies from the local requirements file
RUN pip install -r requirements-local.txt && \
    pip cache purge

# Run the code generation for Llama3-8B model
RUN python3 utils/codegen_tl2.py --model Llama3-8B-1.58-100B-tokens --BM 256,128,256,128 --BK 96,96,96,96 --bm 32,32,32,32

# Build the model using cmake with specified compilers
RUN cmake -B build -DBITNET_X86_TL2=ON -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ && \
    cmake --build build --target llama-cli --config Release

# Download the Llama model from HuggingFace
ADD https://huggingface.co/brunopio/Llama3-8B-1.58-100B-tokens-GGUF/resolve/main/Llama3-8B-1.58-100B-tokens-TQ2_0.gguf .

# Verify the integrity of the model file
RUN echo "2565559c82a1d03ecd1101f536c5e99418d07e55a88bd5e391ed734f6b3989ac Llama3-8B-1.58-100B-tokens-TQ2_0.gguf" | sha256sum -c

# Expose port for communication with the Node.js app
EXPOSE 5000

# Run a Python script that handles queries from the Node.js app using socket.io
COPY run_model.py .

# Run the model in inference mode, listening for queries
CMD ["python3", "run_model.py", "-m", "Llama3-8B-1.58-100B-tokens-TQ2_0.gguf"]
```

### apps/web/Dockerfile (Node.js Application)

This Dockerfile sets up the Node.js application environment. It installs required packages and specifies how to run the application.

```dockerfile
# Base image for Node.js
FROM node:16-alpine

# Set working directory
WORKDIR /usr/src/app

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy app files
COPY . .

# Expose port
EXPOSE 3000

# Run the Node.js app
CMD ["node", "app.js"]
```

### docker-compose.yml

The `docker-compose.yml` file defines the services for both the Node.js and BitNet containers.

```yml
version: '3'
services:
  llm:
    build:
      context: ./apps/llm
    container_name: llm
    ports:
      - "5000:5000"
    networks:
      - app-network
    tty: True

  web:
    build:
      context: ./apps/web
    container_name: web
    ports:
      - "3000:3000"
    depends_on:
      - llm
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
