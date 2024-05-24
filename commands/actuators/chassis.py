class Chassis:
    def __init__(self, got):
        self.got = got

    def spin_on_location(self, turn_speed):
        if turn_speed < 0:
            self.got.mecanum_turn_speed(2, abs(turn_speed))
        else:
            self.got.mecanum_turn_speed(3, abs(turn_speed))

    def stop(self):
        self.got.mecanum_stop()

    def translate(self, angle, speed):
        self.got.mecanum_translate_speed(angle, speed)

    def translate_for_time(self, angle, speed, times, unit):
        self.got.mecanum_translate_speed_times(angle, speed, times, unit)
