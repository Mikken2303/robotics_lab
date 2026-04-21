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


class Arm:
    def __init__(self,motor_o):
        self.motor = Motor(motor_o)
        self.cube_picked_up = False

    def pickup(self):
        self.motor.on_for_rotations(speed=-10, rotations=0.12)
        self.cube_picked_up = True

    def putDown(self):
        self.motor.on_for_rotations(speed=10, rotations=0.12)
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
        if(self.color.reflected_light_intensity in range(0,19)):
            self.tank_drive.on_for_rotations(left_speed=5, right_speed=-5, rotations=0.01)
        elif(self.color.reflected_light_intensity in range(20,29)):
            self.tank_drive.on_for_rotations(left_speed=5, right_speed=5, rotations=0.03)
        elif(self.color.reflected_light_intensity in range(30,100)):
            self.tank_drive.on_for_rotations(left_speed=-5, right_speed=5, rotations=0.01)
    
    def turn(self,angle):
        g = self.gyro.angle
        self.tank_drive.on(SpeedPercent(-25), SpeedPercent(25))
        while(abs(self.gyro.angle - g) < angle):
            sleep(0.05)
        self.tank_drive.off()



    # find and pickup the cube (optionally the delivery point as well)
    def search(self):
        while(True):
            #red pickup
            if(self.color.color == 5):
                self.pickup.find()
            elif(self.sonic.distance_centimeters < 11):
                self.arm.pickup()
                return

            self.step()


    def go_home(self):
        while(self.color.color != 4):
            self.step()
        self.turn(180)

    # ignore the line go straight to the delivery point
    def goto_delivery_point(self):
        self.turn(100)
        self.tank_drive.on_for_rotations(left_speed=-25, right_speed=-25, rotations=0.2)
        while(self.color.color != 5):
            self.step()
        self.arm.putDown()
        self.tank_drive.on_for_rotations(left_speed=-25, right_speed=-25, rotations=0.5)
        self.tank_drive.on_for_rotations(left_speed=25, right_speed=5, rotations=1)
        self.tank_drive.on_for_rotations(left_speed=25, right_speed=25, rotations=1)
        self.go_home()


    def deliver(self):
        if(self.pickup.found == False):
            while(self.color.color != 5):
                self.step() 
            self.arm.putDown()
            self.tank_drive.on_for_rotations(left_speed=-25, right_speed=-25, rotations=0.5)
            self.turn(90)
            self.go_home()
            return
                       


        else:
            self.goto_delivery_point()


delivery_robot = DeliveryRobot(left_motor_o=OUTPUT_A, right_motor_o=OUTPUT_B, arm_motor_o=OUTPUT_D, sonic_i=INPUT_1, gyro_i=INPUT_2, color_i=INPUT_4)
delivery_robot.search()
delivery_robot.deliver()

while(True):
    sleep(1)

