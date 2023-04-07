from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from threadactionmanager import ThreadActionManager
from _thread import start_new_thread

# constants
MAX_SPEED_MM_PER_SEC = 150
MAX_ROTATION_SPEED_DEG_PER_SEC = 90
WHEEL_DIAMETER = 45
AXEL_TRACK = 119.38
CLAW_FULL_CLOSE_DEGREES = 2000
CLAW_FULL_OPEN_DEGREES = -2000

class GreatRobotV1:
    left_motor = None
    right_motor = None
    claw_motor = None
    robot = None
    gyro = None
    ev3 = None

    claw_current_percent_open = 100 # start with the claw open

    def __init__(self):
        self.ev3 = EV3Brick()

        self.left_motor = Motor(Port.A, positive_direction=Direction.CLOCKWISE)
        self.right_motor = Motor(Port.B, positive_direction=Direction.CLOCKWISE)
        self.claw_motor = Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE)

        self.robot = DriveBase(self.left_motor, self.right_motor, wheel_diameter=WHEEL_DIAMETER, axle_track=AXEL_TRACK)
        self.robot.settings(
            straight_speed=MAX_SPEED_MM_PER_SEC,
            straight_acceleration=MAX_SPEED_MM_PER_SEC,
            turn_rate=MAX_ROTATION_SPEED_DEG_PER_SEC,
        )

        self.gyro = GyroSensor(Port.S2)
        self.gyro.reset_angle(0)

        self.ultrasonic_sensor = UltrasonicSensor(Port.S3)
        # self.color_sensor = ColorSensor(Port.S1)
    
    # Drives the robot by some distance
    # distance = mm
    def drive_some_distance(self, distance):
        self.robot.straight(distance)

    # Turns the robot by some angle
    # angle = degrees
    def turn_some_angle(self, angle):
        self.gyro.reset_angle(0)
        current_angle = self.gyro.angle()
        while abs(current_angle) < angle - 2:
            self.robot.turn(10)
            current_angle = self.gyro.angle()

    # Opens the claw
    def open_claw(self, percent=100):
        # target degrees based on percent
        target_degrees = CLAW_FULL_OPEN_DEGREES * (percent / 100)
        # target degrees based on the calculated target degrees and the current percent open
        target_degrees = target_degrees * ((100 - self.claw_current_percent_open) / 100)
        self.claw_motor.run_angle(2000, target_degrees)
        # update the current percent open
        self.claw_current_percent_open = percent

    # Closes the claw
    def close_claw(self, percent=100):
        # target degrees based on percent
        target_degrees = CLAW_FULL_CLOSE_DEGREES * (percent / 100)
        # target degrees based on the calculated target degrees and the current percent open
        target_degrees = target_degrees * (self.claw_current_percent_open / 100)
        self.claw_motor.run_angle(2000, target_degrees)
        # update the current percent open
        self.claw_current_percent_open = 100 - percent

    def reset_claw(self):
        pass

    def play_sound_effect(self, sound_effect):
        self.ev3.speaker.play_file(sound_effect)

    def sound(self, name):
        file_name = "sounds/" + name + ".wav"
        self.ev3.speaker.set_volume(1000)
        self.ev3.speaker.play_file(file_name)

    # Distance = mm
    def __detect_object(self, distance):
        while True:
            if self.ultrasonic_sensor.distance() < distance:
                return True
            
    def __create_object_detection_tam(self, action):
        return ThreadActionManager(
            action,
            self.__detect_object,
            should_restart_after_end=True
        )
    
    def on_object_detected(self, distance, action):
        tam = self.__create_object_detection_tam(action)
        tam.start(distance)


