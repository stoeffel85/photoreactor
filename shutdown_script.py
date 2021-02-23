# Copyright 2020 by Chirstoph Winkler, University of Graz, Austria.
# This file is part of the "Open Source Photoreactor for Parallel Evaluation 
# of Small-Scale Reactions" by Christoph Winkler and is licensed under a 
# Creative Commons Attribution-ShareAlike 4.0 International (BY-SA) License.
# http://creativecommons.org/licenses/by-sa/4.0/
# https://github.com/stoeffel85/photoreactor
# Permissions beyond the scope of this license may be available at http://biocatalysis.uni-graz.at.
# This script uses Pigpio: http://abyz.me.uk/rpi/pigpio/python.html

# coding=utf-8
import os    #import os module
os.system('sudo pigpiod') #switch on pigpiod in the shell
import pigpio #import pigpio
from signal import pause

#this function starts the PWM for the LEDs and can only be called after the pigpio has been initialized with pi = pigpio.pi()
def start_hardware_timed_software_pwm(pi, pin, frequency, range, duty_cycle):
    pi.set_mode(pin, pigpio.OUTPUT) #switch pin to output
    pi.set_PWM_frequency(pin, frequency)  #e.g. set_PWM_frequency(4, 1100) sets the frequency of pin 4 to the closest choosable frequency of t (check pigpio table)
    pi.set_PWM_range(pin, range) #sets the range of the gpio to the second number, e.g. 100 to work in %,
    pi.set_PWM_dutycycle(pin, duty_cycle) #sets the dutycycle of a pin according to pwmrange (if 100, then in %), also starts the pwm

#this stops the PWM for the LEDs
def stop_hardware_timed_software_pwm(pi, pin):
    pi.set_PWM_dutycycle(pin, 0) #sets the dutycycle of a pin according to pwmrange (if 100, then in %), also stops the pwm
    return("OFF")

def callbackfunction(gpio, level, tick):
    global globaltick
    global all_pins
    if level == 0: #when butten is pressed
        globaltick = tick #time stamp when pressed
    elif level == 1: #when butten is released
        diff = pigpio.tickDiff(globaltick, tick) #difference bewteen time stamp pressed and released
        if diff < 3000000: #nothing happens if its shorter than 3 sec
            print("too short")
        if diff >= 3000000: #shutdown if its longer than 3 sec
            print("stopping")
            #stop LEDs
            for i in range(12):
                stop_hardware_timed_software_pwm(pi, all_pins[i])
            print("LEDs stopped")
            #stop fans
            pi.hardware_PWM(18, 0, 0)
            pi.set_mode(18, pigpio.INPUT)
            print("Fans stopped")
            pi.stop() #stop connection
            #stop the pigpiod
            os.system('sudo killall pigpiod')
            print("pigpiod stopped")
            os.system('sudo shutdown -h now')

pi = pigpio.pi()  #connect pigpio to the gpio of the pi
globaltick = pi.get_current_tick() #time stamp at boot

#numbers of the used GPIO pins used for the LED channels
pin_channel1 = 24
pin_channel2 = 10
pin_channel3 = 9
pin_channel4 = 25
pin_channel5 = 11
pin_channel6 = 8
pin_channel7 = 7
pin_channel8 = 5
pin_channel9 = 17
pin_channel10 = 27
pin_channel11 = 22
pin_channel12 = 23
all_pins = [pin_channel1, pin_channel2, pin_channel3, pin_channel4, pin_channel5, pin_channel6, pin_channel7, pin_channel8, pin_channel9, pin_channel10, pin_channel11, pin_channel12]

#start all pins with a duty cycle of "0"
for i in range(12):
    start_hardware_timed_software_pwm(pi, all_pins[i], 100, 100, 0)

pi.set_mode(3, pigpio.INPUT) #switch pin to input
pi.set_pull_up_down(3, pigpio.PUD_UP) #pull up
pi.callback(3, pigpio.EITHER_EDGE, callbackfunction) #callback fuction waiting for a change at pin 3

pause()  