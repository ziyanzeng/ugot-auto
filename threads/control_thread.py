import time
from commands.CommandPlanner import CommandPlanner
from commands.TranslateToBallCommand import TranslateToBallCommand
from commands.AlignWithBallCommand import AlignWithBallCommand
from commands.RestCommand import RestCommand
from shared_data import SharedData
from logger import logger  # Import the global logger

# Full automatic control thread
def control_thread(got, condition, control_signal):
    logger.info("Control thread started")

    command_planner = CommandPlanner(got)

    while True:
        with condition:
            condition.wait()  # Wait for notification from the camera thread
            
        with SharedData.shared_data["lock"]:
            if SharedData.shared_data["exit"]:
                break

        command_name = command_planner.update()
        
        if (command_name == "kick_command"):
            with control_signal:
                control_signal.notify_all()
        # logger.info('Command planner updated')

        time.sleep(0.1)  # Control loop interval

    logger.info('Control thread exited')


# PID Tunning control thread
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
                    current_command = TranslateToBallCommand(got)
                    current_command.initialize()
            elif SharedData.shared_data["command"] == "align":
                if not isinstance(current_command, AlignWithBallCommand):
                    current_command = AlignWithBallCommand(got)
                    current_command.initialize()
        else:
            current_command.execute()
            

        time.sleep(0.1)  # Control loop interval

    logger.info('Control thread exited')

