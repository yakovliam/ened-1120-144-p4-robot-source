#!/usr/bin/env pybricks-micropython
import random
from robot import GreatRobotV1
from dountil import singleton_do_until as do_until
from pybricks.tools import wait

def rand_between(min, max):
    return random.randint(min, max)

def turn(robot: GreatRobotV1):
    for _ in range(4):
        robot.turn_degrees(rand_between(-90, 90))

def party(robot: GreatRobotV1):
    do_until.do(
        lambda: robot.sound("party")
    )

    wait(3000)

    do_until.do(
        lambda: turn(robot),
        blocking=False
    )

    for _ in range(6):
        robot.open_claw(100, 2000)
        robot.close_claw(100, 2000)

