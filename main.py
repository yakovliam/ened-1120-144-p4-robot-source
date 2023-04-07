#!/usr/bin/env pybricks-micropython

from robot import GreatRobotV1
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.tools import wait
from threadactionmanager import ThreadActionManager

robot = GreatRobotV1()

robot.sound("starting")


# Self explanatory
robot.drive_some_distance(800)
robot.sound("b2d")
robot.close_claw(percent=100)
robot.drive_some_distance(-800)
robot.open_claw(percent=100)

# Self explanatory (object avoidance)
robot.on_object_detected(100, lambda: robot.drive_some_distance(0))


