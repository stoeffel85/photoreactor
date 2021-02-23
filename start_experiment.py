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
import reactor_programm as runexp #the second file of this script
import time

#adjust these once for the correct path to the temperature sensors when new sensors are connected, otherwise dont change
sensorpath1 = '/sys/bus/w1/devices/28-0219917790d4/w1_slave'

#switch channels "OFF" and "ON" depending which channels will be used; channels 1-8 are constant current (700 mA); channels 9-12 are constant voltage and PWM (24 V)
state_channel1 = "ON"
state_channel2 = "OFF"
state_channel3 = "ON"
state_channel4 = "ON"
state_channel5 = "ON"
state_channel6 = "ON"
state_channel7 = "OFF"
state_channel8 = "OFF"
state_channel9 = "ON"
state_channel10 = "ON"
state_channel11 = "ON"
state_channel12 = "ON"

#set the frequency in Hz (standard: 1000), the duty cycle of the LED channel (as standard: from a range of 100) and the range of the duty cycle (standard: 100)
#Pigpio can go to high frequencies but only for specific values (check Pigpio Table below) and freely choosable ranges (25-40000).
#only the frequencies below can be chosen according to the sampling rate that is set on the system (1,2,4,5 or 10µs), see table
#standard sampling rate = 5µs, sampling rate can be set only in the terminal before starting the experiment, going to shorter sampling rates is very CPU intensive
#e.g. to go to 2µs: sudo pigpiod -s 2 
#the pigpiod can be stoped by sudo kill pigpiod
#
#sample rate [µs]      possible frequencies for the software PWM [Hz]
#
#   1                  40000; 20000; 10000; 8000; 5000; 4000; 2500; 2000; 1600; 1250; 1000; 800; 500; 400; 250; 200; 100; 50
#   2                  20000; 10000; 5000; 4000; 2500; 2000; 1250; 1000; 800; 625; 500; 400; 250; 200; 125; 100; 50; 25
#   4                  10000; 5000; 2500; 2000; 1250; 1000; 625; 500; 400; 313; 250; 200; 125; 100; 63; 50; 25; 13
#   5 (standard)	   8000; 4000; 2000; 1600; 1000; 800; 500; 400; 320; 250; 200; 160; 100; 80; 50; 40; 20; 10
#   8	               5000; 2500; 1250; 1000; 625; 500; 313; 250; 200; 156; 125; 100; 63; 50; 31; 25; 13; 6
#   10	               4000; 2000; 1000; 800; 500; 400; 250; 200; 160; 125; 100; 80; 50; 40; 25; 20; 10; 5

#do not change the folling frequences and duty ranges (required for comuncation to the constant current driver)
frequency_channel1 = frequency_channel2 = frequency_channel3 = frequency_channel4 = frequency_channel5 = frequency_channel6 = frequency_channel7 = frequency_channel8 = 100
duty_range1 = duty_range2 = duty_range3 = duty_range4 = duty_range5 = duty_range6 = duty_range7 = duty_range8 = 100

#the following frequences, duty cycles and duty ranges may be altered
frequency_channel9 = 100
frequency_channel10 = 100
frequency_channel11 = 100
frequency_channel12 = 100

duty_range9 = 100
duty_range10 = 100
duty_range11 = 100
duty_range12 = 100

dutycycle_channel1 = 10
dutycycle_channel2 = 10
dutycycle_channel3 = 10
dutycycle_channel4 = 10
dutycycle_channel5 = 10
dutycycle_channel6 = 10
dutycycle_channel7 = 10
dutycycle_channel8 = 10
dutycycle_channel9 = 90
dutycycle_channel10 = 90
dutycycle_channel11 = 90
dutycycle_channel12 = 90

#set the reaction times in seconds
reactiontime1 = 60*60*16
reactiontime2 = 60*60*16
reactiontime3 = 60*60*16
reactiontime4 = 60*60*16
reactiontime5 = 60*60*16
reactiontime6 = 60*60*16
reactiontime7 = 60*60*16
reactiontime8 = 60*60*16
reactiontime9 = 60*60*16
reactiontime10 = 60*60*16
reactiontime11 = 60*60*16
reactiontime12 = 60*60*16

