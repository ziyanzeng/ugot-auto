import time
from commands.CommandPlanner import CommandPlanner
from commands.LocateBallCommand import LocateBallCommand
from commands.LocateGoalCommand import LocateGoalCommand
from commands.TranslateToBallCommand import TranslateToBallCommand
from commands.AlignWithBallCommand import AlignWithBallCommand
from commands.RestCommand import RestCommand
from commands.KickCommand import KickCommand
from shared_data import SharedData
from logger import logger  # Import the global logger

# PID Tunning control thread
def control_thread(got, condition):
    logger.info("Control thread started")

    current_command = RestCommand(got)
    command_planner = CommandPlanner(got)

    while True:
        with condition:
            condition.wait()  # Wait for notification from the camera thread

        with SharedData.shared_data["lock"]:
            if SharedData.shared_data["exit"]:
                break

        if SharedData.shared_data["detections"] is not None:
            # Update shared_data for chart update
            SharedData.shared_data["distance_history"].append(SharedData.shared_data["distance"])
            # SharedData.shared_data["angle_history"].append(SharedData.shared_data["angle"])
            SharedData.shared_data["angle_history"].append(SharedData.shared_data["angle_goal"])

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
            
        update_signal = current_command.isFinished() and SharedData.shared_data["command"] != "disable"
        command_planner.update(update_signal)
        
        if SharedData.shared_data["command"] == "disable":
            continue

        # logger.info(SharedData.shared_data["command"])
        if current_command.isFinished():
            command_name = SharedData.shared_data["command"]
            logger.info(f"next command updating: {command_name}")
            if SharedData.shared_data["command"] == "locate":
                # if not isinstance(current_command, LocateBallCommand) or got.read_gyro_data()[5] < 1:
                    current_command = LocateBallCommand(got)
                    current_command.initialize()
            elif SharedData.shared_data["command"] == "translate":
                # if not isinstance(current_command, TranslateToBallCommand):
                    current_command = TranslateToBallCommand(got)
                    current_command.initialize()
            elif SharedData.shared_data["command"] == "align":
                # if not isinstance(current_command, AlignWithBallCommand):
                    current_command = AlignWithBallCommand(got)
                    current_command.initialize()
            elif SharedData.shared_data["command"] == "goal":
                # if not isinstance(current_command, LocateGoalCommand):
                    current_command = LocateGoalCommand(got)
                    current_command.initialize()
            elif SharedData.shared_data["command"] == "kick":
                current_command = KickCommand(got)
                current_command.initialize()
                SharedData.shared_data["command"] = "rest"
            else:
                current_command = RestCommand(got)
                SharedData.shared_data["command"] = "rest"
                
        else:
            current_command.execute()
            

        time.sleep(0.1)  # Control loop interval

    logger.info('Control thread exited')

