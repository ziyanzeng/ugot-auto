import asyncio
import signal
import websockets
import json
from shared_data import shared_data
from logger import logger

class WSServer:
    def __init__(self):
        self.current_command = None
        self.clients = set()

    async def pid_tuner(self, websocket, path):
        logger.info('New WebSocket connection established')
        self.clients.add(websocket)
        try:
            while True:
                message = await websocket.recv()
                logger.info(f'Received message: {message}')
                data = json.loads(message)

                if 'linear' in data and 'angle' in data:
                    shared_data["linear_pid"].set_pid(data['linear']['kp'], data['linear']['ki'], data['linear']['kd'])
                    shared_data["angle_pid"].set_pid(data['angle']['kp'], data['angle']['ki'], data['angle']['kd'])
                    logger.info(f'Updated PID parameters: {data}')

                if 'command' in data:
                    shared_data["command"] = data['command']
                    self.current_command = data['command']
                    logger.info(f'Received command: {self.current_command}')

                # For testing purposes, send back the updated shared data
                response_data = {
                    'linear_pid': {
                        'kp': shared_data["linear_pid"].kp,
                        'ki': shared_data["linear_pid"].ki,
                        'kd': shared_data["linear_pid"].kd
                    },
                    'angle_pid': {
                        'kp': shared_data["angle_pid"].kp,
                        'ki': shared_data["angle_pid"].ki,
                        'kd': shared_data["angle_pid"].kd
                    },
                    'command': shared_data["command"]
                }
                await websocket.send(json.dumps(response_data))
                logger.info('Sent updated data back to client')
        except websockets.ConnectionClosed:
            logger.info("Client disconnected")
        except KeyError as e:
            logger.error(f"KeyError: {e}")
        finally:
            self.clients.remove(websocket)

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

    logger.info("WebSocket server started")
    loop.run_until_complete(start_server)
    loop.run_forever()

if __name__ == "__main__":
    start_server()
