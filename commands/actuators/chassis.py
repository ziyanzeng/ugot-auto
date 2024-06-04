import math
from logger import logger

class Chassis:
    def __init__(self, got):
        self.got = got

    def spin_on_location(self, turn_speed):
        if turn_speed < 0:
            self.got.mecanum_turn_speed(2, int(abs(turn_speed)))
        else:
            self.got.mecanum_turn_speed(3, int(abs(turn_speed)))

    def stop(self):
        # self.got.mecanum_stop()
        self.got.stop_chassis()

    def translate(self, angle, speed):
        self.got.mecanum_translate_speed(int(angle), int(speed))

    def translate_for_time(self, angle, speed, times, unit):
        self.got.mecanum_translate_speed_times(int(angle), int(speed), int(times), int(unit))

    def turn_on_pivot(self, distance, direction, angular_velocity):
        """turn robot on pivot outside of the robot frame

        Args:
            distance (int): unit - cm
            angle (int): unit - degree
            direction (int): either -1 or 1, -1 makes robot turn clockwise, 1 makes robot turn anticlockwise
        """
        logger.info("running turn on pivot function")
        logger.info("distance param: " + str(distance))
        logger.info("direction param: " + str(direction))
        if distance == 0:
            return
        self.got.mecanum_move_turn(int(direction * 90), angular_velocity, 2 if direction == 1 else 3, int(180 * angular_velocity / (math.pi * distance)))
        logger.info("correctly set params for moventurn function")
