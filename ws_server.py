import asyncio
import signal
import websockets
import json
import numpy as np
from utils.pid_controller import PID
from config import shared_data
from logger import logger

class WSServer:
    def __init__(self):
        self.current_command = None
        self.clients = set()

    async def pid_tuner(self, websocket, path):
        self.clients.add(websocket)
        try:
            while True:
                message = await websocket.recv()
                data = json.loads(message)

                if 'linear' in data and 'angle' in data:
                    shared_data["linear_pid"].set_pid(data['linear']['kp'], data['linear']['ki'], data['linear']['kd'])
                    shared_data["angle_pid"].set_pid(data['angle']['kp'], data['angle']['ki'], data['angle']['kd'])
                    logger.info('PID parameters updated from WebSocket')

                if 'command' in data:
                    self.current_command = data['command']
                    logger.info(f'Received command: {self.current_command}')

                time_data, distance_data, angle_data = self.get_robot_response()
                response_data = {
                    'type': 'chart',
                    'time': time_data,
                    'distance': distance_data,
                    'angle': angle_data
                }
                await websocket.send(json.dumps(response_data))
        except websockets.ConnectionClosed:
            print("Client disconnected")
        finally:
            self.clients.remove(websocket)

    def get_robot_response(self):
        time_data = list(range(len(shared_data["distance_history"])))
        distance_data = shared_data["distance_history"]
        angle_data = shared_data["angle_history"]
        return time_data, distance_data, angle_data

    async def send_video_frame(self, frame):
        if self.clients:
            message = json.dumps({
                'type': 'video',
                'frame': frame
            })
            await asyncio.wait([client.send(message) for client in self.clients])

def start_server():
    ws_server = WSServer()
    loop = asyncio.get_event_loop()
    start_server = websockets.serve(ws_server.pid_tuner, "localhost", 8765)

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
