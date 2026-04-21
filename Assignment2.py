#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, Motor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import GyroSensor, TouchSensor, ColorSensor, UltrasonicSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.display import Display

from time import sleep



#TODO
class PickupPoint:
    def __init__(self, gyro):
        self.gyro = gyro
        self.found = False
        self.angle_to_pickup = 0

    def find(self):
        self.found = True

    def update(self):
        if(self.found == True):
            self.angle_to_pickup


class Arm:
    def __init__(self,motor_o):
        self.motor = Motor(motor_o)
        self.cube_picked_up = False

    def pickup(self):
        self.motor.on_for_rotations(speed=-10, rotations=0.20)
        self.cube_picked_up = True

    def putDown(self):
        self.motor.on_for_rotations(speed=10, rotations=0.20)
        self.cube_picked_up = False
    


class DeliveryRobot:
    def __init__(self, left_motor_o, right_motor_o, arm_motor_o, gyro_i, color_i, sonic_i):

        # move the robot
        self.tank_drive = MoveTank(left_motor_o, right_motor_o)

        #cube pickup arm
        self.arm = Arm(arm_motor_o)

        # gyroscope sensor 
        self.gyro = GyroSensor(gyro_i)

        # light sensor (down)
        self.color = ColorSensor(color_i)

        #sonar sensor (front)
        self.sonic = UltrasonicSensor(sonic_i)

        self.pickup = PickupPoint(gyro=self.gyro)


    def convert(self, light_intensity):
        return (light_intensity/6)*2 - 5
        

    #one step forward along the line
    def step(self):
        # TODO
        if(self.color.reflected_light_intensity in range(0,39)):
            self.tank_drive.on_for_rotations(left_speed=-5, right_speed=5, rotations=0.01)
        elif(self.color.reflected_light_intensity in range(40,69)):
            self.tank_drive.on_for_rotations(left_speed=5, right_speed=5, rotations=0.05)
        elif(self.color.reflected_light_intensity in range(70,100)):
            self.tank_drive.on_for_rotations(left_speed=5, right_speed=-5, rotations=0.01)
    
    def step_con(self):
         light = self.color.reflected_light_intensity
         self.tank_drive.on_for_rotations(left_speed=self.convert(light), right_speed=self.convert(light)*(-1), rotations=0.01)

    # find and pickup the cube (optionally the delivery point as well)
    def search(self):
        while(True):
            #red pickup
            if(self.color.color == 5):
                self.pickup.find()
                for i in range(0,3):
                    self.step()
            elif(self.sonic.distance_centimeters < 10):
                for i in range(0,3):
                    self.step()
                self.arm.pickup()
                    
                return

            self.step()


    # ignore the line go straight to the delivery point
    def goto_delivery_point(self):
        pass

    def deliver(self):
        if(self.pickup.found == False):
            while(True):
                if(self.color.color == 2):
                    self.arm.putDown()
            self.step()        


        else:
            self.goto_delivery_point()


delivery_robot = DeliveryRobot(left_motor_o=OUTPUT_A, right_motor_o=OUTPUT_B, arm_motor_o=OUTPUT_D, sonic_i=INPUT_1, gyro_i=INPUT_2, color_i=INPUT_4)
delivery_robot.search()
delivery_robot.deliver()

while(True):
    sleep(1)

