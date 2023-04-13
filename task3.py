#!/usr/bin/env pybricks-micropython

from robot import GreatRobotV1
from pybricks.tools import wait
from dountil import singleton_do_until as do_until
import robotutils

inp = ["A1_8", "3", "B"]

absolute_coordinates = robotutils.coordinates.generate_stage1_coordinates(
    inp
)

print(absolute_coordinates)

relative_coordinates = robotutils.coordinates.adjust_coordinates_by_starting_position(absolute_coordinates)

print(relative_coordinates)

mm_coordinates = robotutils.coordinates.coordinate_to_mm(relative_coordinates)

box_number = int(inp[0].split("_")[1])
box_is_on_lower_side = box_number <= 6

robot = GreatRobotV1()

robot.open_claw(percent=50)

#######
# do_until.do(
#     lambda: robot.drive_straight(mm_coordinates[1] + 50),
#     blocking=True
# )
# do_until.do(
#     lambda: robot.turn_degrees(90),
#     blocking=True
# )
##########

do_until.do(
    lambda: robot.drive_straight(mm_coordinates[0] + 200),
    blocking=True
)

do_until.do(
    lambda: robot.turn_degrees(90),
    blocking=True
)

do_until.do(
    lambda: robot.drive_straight(6 * 25.4),
    blocking=True
)


robot.close_claw()
robot.scan_barcode(target="3")

robot.close_claw(percent=100)

# UNCOMMENT FOR TASK 4 ONLY (AND DELETE ALL THE ABOVE EXCEPT ROBOT DEFINITION)

# robot.open_claw()
# do_until.do(
#     lambda: robot.drive_straight(1 * 6 * 25.4),
#     blocking=True
# )
# wait(500)
# robot.close_claw()

##############################

do_until.do(
    lambda: robot.drive_straight(-1 * 3 * 25.4),
    blocking=True
)

robot.close_claw()

do_until.do(
    lambda: robot.turn_degrees(-90),
    blocking=True
)

robot.close_claw()

home_b_abs = robotutils.coordinates.home_b_coordinates()
home_b_rel = robotutils.coordinates.adjust_coordinates_by_starting_position(home_b_abs)
home_b_mm = robotutils.coordinates.coordinate_to_mm(home_b_rel)
home_b = (home_b_mm[0] - mm_coordinates[0], home_b_mm[1] - mm_coordinates[1])

do_until.do(
    lambda: robot.drive_straight(abs(home_b[0]) - 100),
    blocking=True
)

# do_until.do(
#     lambda: robot.turn_degrees(90),
#     blocking=True
# )

# do_until.do(
#     lambda: robot.drive_straight(abs(home_b[1]) + 150),
#     blocking=True
# )

robot.open_claw(percent=100)