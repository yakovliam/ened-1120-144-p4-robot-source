#!/usr/bin/env pybricks-micropython

from robot import GreatRobotV1
from pybricks.tools import wait
from dountil import singleton_do_until as do_until

robot = GreatRobotV1()
robot.scan_barcode()



# # do_until.do_thread_until(
# #     do_callable=lambda: robot.drive_straight(1000),
# #     until_callable=lambda: robot.ultrasonic_sensor.distance() < 50,
# #     callback=robot.stop_driving,
# #     blocking=True
# # )
# robot.close_claw()
# robot.open_claw()
# robot.close_claw()

# while True:
#     print(robot.color_sensor.color())
#     wait(200)


# BARCODE DETECTION PSUDEOCODE
# background: color sensor angle and claw angle are tethered, so when the claw is open, the color sensor is up 100%, and when the claw is closed, the color sensor is down 100%
# Color sensor starts down (claw closed), and it moves up slowly (claw open)
# A "Barcode" is blocks of white and black, so when the color sensor is over a white block, it will see white, and when it is over a black block, it will see black
# A barcode always starts with a black block, and there are 4 blocks total

# 1. Start with the claw closed, and the color sensor down
# 2. Open the claw slowly, and move the color sensor up with it
# 3. When the color sensor sees black, that's the start of the barcode
# 4. Figure out the seconds per each block on the barcode
# 5. Move the claw and color sensor 4 blocks (4 * x seconds per block)
# 6. Close the claw
# 7. Save the data to an array of size 4
