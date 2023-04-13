#!/usr/bin/env pybricks-micropython

from robot import GreatRobotV1
from pybricks.tools import wait
from dountil import singleton_do_until as do_until
import robotutils

inp = ["C1_5", "3", "C"]

absolute_coordinates = robotutils.coordinates.generate_stage1_coordinates(
    inp
)

print(absolute_coordinates)

relative_coordinates = robotutils.coordinates.adjust_coordinates_by_starting_position(absolute_coordinates)

print(relative_coordinates)

mm_coordinates = robotutils.coordinates.coordinate_to_mm(relative_coordinates)

box_number = int(inp[0].split("_")[1])
box_is_on_lower_side = box_number <= 6
home = inp[2]

robot = GreatRobotV1()

robot.open_claw(percent=50)

do_until.do(
    lambda: robot.drive_straight(mm_coordinates[1] + 50),
    blocking=True
)
do_until.do(
    lambda: robot.turn_degrees(90),
    blocking=True
)
do_until.do(
    lambda: robot.drive_straight(mm_coordinates[0] + 200),
    blocking=True
)

do_until.do(
    lambda: robot.turn_degrees(-90),
    blocking=True
)

do_until.do(
    lambda: robot.drive_straight(12 * 25.4),
    blocking=True
)

robot.close_claw()
robot.scan_barcode(target="2")

do_until.do(
    lambda: robot.drive_straight(-1 * 6 * 25.4),
    blocking=True
)

do_until.do(
    lambda: robot.turn_degrees(-90),
    blocking=True
)

robot.close_claw()

home_coords = None

if home == "B":
    home = robotutils.coordinates.home_b_coordinates()
elif home == "C":
    home = robotutils.coordinates.home_c_coordinates()
elif home == "D":
    home = robotutils.coordinates.home_d_coordinates()
else:
    home = robotutils.coordinates.home_a_coordinates()

home_coords = robotutils.coordinates.adjust_coordinates_by_starting_position(home)
home_mm = robotutils.coordinates.coordinate_to_mm(home_coords)

# drive to the home
do_until.do(
    lambda: robot.drive_straight(abs(abs(home_mm[1]) - abs(mm_coordinates[1])) - 12),
    blocking=True
)

from party import party
party(robot)

wait(10000)
