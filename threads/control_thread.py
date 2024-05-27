import time
from commands.CommandPlanner import CommandPlanner
import utils
from config import shared_data
from logger import logger  # Import the global logger

def control_thread(got):
    # Create PID controllers
    pid_linear = utils.PID(kp=0.1, ki=0.01, kd=0.05)
    pid_angle = utils.PID(kp=0.1, ki=0.01, kd=0.05)
    pid_controllers = {
        "linear": pid_linear,
        "angle": pid_angle
    }

    command_planner = CommandPlanner(got, shared_data, pid_controllers)

    while True:
        with shared_data["lock"]:
            if shared_data["exit"]:
                break

            if shared_data["detections"] is not None:
                frame_width = shared_data["frame_width"]
                frame_height = shared_data["frame_height"]
                detections = shared_data["detections"]

                distance, angle = utils.get_single_relative_pos(detections, frame_width, frame_height)
                command_planner.update(distance, angle)

                # Log the detection results
                logger.info(f'Detection results - Distance: {distance}, Angle: {angle}')
            else:
                logger.info('No detections found')

        time.sleep(0.1)  # Control loop interval

    logger.info('Control thread exited')
