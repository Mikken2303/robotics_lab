#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B,OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import GyroSensor, TouchSensor, ColorSensor, UltrasonicSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.display import Display

from time import sleep

tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)

gyro = GyroSensor(INPUT_4)
touch = TouchSensor(INPUT_1)
color = ColorSensor(INPUT_3)
sonic = UltrasonicSensor(INPUT_2)
display = Display()


#1
display.draw.text((48,13),"Assignment 1", fill='black')
display.update()


#2
while(touch.is_released):
    sleep(0.05)


#3
display.clear()
display.update()


#4
tank_drive.on(SpeedPercent(25), SpeedPercent(25))

while(sonic.distance_centimeters > 25):
    sleep(0.05)

tank_drive.off()


#5
tank_drive.on(SpeedPercent(25), SpeedPercent(-25))
g = gyro.angle
while(gyro.angle - g < 168):
    sleep(0.05)

tank_drive.off()

#6
tank_drive.on_for_rotations(SpeedPercent(25), SpeedPercent(25), 2)

#7
tank_drive.on(SpeedPercent(5), SpeedPercent(25))
g = gyro.angle
while(gyro.angle - g > -85):
    sleep(0.05)

tank_drive.off()


#8 
tank_drive.on(SpeedPercent(25), SpeedPercent(25))

while(color.reflected_light_intensity > 30):
    sleep(0.05)
tank_drive.off()

#9
sleep(2)

#10
tank_drive.on(SpeedPercent(-25), SpeedPercent(25))
g = gyro.angle
while(gyro.angle - g > -80):
    sleep(0.05)

tank_drive.off()

#11

tank_drive.on(SpeedPercent(-25), SpeedPercent(-25))

while(touch.is_released):
    sleep(0.05)

tank_drive.off()

