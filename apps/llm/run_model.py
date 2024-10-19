import socketio
from flask import Flask, request, jsonify
import subprocess

# Initialize Flask and Socket.io
app = Flask(__name__)
sio = socketio.Client()

# Route to handle incoming query requests
@app.route('/query', methods=['POST'])
def handle_query():
    data = request.json
    query = data['query']
    
    # Run the Llama inference model with the query
    result = subprocess.run(
        ['python3', 'run_inference.py', '-m', 'Llama3-8B-1.58-100B-tokens-TQ2_0.gguf', '-p', query],
        capture_output=True,
        text=True
    )
    
    # Return the model's response
    return jsonify(result=result.stdout)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
