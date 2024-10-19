const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const clientIo = require('socket.io-client');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

// Connect to Python Socket.IO server
const pythonSocket = clientIo.connect('http://llm:5000');

// Serve static files (HTML)
app.use(express.static(__dirname));

// Socket connection with browser client
io.on('connection', (socket) => {
  console.log('New browser client connected');

  // When a query is received from the browser client
  socket.on('query', (query) => {
    console.log(`Received query from browser: ${query}`);

    // Forward the query to the Python server
    pythonSocket.emit('query', { query });
  });

  // Receive words from Python server and send to browser client
  pythonSocket.on('response', (data) => {
    const word = data.word;
    console.log(`Received word from Python: ${word}`);

    // Emit the word to the browser client
    socket.emit('response', word);
  });

  socket.on('disconnect', () => {
    console.log('Browser client disconnected');
  });
});

// Handle Python server connection events
pythonSocket.on('connect', () => {
  console.log('Connected to Python server');
});

pythonSocket.on('disconnect', () => {
  console.log('Disconnected from Python server');
});

server.listen(3000, () => {
  console.log('Node.js app listening on port 3000');
});
