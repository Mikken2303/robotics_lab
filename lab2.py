#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import GyroSensor, TouchSensor
from ev3dev2.sensor import INPUT_4, INPUT_1

from time import sleep


tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
gyro = GyroSensor(INPUT_4)
touch = TouchSensor(INPUT_1)

tank_drive.on(SpeedPercent(25), SpeedPercent(10))

while(True):
    if(touch.is_pressed):
        tank_drive.off()

        tank_drive.on_for_seconds(SpeedPercent(-25), SpeedPercent(-25), 1)

        tank_drive.on(SpeedPercent(25), SpeedPercent(-25))
        g = gyro.angle
        while(gyro.angle - g < 180):
            sleep(0.01)

        tank_drive.off()
        tank_drive.on(SpeedPercent(25), SpeedPercent(10))

    sleep(0.01)    






#while(touch.is_pressed):
