#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import GyroSensor, TouchSensor
from ev3dev2.sensor import INPUT_4, INPUT_1


tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
gyro = GyroSensor(INPUT_4)
touch = TouchSensor(INPUT_1)

# drive in a turn for 5 rot



while(True):
    tank_drive.on_for_rotations(SpeedPercent(25), SpeedPercent(25), 1)
    while(gyro.angle < 90):
        tank_drive.on_for_rotations(SpeedPercent(0), SpeedPercent(25), 0.1)
    gyro.angle = 0    






#while(touch.is_pressed):
