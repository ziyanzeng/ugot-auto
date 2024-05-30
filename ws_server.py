import asyncio
import websockets
import json
from shared_data import SharedData
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
                    SharedData.shared_data["linear_pid"].set_pid(data['linear']['kp'], data['linear']['ki'], data['linear']['kd'])
                    SharedData.shared_data["angle_pid"].set_pid(data['angle']['kp'], data['angle']['ki'], data['angle']['kd'])
                    logger.info(f'Updated PID parameters: {data}')

                if 'command' in data:
                    SharedData.shared_data["command"] = data['command']
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
                logger.info('Sent updated data back to client')
        except websockets.ConnectionClosed:
            logger.info("Client disconnected")
        except KeyError as e:
            logger.error(f"KeyError: {e}")
        finally:
            self.clients.remove(websocket)
            
    def get_robot_response(self):
        time_data = list(range(len(SharedData.shared_data["distance_history"])))
        distance_data = SharedData.shared_data["distance_history"]
        angle_data = SharedData.shared_data["angle_history"]
        return time_data, distance_data, angle_data

def start_server(shutdown_event):
    ws_server = WSServer()
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    start_server = websockets.serve(ws_server.pid_tuner, "localhost", 8765)

    async def shutdown():
        logger.info("Shutting down server...")
        await start_server.ws_server.close()
        loop.stop()

    async def run_server():
        await start_server
        while not shutdown_event.is_set():
            await asyncio.sleep(1)
        await shutdown()

    logger.info("WebSocket server started")
    loop.run_until_complete(run_server())
    loop.run_forever()
