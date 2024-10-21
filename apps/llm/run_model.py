from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

def stream_process_output(command):
    """Execute a command and emit stdout line by line."""

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for stdout_line in process.stdout:
        socketio.emit('response', {'word': stdout_line})
        socketio.sleep(0.1)
    process.stdout.close()
    process.wait()

@socketio.on('query')
def start_stream(data=None):
    """Start the process and stream its stdout to the client."""

    if data is None:
        return

    query = data['query']

    print(f"query to send- {query}")

    command = ['python3', 'run_inference.py', '-m', 'Llama3-8B-1.58-100B-tokens-TQ2_0.gguf', '-p', query]
    socketio.start_background_task(target=stream_process_output, command=command)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
