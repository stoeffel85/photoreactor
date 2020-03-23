# coding=utf-8
import os    #import os module
import reactor_programm_fast as runexp #the second file of this script with the programm
import time #to measure the overall startingtime

#adjust these once for the correct path to the temperature sensors when new sensors are connected, otherwise dont change
sensorpath1 = sensorpath2 = '/sys/bus/w1/devices/28-0219917790d4/w1_slave'
# sensorpath2 = '/sys/bus/w1/devices/28-021481625dff/w1_slave'

#switch channels "OFF" and "ON" depending which channels will be used; channels 1-8 are constant current (700 mA); channels 9-12 are constant voltage and PWM (24 V)
LEDchannel1 = "ON"
LEDchannel2 = "ON"
LEDchannel3 = "ON"
LEDchannel4 = "ON"
LEDchannel5 = "ON"
LEDchannel6 = "ON"
LEDchannel7 = "ON"
LEDchannel8 = "ON"
LEDchannel9 = "ON"
LEDchannel10 = "ON"
LEDchannel11 = "ON"
LEDchannel12 = "ON"

#set the frequency in Hz (standard: 1000), the duty cycle of the LED channel (as standard: from a range of 100) and the range of the duty cycle (standard: 100)
#Pigpio can go to high frequencies but only for specific values (check Pigpio Table below) and freely choosable ranges (25-40000).
#only the frequencies below can be chosen according to the sampling rate that is set on the system (1,2,4,5 or 10us), see table
#standard sampling rate = 5µs, sampling rate can be set only in the terminal before starting the experiment, going to shorter sampling rates is very CPU intensive
#e.g. to go to 2µs: sudo pigpiod -s 2 
#the pigpiod can be stoped by sudo kill pigpiod
#
#sample rate [µs]           possible frequencies for the software PWM [Hz]
#
#   1                  40000; 20000; 10000; 8000; 5000; 4000; 2500; 2000; 1600; 1250; 1000; 800; 500; 400; 250; 200; 100; 50
#   2                  20000; 10000; 5000; 4000; 2500; 2000; 1250; 1000; 800; 625; 500; 400; 250; 200; 125; 100; 50; 25
#   4                  10000; 5000; 2500; 2000; 1250; 1000; 625; 500; 400; 313; 250; 200; 125; 100; 63; 50; 25; 13
#   5 (standard)	   8000; 4000; 2000; 1600; 1000; 800; 500; 400; 320; 250; 200; 160; 100; 80; 50; 40; 20; 10
#   8	               5000; 2500; 1250; 1000; 625; 500; 313; 250; 200; 156; 125; 100; 63; 50; 31; 25; 13; 6
#   10	               4000; 2000; 1000; 800; 500; 400; 250; 200; 160; 125; 100; 80; 50; 40; 25; 20; 10; 5

# Do not change the folling frequences and duty ranges (required for constant current driver)
frequency_channel1 = frequency_channel2 = frequency_channel3 = frequency_channel4 = frequency_channel5 = frequency_channel6 = frequency_channel7 = frequency_channel8 = 100
duty_range1 = duty_range2 = duty_range3 = duty_range4 = duty_range5 = duty_range6 = duty_range7 = duty_range8 = 100

# These frequences, duty cycles and duty ranges may be altered
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
reactiontime1 = 2000
reactiontime2 = 2000
reactiontime3 = 2000
reactiontime4 = 2000
reactiontime5 = 2000
reactiontime6 = 2000
reactiontime7 = 2000
reactiontime8 = 2000
reactiontime9 = 2000
reactiontime10 = 2000
reactiontime11 = 2000
reactiontime12 = 2000

#set the reaction temperatures in °C
reactiontemperature1 = reactiontemperature2 = 30
#reactiontemperature2 = 25

#set intervall of data logging in sec (to be exact in cycles of the while loop), should be the same or an integral multiple as controllintervall and greater than 1
reportintervall = 5

#set mode of experiment "single" for single-experiment, "seq" for sequential. The first experiment in  a sequence must be single 
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
runexp.run_experiment(controllerP, controllerI, controllIntervall, LEDchannel1, LEDchannel2, LEDchannel3, LEDchannel4, LEDchannel5, LEDchannel6, LEDchannel7, LEDchannel8, LEDchannel9, LEDchannel10, LEDchannel11, LEDchannel12, reactiontime1, reactiontime2, reactiontime3, reactiontime4, reactiontime5, reactiontime6, reactiontime7, reactiontime8, reactiontime9, reactiontime10, reactiontime11, reactiontime12, reactiontemperature1, reactiontemperature2, dutycycle_channel1, dutycycle_channel2, dutycycle_channel3, dutycycle_channel4, dutycycle_channel5, dutycycle_channel6, dutycycle_channel7, dutycycle_channel8, dutycycle_channel9, dutycycle_channel10, dutycycle_channel11, dutycycle_channel12, duty_range1, duty_range2, duty_range3, duty_range4, duty_range5, duty_range6, duty_range7, duty_range8, duty_range9, duty_range10, duty_range11, duty_range12, frequency_channel1, frequency_channel2, frequency_channel3, frequency_channel4, frequency_channel5, frequency_channel6, frequency_channel7, frequency_channel8, frequency_channel9, frequency_channel10, frequency_channel11, frequency_channel12, reportintervall, experimentmode, overallstartingtime, logfilepath, sensorpath1, sensorpath2)

#to run a sequence of experiments: change variable values below, set the experiment into sequential mode and rund the run_experiment() function again.
#all unchanged variables are identical as above

#uncomment below to test:
#experimentmode = "seq"
#reactiontime3 = 9
#reactiontime4 = 20
#runexp.run_experiment(controllerP, controllerI, controllIntervall, LEDchannel1, LEDchannel2, LEDchannel3, LEDchannel4, LEDchannel5, LEDchannel6, LEDchannel7, LEDchannel8, LEDchannel9, LEDchannel10, LEDchannel11, LEDchannel12, reactiontime1, reactiontime2, reactiontime3, reactiontime4, reactiontime5, reactiontime6, reactiontime7, reactiontime8, reactiontime9, reactiontime10, reactiontime11, reactiontime12, reactiontemperature1, reactiontemperature2, dutycycle_channel1, dutycycle_channel2, dutycycle_channel3, dutycycle_channel4, dutycycle_channel5, dutycycle_channel6, dutycycle_channel7, dutycycle_channel8, dutycycle_channel9, dutycycle_channel10, dutycycle_channel11, dutycycle_channel12, duty_range1, duty_range2, duty_range3, duty_range4, duty_range5, duty_range6, duty_range7, duty_range8, duty_range9, duty_range10, duty_range11, duty_range12, frequency_channel1, frequency_channel2, frequency_channel3, frequency_channel4, frequency_channel5, frequency_channel6, frequency_channel7, frequency_channel8, frequency_channel9, frequency_channel10, frequency_channel11, frequency_channel12, reportintervall, experimentmode, overallstartingtime, logfilepath, sensorpath1, sensorpath2)

#stop the pigpiod
os.system('sudo killall pigpiod')