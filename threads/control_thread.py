import time
from commands.CommandPlanner import CommandPlanner
import utils
from config import shared_data
from logger import logger  # Import the global logger

def control_thread(got, condition):
    # Create PID controllers
    pid_linear = utils.PID(kp=0.1, ki=0.01, kd=0.05)
    pid_angle = utils.PID(kp=0.1, ki=0.01, kd=0.05)
    pid_controllers = {
        "linear": pid_linear,
        "angle": pid_angle
    }

    command_planner = CommandPlanner(got, pid_controllers)
    logger.info("Control thread started")

    while True:
        with condition:
            condition.wait()  # Wait for notification from the camera thread

        distance, angle = None, None
        detections_exist = False

        with shared_data["lock"]:
            if shared_data["exit"]:
                break

            if shared_data["detections"] is not None:
                frame_width = shared_data["frame_width"]
                frame_height = shared_data["frame_height"]
                detections = shared_data["detections"]

                distance, angle = utils.get_single_relative_pos(detections, frame_width, frame_height)
                shared_data["distance"] = distance
                shared_data["angle"] = angle
                logger.info(f'Updating command planner with distance: {distance}, angle: {angle}')
            else:
                logger.info('No detections found')

        command_planner.update(distance, angle)
        logger.info('Command planner updated')

        time.sleep(0.1)  # Control loop interval

    logger.info('Control thread exited')
