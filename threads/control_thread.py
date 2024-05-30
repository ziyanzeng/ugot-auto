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
from commands.RestCommand import RestCommand
from shared_data import SharedData
from logger import logger  # Import the global logger

def control_thread(got, condition):
    logger.info("Control thread started")

    current_command = RestCommand(got)

    while True:
        with condition:
            condition.wait()  # Wait for notification from the camera thread

        with SharedData.shared_data["lock"]:
            if SharedData.shared_data["exit"]:
                break

        if SharedData.shared_data["detections"] is not None:
            # Update shared_data for chart update
            SharedData.shared_data["distance_history"].append(SharedData.shared_data["distance"])
            SharedData.shared_data["angle_history"].append(SharedData.shared_data["angle"])

            # Log detection data
            # logger.info(f'Detected distance: {SharedData.shared_data["distance"]}, angle: {SharedData.shared_data["angle"]}')
        else:
            SharedData.shared_data["distance_history"].append(0)
            SharedData.shared_data["angle_history"].append(0)
        
        # Maintain only the last 50 records
        if len(SharedData.shared_data["distance_history"]) > 50:
            SharedData.shared_data["distance_history"].pop(0)
        if len(SharedData.shared_data["angle_history"]) > 50:
            SharedData.shared_data["angle_history"].pop(0)

        if current_command.isFinished():
            if SharedData.shared_data["command"] == "translate":
                if not isinstance(current_command, TranslateToBallCommand):
                    current_command = TranslateToBallCommand(got, {"linear": SharedData.shared_data["linear_pid"], "angle": SharedData.shared_data["angle_pid"]})
                    current_command.initialize()
            elif SharedData.shared_data["command"] == "align":
                if not isinstance(current_command, AlignWithBallCommand):
                    current_command = AlignWithBallCommand(got, {"linear": SharedData.shared_data["linear_pid"], "angle": SharedData.shared_data["angle_pid"]})
                    current_command.initialize()
        else:
            current_command.execute()
            

        time.sleep(0.1)  # Control loop interval

    logger.info('Control thread exited')

