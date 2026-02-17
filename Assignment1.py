#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B,OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import GyroSensor, TouchSensor,LightSensor,UltrasonicSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.display import Display

from time import sleep


tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

gyro = GyroSensor(INPUT_4)
touch = TouchSensor(INPUT_1)
light = LightSensor(INPUT_3)
sonic = UltrasonicSensor(INPUT_2)
display = Display()



#1
display.text_pixels("Assignment 1", x=64, y=64)


#2
while(touch.is_pressed):
    sleep(0.05)


#3
display.clear()


#4
tank_drive.on(SpeedPercent(25), SpeedPercent(25))

while(sonic.distance_centimeters() > 25):
    sleep(0.05)

tank_drive.off()


#5
tank_drive.on(SpeedPercent(25), SpeedPercent(-25))
g = gyro.angle
while(gyro.angle - g < 180):
    sleep(0.05)

tank_drive.off()

#6
tank_drive.on_for_rotations(SpeedPercent(25), SpeedPercent(25), 2)

#7
tank_drive.on(SpeedPercent(25), SpeedPercent(5))
g = gyro.angle
while(gyro.angle - g < 90):
    sleep(0.05)

tank_drive.off()


#8 
tank_drive.on(SpeedPercent(25), SpeedPercent(25))

while(light.reflected_light_intensity > 30):
    sleep(0.05)

#9
tank_drive.off()

#10
tank_drive.on(SpeedPercent(25), SpeedPercent(-25))
g = gyro.angle
while(gyro.angle - g < 90):
    sleep(0.05)

tank_drive.off()

#11

tank_drive.on(SpeedPercent(25), SpeedPercent(25))

while(touch.is_released):
    sleep(0.05)

tank_drive.off()

