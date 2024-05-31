import time
from commands.actuators.arm import Arm
from logger import logger

def arm_thread(got, control_signal):
    arm = Arm(got)
    while True:
        with control_signal:
            control_signal.wait()
            
        logger.info("kick signal received. Starting routine...")
        arm.kick_motion()
        logger.info("kick routine ended, waiting for next signal...")