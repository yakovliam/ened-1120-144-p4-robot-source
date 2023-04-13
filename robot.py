from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from threadactionmanager import ThreadActionManager
from _thread import start_new_thread
from dountil import singleton_do_until as do_until
from statetoken import StateToken
import robotutils

# constants
MAX_SPEED_MM_PER_SEC = 150
MAX_ROTATION_SPEED_DEG_PER_SEC = 60
WHEEL_DIAMETER = 70  #45
AXEL_TRACK = 190 #119.38
CLAW_FULL_CLOSE_DEGREES = 2000
CLAW_FULL_OPEN_DEGREES = -2000
CLAW_DEFAULT_SPEED = 2000

class GreatRobotV1:
    left_motor = None
    right_motor = None
    claw_motor = None
    robot = None
    gyro = None
    ev3 = None
    screen = None

    claw_current_percent_open = 0 # start with the claw closed

    def __init__(self):
        self.ev3 = EV3Brick()

        self.screen = self.ev3.screen

        self.left_motor = Motor(Port.A, positive_direction=Direction.CLOCKWISE)
        self.right_motor = Motor(Port.B, positive_direction=Direction.CLOCKWISE)
        self.claw_motor = Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE)

        self.robot = DriveBase(self.left_motor, self.right_motor, wheel_diameter=WHEEL_DIAMETER, axle_track=AXEL_TRACK)
        self.robot.settings(
            straight_speed=MAX_SPEED_MM_PER_SEC,
            straight_acceleration=MAX_SPEED_MM_PER_SEC,
            turn_rate=MAX_ROTATION_SPEED_DEG_PER_SEC,
        )

        self.gyro = GyroSensor(Port.S4)
        self.gyro.reset_angle(0)

        self.ultrasonic_sensor = UltrasonicSensor(Port.S3)
        self.color_sensor = ColorSensor(Port.S1)

        self.ev3.speaker.set_volume(100)

    def draw_text(self, text):
        self.screen.draw_text(0, 0, text)
    
    # Drives the robot by some distance
    # distance = mm
    def drive_straight(self, distance):
        # # dc = -100-100
        # speed = 50

        # left_speed = speed + 9
        # right_speed = speed

        # self.left_motor.dc(left_speed)
        # self.right_motor.dc(right_speed)

        # wait(5 * distance)
        # self.left_motor.dc(0)
        # self.right_motor.dc(0)

        self.robot.straight(distance)

    


    # Stops the robot
    def stop_driving(self):
        self.robot.stop()
    
    def _reset_gyro_and_stop(self):
        self.gyro.reset_angle(0)
        self.stop_driving()

    # Turns the robot by some angle
    # angle = degrees
    def turn_degrees(self, angle):
        self.gyro.reset_angle(0)

        # break up into 90 degree turns so it doesn't overshoot
        times_to_turn = int(abs(angle) / 90)
        angle_each_turn = 90
        last_turn_angle = abs(angle) % 90

        sign = 1 if angle > 0 else -1

        for i in range(times_to_turn + 1):
            rotate_by = last_turn_angle if i == times_to_turn - 1 else angle_each_turn
            rotate_by -= 6
            do_until.do_until(
                do_callable=lambda: self.robot.turn(1000 * sign),
                until_callable=lambda: abs(self.gyro.angle()) >= rotate_by,
                callback=lambda: self._reset_gyro_and_stop()
            )

        # self.gyro.reset_angle(0)
        # sign = 1 if angle > 0 else -1
        # self.robot.turn(angle + (sign * 36))

    # Scans a vertical barcode
    # Make sure that the claws are clear of any obstacles
    # to the left or right of the box it is currently in posession of
    def scan_barcode(self, target):
        # close the claw
        self.close_claw(60)

        state_token = StateToken()
        scanned_colors = []

        do_until.do(
                do_callable=lambda: self.open_claw(percent=55, speed=750),
                blocking=False,
                callback=lambda: state_token.flag()
        )

        def scan_print_append():
            color = self.color_sensor.color()
            print(color)
            scanned_colors.append(color)

        wait(250)

        do_until.do_until(
            do_callable=lambda: scan_print_append(),
            until_callable=lambda: state_token.is_flagged(),
            blocking=True,
            callback=lambda: print("callback called"),
            do_callable_delay_ms=200
        )
        
        do_until.do(
            do_callable=lambda: self.close_claw(),
            blocking=True,
        )

        scanned_barcode_ident = robotutils.barcode_utils.convert_scanned_colors_to_barcode(
            scanned_colors
        )

        if scanned_barcode_ident == 1:
            self.sound("b1d")
            self.screen.draw_text(0, 0, "Barcode 1")

        elif scanned_barcode_ident == 2:
            self.sound("b2d")
            self.screen.draw_text(0, 0, "Barcode 2: MATCH")

        elif scanned_barcode_ident == 3:
            self.sound("b3d")
            self.screen.draw_text(0, 0, "Barcode 3")

        elif scanned_barcode_ident == 4:
            self.sound("b4d")
            self.screen.draw_text(0, 0, "Barcode 4")

        # if scanned_barcode_ident == target:
        #     self.screen.draw_text(0, 2, "Match!")


        wait(10000)


    # Opens the claw
    def open_claw(self, percent=100, speed=CLAW_DEFAULT_SPEED):
        # target degrees based on percent
        target_degrees = CLAW_FULL_OPEN_DEGREES * (percent / 100)
        # target degrees based on the calculated target degrees and the current percent open
        target_degrees = target_degrees * ((100 - self.claw_current_percent_open) / 100)
        self.claw_motor.run_angle(speed, target_degrees, wait=False)
        # update the current percent open
        self.claw_current_percent_open = percent

    # Closes the claw
    def close_claw(self, percent=100, speed=CLAW_DEFAULT_SPEED):
        # target degrees based on percent
        target_degrees = CLAW_FULL_CLOSE_DEGREES * (percent / 100)
        # target degrees based on the calculated target degrees and the current percent open
        target_degrees = target_degrees * (self.claw_current_percent_open / 100)
        self.claw_motor.run_angle(speed, target_degrees, wait=False)
        # update the current percent open
        self.claw_current_percent_open = 100 - percent

    def reset_claw(self):
        self.close_claw(100)

    def play_sound_effect(self, sound_effect):
        self.ev3.speaker.play_file(sound_effect)

    def sound(self, name):
        file_name = "sounds/" + name + ".wav"
        self.ev3.speaker.play_file(file_name)

    # Distance = mm
    def __detect_object(self, distance):
        while True:
            if self.ultrasonic_sensor.distance() < distance:
                return True
            
    def on_object_detected(self, distance, action):
        tam = ThreadActionManager(
            lambda: (),
            lambda: self.__detect_object(distance),
            action,
            should_restart_after_end=False
        )

        start_new_thread(tam.start, ())

