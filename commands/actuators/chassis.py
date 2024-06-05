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
        self.got.mecanum_translate_speed(int(angle), int(speed) if speed > 5 else 5)

    def translate_for_time(self, angle, speed, times, unit):
        self.got.mecanum_translate_speed_times(int(angle), int(speed) if speed > 5 else 5, int(times), int(unit))

    def turn_on_pivot(self, distance:float, direction:float, drifting_velocity:float)->None:
        """turn robot on pivot outside of the robot frame

        Args:
            distance (float): unit - cm, distance to the ball (pivot point of turnings)
            direction (float): either -1 or 1, -1 makes robot turn clockwise, 1 makes robot turn anticlockwise
            drifting_velocity (float): pid controller input
        """
        logger.info("running turn on pivot function")
        logger.info("distance param: " + str(distance))
        logger.info("direction param: " + str(direction))
        if distance == 0:
            return
        omega = max(round(180 * drifting_velocity / (math.pi * (distance + 10.5))), 280)
        self.got.mecanum_move_turn(round(direction * 90), round(drifting_velocity) if drifting_velocity > 5 else 5, 2 if direction == 1 else 3, omega if omega > 5 else 5)
        logger.info("correctly set params for moventurn function")
