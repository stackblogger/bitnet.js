from flask import Flask
from flask_socketio import SocketIO, emit
import subprocess
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

# Global variable to manage thread control
stop_event = threading.Event()
# Global variable to store the process reference
current_process = None

def stream_process_output(command):
    """Execute a command and emit stdout line by line, with thread control."""
    global current_process

    # Start the subprocess
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    current_process = process  # Store the reference to the current process

    for stdout_line in process.stdout:
        if stop_event.is_set():  # Stop if the event is triggered
            break
        socketio.emit('response', {'word': stdout_line})
        socketio.sleep(0.1)  # Yield to allow other threads to run

    process.stdout.close()
    process.wait()

@socketio.on('query')
def start_stream(data=None):
    """Start the process and stream its stdout to the client, ensuring thread control."""
    global stop_event, current_process

    if data is None:
        return

    query = data['query']

    command = ['python3', 'run_inference.py', '-m', 'Llama3-8B-1.58-100B-tokens-TQ2_0.gguf', '-p', query]

    if 'args' in data and data.get('args'):
        additional_args = data['args'].strip().split()
        command.extend(additional_args)

    print(f"command- {command}")

    # If there is an existing running task, terminate it
    if current_process and current_process.poll() is None:
        current_process.terminate()

    stop_event.set()  # Signal the current thread to stop
    stop_event.clear()  # Reset the stop event for the new thread

    # Start a new background task
    socketio.start_background_task(target=stream_process_output, command=command)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
