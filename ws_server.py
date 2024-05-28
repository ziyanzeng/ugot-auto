import asyncio
import websockets
import json
import numpy as np
from utils import PID  # 假设您有一个单独的PID实现

async def pid_tuner(websocket, path):
    pid = PID()
    while True:
        message = await websocket.recv()
        pid_values = json.loads(message)

        kp = pid_values['kp']
        ki = pid_values['ki']
        kd = pid_values['kd']

        pid.kp = kp
        pid.ki = ki
        pid.kd = kd

        time, response = get_robot_response(pid, target=1.0)
        data = {
            'time': time.tolist(),
            'response': response.tolist()
        }
        await websocket.send(json.dumps(data))

def get_robot_response(pid, target, duration=10, dt=0.1):
    t = np.arange(0, duration, dt)
    response = []
    current_value = 0.0
    for _ in t:
        error = target - current_value
        control_signal = pid.update(error, dt)
        current_value += control_signal * dt  # Simple model: response is proportional to control signal
        response.append(current_value)
    return t, response

start_server = websockets.serve(pid_tuner, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
