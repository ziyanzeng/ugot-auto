import asyncio
import signal
import websockets
import json
import numpy as np
from utils import PID

async def pid_tuner(websocket, path):
    pid = PID(1.0, 0.0, 0.0)
    try:
        while True:
            message = await websocket.recv()
            pid_values = json.loads(message)

            kp = pid_values['kp']
            ki = pid_values['ki']
            kd = pid_values['kd']

            pid.set_pid(kp, ki, kd)

            time, response = get_robot_response(pid, target=1.0)
            data = {
                'time': time.tolist(),
                'response': response.tolist()
            }
            await websocket.send(json.dumps(data))
    except websockets.ConnectionClosed:
        print("Client disconnected")

def get_robot_response(pid, target, duration=10, dt=0.1):
    t = np.arange(0, duration, dt)
    response = []
    current_value = 0.0
    for _ in t:
        error = target - current_value
        control_signal = pid.update(error)
        current_value += control_signal * dt  # Simple model: response is proportional to control signal
        response.append(current_value)
    return t, response

def start_server():
    loop = asyncio.get_event_loop()
    start_server = websockets.serve(pid_tuner, "localhost", 8765)

    # Handle signal for clean shutdown
    def shutdown():
        print("Shutting down server...")
        start_server.ws_server.close()
        loop.stop()

    for signame in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, signame), shutdown)

    loop.run_until_complete(start_server)
    loop.run_forever()

if __name__ == "__main__":
    start_server()
