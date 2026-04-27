#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, Motor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import GyroSensor, TouchSensor, ColorSensor, UltrasonicSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.display import Display

from time import sleep


class Arm:
    """Controls the arm used to pick up and put down the cube"""

    def __init__(self, motor_o):
        self.motor = Motor(motor_o)
        self.cube_picked_up = False

    def pickup(self):
        """Lower the arm to and pick up a cube."""
        self.motor.on_for_rotations(speed=-10, rotations=0.12)
        self.cube_picked_up = True

    def putDown(self):
        """Raise the arm to put down a cube."""
        self.motor.on_for_rotations(speed=10, rotations=0.12)
        self.cube_picked_up = False


class DeliveryRobot:
    """
    A line-following delivery robot that searches for a cube,
    picks it up, and delivers it to a colour-coded drop-off point.
    """

    # Colour sensor constants 
    COLOR_YELLOW = 4  # Used to detect home/base
    COLOR_RED = 5     # Used to detect  delivery point

    # Line following light intensity thresholds
    LIGHT_TURN_RIGHT = range(0, 20)   # Dark - robot is too far right, steer left
    LIGHT_STRAIGHT = range(20, 30)    # On the line edge - go straight
    LIGHT_TURN_LEFT = range(30, 101)  # Light - robot is too far left, steer right

    # Ultrasonic distance threshold (cm) to detect a cube in front of the arm
    CUBE_DETECT_DISTANCE_CM = 11

    def __init__(self, left_motor_o, right_motor_o, arm_motor_o, gyro_i, color_i, sonic_i):
        # Drive controller for movement
        self.tank_drive = MoveTank(left_motor_o, right_motor_o)

        # Arm mechanism for picking up and dropping the cube
        self.arm = Arm(arm_motor_o)

        # Gyroscope for measuring angle during turns
        self.gyro = GyroSensor(gyro_i)

        # Downward-facing colour sensor for line following and zone detection
        self.color = ColorSensor(color_i)

        # Downward-facing ultrasonic sensor for detecting the cube
        self.sonic = UltrasonicSensor(sonic_i)

        # Flag set when the red pickup zone is spotted during search
        self.pickup_found = False

    def step(self):
        """
        Advance one small increment along the line using bang-bang line following.
        """
        light = self.color.reflected_light_intensity
        if light in self.LIGHT_TURN_RIGHT:
            self.tank_drive.on_for_rotations(left_speed=5, right_speed=-5, rotations=0.01)
        elif light in self.LIGHT_STRAIGHT:
            self.tank_drive.on_for_rotations(left_speed=5, right_speed=5, rotations=0.03)
        elif light in self.LIGHT_TURN_LEFT:
            self.tank_drive.on_for_rotations(left_speed=-5, right_speed=5, rotations=0.01)

    def turn(self, angle):
        """
        Rotate the robot in place by the given angle (degrees) using the gyroscope.
        """
        start_angle = self.gyro.angle
        self.tank_drive.on(SpeedPercent(-25), SpeedPercent(25))
        while abs(self.gyro.angle - start_angle) < angle:
            sleep(0.05)
        self.tank_drive.off()

    def search(self):
        """
        Follow the line searching for the cube.
        - If a red zone is detected record that the pickup point was found.
        - If an object is within CUBE_DETECT_DISTANCE_CM, pick up the cube and return.
        """
        while True:
            if self.color.color == self.COLOR_RED:
                self.pickup_found = True
            elif self.sonic.distance_centimeters < self.CUBE_DETECT_DISTANCE_CM:
                self.arm.pickup()
                return
            self.step()

    def go_home(self):
        """
        Follow the line until the yellow home zone is detected, then turn 180° to face forward.
        """
        while self.color.color != self.COLOR_YELLOW:
            self.step()
        self.turn(180)
        self.pickup_found = False

    def goto_delivery_point(self):
        """
        Deliver the cube to the red delivery point using a fixed manoeuvre:
        1. Turn off the line toward the delivery area.
        2. Drive forward until the red zone is found.
        3. Drop the cube, reverse, realign, and return home.
        """
        self.turn(100)
        # Short drive to clear the main line before searching for the delivery zone
        self.tank_drive.on_for_rotations(left_speed=-25, right_speed=-25, rotations=0.2)
        while self.color.color != self.COLOR_RED:
            self.step()
        self.arm.putDown()
        # Reverse away from the drop point, then arc back toward the line going around the cube
        self.tank_drive.on_for_rotations(left_speed=-25, right_speed=-25, rotations=0.5)
        self.tank_drive.on_for_rotations(left_speed=25, right_speed=5, rotations=1)
        self.tank_drive.on_for_rotations(left_speed=25, right_speed=25, rotations=1)
        self.go_home()

    def deliver(self):
        """
        Deliver the cube based on whether the red pickup point was spotted during search.
        - pickup_found=False: deliver inline on the line, then turn and go home.
        - pickup_found=True:  use the goto_delivery_point off-line manoeuvre.
        """
        if not self.pickup_found:
            # Follow the line to the first red zone encountered and drop the cube there
            while self.color.color != self.COLOR_RED:
                self.step()
            self.arm.putDown()
            # Back up slightly, turn, and navigate home
            self.tank_drive.on_for_rotations(left_speed=-25, right_speed=-25, rotations=0.5)
            self.turn(90)
            self.go_home()
        else:
            self.goto_delivery_point()


# --- Entry point ---
delivery_robot = DeliveryRobot(
    left_motor_o=OUTPUT_A,
    right_motor_o=OUTPUT_B,
    arm_motor_o=OUTPUT_D,
    sonic_i=INPUT_1,
    gyro_i=INPUT_2,
    color_i=INPUT_4
)

while True:
    delivery_robot.search()
    delivery_robot.deliver()