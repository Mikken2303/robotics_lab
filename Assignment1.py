#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B,OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import GyroSensor, TouchSensor, ColorSensor, UltrasonicSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.display import Display

from time import sleep



# move the robot
tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)

# gyroscope sensor 
gyro = GyroSensor(INPUT_4)

# touch sensor (rear)
touch = TouchSensor(INPUT_1)

# light sensor (down)
color = ColorSensor(INPUT_3)

#sonar sensor (front)
sonic = UltrasonicSensor(INPUT_2)

#display for text
display = Display()


""" @brief drive until the condition is satisfied 
    @param MoveTank drive - motors of the tank
    @param function cond - condition to be satisfied 
    @param int speed - movement speed (-100 to 100) 
"""
def drive_until(drive, cond, speed):
    drive.on(SpeedPercent(speed), SpeedPercent(speed))
    while not cond():
        sleep(0.05)
    drive.off()

""" @brief drive until the condition is satisfied 
    @param MoveTank drive - motors of the tank
    @param int angle - angle of the turn
    @param int speedL - movement speed of the left motor (-100 to 100) 
    @param int speedR - movement speed of the right motor (-100 to 100) 
"""
def turn(drive, angle, speedL, speedR):
    drive.on(SpeedPercent(speedL), SpeedPercent(speedR))
    g = gyro.angle
    while(abs(gyro.angle - g) < angle):
        sleep(0.05)
    drive.off()


#1 Print “Assignment 1” on the screen
display.draw.text((48,13),"Assignment 1", fill='black')
display.update()


#2 Wait for a button to be pressed
while(touch.is_released):
    sleep(0.05)


#3 Clear the screen
display.clear()
display.update()


#4 Move forward until the sonar detects an obstacle at less than 25 cm distance
drive_until(tank_drive, lambda: sonic.distance_centimeters < 25, 25)

#5 Turn 180 degrees using the gyroscope to measure angle
turn(tank_drive, 168, 25, -25)

#6 Move forward 20 units (1 unit corresponds to 0.1 rotations)
unit = 0.1
tank_drive.on_for_rotations(SpeedPercent(25), SpeedPercent(25), 20*unit)

#7 Turn 90 degrees to the left
turn(tank_drive, 85, 5, 25)

#8 Move forward until detecting a dark surface underneath
drive_until(tank_drive, lambda: color.reflected_light_intensity < 30, 25)

#9 Stop
sleep(2)

#10 Rotate 90 degrees to the left
turn(tank_drive, 80, -25, 25)

#11 Move backward until the touch sensor causes the robot to stop.
drive_until(tank_drive, lambda: touch.is_pressed, -25)
