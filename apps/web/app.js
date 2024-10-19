const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const axios = require('axios');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

// Serve static files (HTML)
app.use(express.static(__dirname));

// Socket connection
io.on('connection', (socket) => {
  console.log('New client connected');

  socket.on('query', async (query) => {
    try {
      // Send query to Python model and get the response
      const response = await axios.post('http://llm:5000/query', { query });
      socket.emit('response', response.data);
    } catch (error) {
      console.error('Error:', error);
    }
  });

  socket.on('disconnect', () => {
    console.log('Client disconnected');
  });
});

server.listen(3000, () => {
  console.log('Node.js app listening on port 3000');
});
