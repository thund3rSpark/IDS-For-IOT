from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import time
import logging
import random

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Simulate a machine learning model
def predict(packet):
    # Replace with your actual model prediction
    if packet["packet_size"] > 1000:  # Example rule
        return 1  # Attack
    else:
        return 0  # Benign

# Simulate packet generation
def generate_simulated_packet():
    return {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "packet_size": random.randint(50, 1500),  # Random packet size
        "protocol": random.choice(["TCP", "UDP", "ICMP"]),  # Random protocol
        "flags": random.choice(["SYN", "ACK", "FIN", "RST"]),  # Random flags
    }

# Simulate real-time updates
def simulate_real_time_updates():
    while True:
        time.sleep(1)  # Simulate a delay
        packet = generate_simulated_packet()
        prediction = predict(packet)
        attack_type = "Attack" if prediction == 1 else "Benign"
        
        # Send data to the frontend
        socketio.emit('new_prediction', {
            'timestamp': packet["timestamp"],
            'attack_type': attack_type,
            'packet_size': packet["packet_size"]
        })
        logging.debug(f"Simulated packet: {packet}, Prediction: {attack_type}")

@app.route('/')
def index():
    logging.debug("Serving index.html")
    return render_template('index.html')

if __name__ == '__main__':
    try:
        # Start simulating real-time updates in a separate thread
        threading.Thread(target=simulate_real_time_updates, daemon=True).start()
        socketio.run(app, port=5001, debug=True)
    except Exception as e:
        logging.error(f"Error starting application: {e}")