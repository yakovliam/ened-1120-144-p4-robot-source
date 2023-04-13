#!/usr/bin/env pybricks-micropython

from robot import GreatRobotV1
from pybricks.tools import wait
from dountil import singleton_do_until as do_until
import robotutils

robot = GreatRobotV1()

do_until.do(
    lambda: robot.drive_straight(-1 * 12 * 25.4),
    blocking=True
)
do_until.do(
    lambda: robot.turn_degrees(90),
    blocking=True
)
do_until.do(
    lambda: robot.drive_straight(8.5 * 12 * 25.4),
    blocking=True
)
do_until.do(
    lambda: robot.turn_degrees(-90),
    blocking=True
)
do_until.do(
    lambda: robot.drive_straight(1.3 * 12 * 25.4),
    blocking=True
)