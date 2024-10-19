from flask import Flask
from flask_socketio import SocketIO, emit
import subprocess
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

# SocketIO event for real-time query handling
@socketio.on('query')
def handle_socket_query(data):
    query = data['query']
    print(f"Received query: {query}")

    # Get the SocketIO client ID (session ID) from the request context
    client_sid = data.get('sid')

    def run_model():
        # Run the Llama inference model with the query
        process = subprocess.Popen(
            ['python3', 'run_inference.py', '-m', 'Llama3-8B-1.58-100B-tokens-TQ2_0.gguf', '-p', query],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        # Read the output line by line
        for line in process.stdout:
            words = line.strip().split()
            for word in words:
                # Emit each word back to the specific client
                socketio.emit('response', {'word': word}, room=client_sid)
        process.stdout.close()
        process.wait()

    # Run the model in a separate thread
    threading.Thread(target=run_model).start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
