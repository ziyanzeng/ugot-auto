# import time
# from commands.CommandPlanner import CommandPlanner
# import utils
# from shared_data import shared_data
# from logger import logger  # Import the global logger

# def control_thread(got, condition):
#     # Create PID controllers
#     pid_linear = utils.PID(kp=0.8, ki=0.1, kd=0.05)
#     pid_angle = utils.PID(kp=2, ki=0.01, kd=0.05)
#     pid_controllers = {
#         "linear": pid_linear,
#         "angle": pid_angle
#     }

#     command_planner = CommandPlanner(got, pid_controllers)
#     logger.info("Control thread started")

#     while True:
#         with condition:
#             condition.wait()  # Wait for notification from the camera thread
            
#         with shared_data["lock"]:
#             if shared_data["exit"]:
#                 break

#             if shared_data["detections"] is not None:
#                 distance, angle = shared_data["distance"], shared_data["angle"]
#                 # logger.info(f'Updating command planner with distance: {distance}, angle: {angle}')
#             else:
#                 logger.info('No detections found')

#         command_planner.update()
#         # logger.info('Command planner updated')

#         time.sleep(0.1)  # Control loop interval

#     logger.info('Control thread exited')


# PID Tunning control thread
import time
from commands.TranslateToBallCommand import TranslateToBallCommand
from commands.AlignWithBallCommand import AlignWithBallCommand
from shared_data import shared_data
from logger import logger  # Import the global logger

def control_thread(got, condition):
    logger.info("Control thread started")

    translate_command = TranslateToBallCommand(got)
    align_command = AlignWithBallCommand(got)
    current_command = None

    while True:
        with condition:
            condition.wait()  # Wait for notification from the camera thread

        with shared_data["lock"]:
            if shared_data["exit"]:
                break

        if shared_data["detections"] is not None:
            distance, angle = shared_data["distance"], shared_data["angle"]
            # Update shared_data for chart update
            shared_data["distance_history"].append(distance)
            shared_data["angle_history"].append(angle)
            
            # Maintain only the last 50 records
            if len(shared_data["distance_history"]) > 50:
                shared_data["distance_history"].pop(0)
            if len(shared_data["angle_history"]) > 50:
                shared_data["angle_history"].pop(0)

            # Log detection data
            logger.info(f'Detected distance: {distance}, angle: {angle}')

        if shared_data["command"] == 'translate':
            current_command = translate_command
            logger.info('Starting TranslateToBallCommand')
        elif shared_data["command"] == 'align':
            current_command = align_command
            logger.info('Starting AlignWithBallCommand')
        else:
            current_command = None
            logger.info('No command to execute, robot is idle')
            got.stop_chassis()

        if current_command:
            if current_command == translate_command:
                translate_command.pid_controllers = {
                    "linear": shared_data["linear_pid"],
                    "angle": shared_data["angle_pid"]
                }
            elif current_command == align_command:
                align_command.pid_controllers = {
                    "linear": shared_data["linear_pid"],
                    "angle": shared_data["angle_pid"]
                }
            current_command.execute()

        time.sleep(0.1)  # Control loop interval

    logger.info('Control thread exited')