#do not change the folling numbers of the GPIO pins
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

#Tthe reaction parameters are packed into two nested lists (essentially a table with all channels as columns and all settings as rows).
#For each channel a list with all settings is generated and then all these lists are combined to the nested list
settings_channel_1 = [pin_channel1, state_channel1, frequency_channel1, duty_range1, dutycycle_channel1, reactiontime1]
settings_channel_2 = [pin_channel2, state_channel2, frequency_channel2, duty_range2, dutycycle_channel2, reactiontime2]
settings_channel_3 = [pin_channel3, state_channel3, frequency_channel3, duty_range3, dutycycle_channel3, reactiontime3]
settings_channel_4 = [pin_channel4, state_channel4, frequency_channel4, duty_range4, dutycycle_channel4, reactiontime4]
settings_channel_5 = [pin_channel5, state_channel5, frequency_channel5, duty_range5, dutycycle_channel5, reactiontime5]
settings_channel_6 = [pin_channel6, state_channel6, frequency_channel6, duty_range6, dutycycle_channel6, reactiontime6]
settings_channel_7 = [pin_channel7, state_channel7, frequency_channel7, duty_range7, dutycycle_channel7, reactiontime7]
settings_channel_8 = [pin_channel8, state_channel8, frequency_channel8, duty_range8, dutycycle_channel8, reactiontime8]
settings_channel_9 = [pin_channel9, state_channel9, frequency_channel9, duty_range9, dutycycle_channel9, reactiontime9]
settings_channel_10 = [pin_channel10, state_channel10, frequency_channel10, duty_range10, dutycycle_channel10, reactiontime10]
settings_channel_11 = [pin_channel11, state_channel11, frequency_channel11, duty_range11, dutycycle_channel11, reactiontime11]
settings_channel_12 = [pin_channel12, state_channel12, frequency_channel12, duty_range12, dutycycle_channel12, reactiontime12]
settings_all_channels = [settings_channel_1, settings_channel_2, settings_channel_3, settings_channel_4, settings_channel_5, settings_channel_6, settings_channel_7, settings_channel_8, settings_channel_9, settings_channel_10, settings_channel_11, settings_channel_12]

#set the reaction temperature in °C
reactiontemperature1 = 30

#set intervall of data logging in sec (to be exact in cycles of the while loop), should be the same or an integer multiple of controllintervall and greater than 1
reportintervall = 5

#set mode of experiment "single" for single-experiment, "seq" for sequential. The first experiment in a sequence must be single 
experimentmode = "single"

#define location and name of the logfile
logfilepath = './log1.csv'

#set parameters for PI(D) controller, controllintervall needs to be grather than 2 sec, as this is the measurement time required by the temperature sensors
controllerP = 10
controllerI = 0.5
controllIntervall = 5

#get the time when the experiment was started
overallstartingtime = time.time()

#run experiment
runexp.run_experiment(settings_all_channels, controllerP, controllerI, controllIntervall, reactiontemperature1, reportintervall, experimentmode, overallstartingtime, logfilepath, sensorpath1)

#to run a sequence of experiments: change variable values below, set the experiment into sequential mode and rund the run_experiment() function again.
#all unchanged variables are identical as above

#uncomment below to test:
#experimentmode = "seq"
#most straight forward is to directly edit the nested list above. 
#therefore use settings_all_channels[number of the channel][number of the setting]
#for number of the channel: take the channel number
#numbers of the settings: 0:GPIO pin of the channel; 1:state of the channel [ON or OFF]; 2: frequency of the channel; 3: duty range of the channel; 4: duty cycle of the channel; 5 reaction time of the channel
#e.g. to change the duty cycle of channel 5:
#settings_all_channels[4][4] = 100
#runexp.run_experiment(settings_all_channels, controllerP, controllerI, controllIntervall, reactiontemperature1, reportintervall, experimentmode, overallstartingtime, logfilepath, sensorpath1)