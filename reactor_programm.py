# Copyright 2021 by Christoph Winkler and Wolfgang Kroutil, University of Graz, Austria.
# This file is part of the "Open Source Photoreactor for Parallel Evaluation 
# of Small-Scale Reactions" by Christoph Winkler and is licensed under a 
# Creative Commons Attribution-ShareAlike 4.0 International (BY-SA) License.
# http://creativecommons.org/licenses/by-sa/4.0/
# https://github.com/stoeffel85/photoreactor
# Permissions beyond the scope of this license may be available at http://biocatalysis.uni-graz.at.
# This script uses Pigpio: http://abyz.me.uk/rpi/pigpio/python.html

# coding=utf-8

import time  #work with time.
import csv   #work with csv files.
import os    #import os module
os.system('sudo pigpiod') #switch on pigpiod in the shell
import pigpio #import pigpio

#set the global variables for the PI(D) controller
controller_sum = 0

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

#measure the PWM frequency of a pin
def output_frequency(pin, pi):
    if pi.get_mode(pin) == 0: #check if the pin is on output mode
        f = 0
    else:
        f = pi.get_PWM_frequency(pin) #measure the PWM frequency of a pin
    return f

#measure the duty cycle of a pin in %
def calculate_duty_cycle_output(pin, pi):
    if pi.get_mode(pin) == 0: #check if the pin is on output mode
        dc = 0
    else:
        dc = pi.get_PWM_dutycycle(pin)*100/pi.get_PWM_range(pin) #measure and caclulate the duty cycle of a pin in %
    return dc

#get the raw temperature data from the sensor file
def get_temperature_raw(sensorpath):
    f = open(sensorpath, 'r') #open the file
    lines = f.readlines()     #read the device details
    f.close()                 #close the file
    return lines

#get the raw temperature from a sensor
def get_temperature(sensorpath):
    lines = get_temperature_raw(sensorpath) #get the tempeature data from the sensor file
    while lines[0].strip()[-3:] != 'YES':   #check if contains data
        time.sleep(0.2)
        lines = get_temperature_raw(sensorpath)  #get the tempeature data from the sensor file
    pos = lines[1].find('t=')       #find temperature
    if pos != -1:                   #ignore first line
        temperature_string = lines[1][pos+2:]
        temperature = float(temperature_string) / 1000.0   #convert to Celsius
        return temperature

#PI(D) regulate the reactiontemperature
def regulate_reaction_temperature1(pi, controllerP, controllerI, targettemperature, measuredtemperature):
    global controller_sum #get the global variables
    Tdifference = measuredtemperature - targettemperature #calculate the difference from the target temperature
    controller_sum = controller_sum + Tdifference
    pDiff = Tdifference * controllerP #calculate the P parameter
    iDiff = controller_sum * controllerI #calculate the I parametre
    fanSpeed = pDiff + iDiff #set the new fan-speed in %
    if fanSpeed > 100:
        fanSpeed = 100
    elif fanSpeed < 15:
        fanSpeed = 15
    if controller_sum > 100: #set the controlersum for the next iteration of the regulation
        controller_sum = 100
    elif controller_sum < -100:
        controller_sum = -100
    calcdutycycle = round(fanSpeed * 10000) #calculate the dutycyle for the PWM regulation of the fanspeed from the fanspeed in %
    pi.hardware_PWM(18, 25000, calcdutycycle) #  pin 18, 25000Hz and dutycycle,
    
    #for tuning etc. print the parameters
    #print("measured T: " + str(measuredtemperature) + "°C; Target T: " + str(targettemperature) + "°C; Difference:" + str(Tdifference) + "°C; Fanspeed: " + str(fanSpeed) + "%, pDiff: " + str(pDiff) + "; iDiff:" + str(iDiff) + "; controller_sum: " + str(controller_sum))
    
    return fanSpeed

#write the status to the CSV-logfile
def write_to_csv(logfilepath, datarow, mode):
    logfile = open(logfilepath, mode)
    if mode == "w":
        with logfile:
            writer = csv.writer(logfile, delimiter=',', lineterminator='\n')
            for row in datarow:
                writer.writerow(row)
    if mode == "a":
        with logfile:
            for entries in datarow:
                logfile.write(entries)
                logfile.write(",")
            logfile.write("\n")


#starts an experiment with one set of parameters.
def run_experiment(settings_all_channels, controllerP, controllerI, controllIntervall, reactiontemperature1, reportintervall, experimentmode, overallstartingtime, logfilepath, sensorpath1):
   try:
        startingtime = time.time() #measure startingtime for control of the reactiontime
        controllIntervall -= 1 #substract the number of temperature measurements  from the controllintervall, as this is the time in seconds that is consumed one temperature measurement
        controllIntervallstate = controllIntervall #start counter of the controllintervall so that the controll starts already at the experiments start
        reportintervallstate = reportintervall #start counter of the reportintervall so that the report starts right at the begining of the experiment

        pi = pigpio.pi()  #connect pigpio to the gpio of the pi

        print("-------------------------------------------------------------------------------------------------------------------------------------")
        print("The startingtime of the experiment is", startingtime, "sec") #starting time of the call of this run_experiment() function
        print("The overall startingtime is", overallstartingtime, "sec") #starting time of the first call of this run_experiment() function; differs from startingtime when this funciton is called several times to generate changing conditions over time (e.g. reaction temperature gradient, experimentmode = seq)
        print("|-----------------------------------------------------------------|-----------------------------------------------------------------|")

        #start logfile if this is the first call of the run_experiment() function
        if experimentmode == "single":
            write_to_csv(logfilepath, [["time in [sec]", "temperature [°C]", "speed cooling fans [%]","LEDchanel1 state", "LEDchannel1 frequency [Hz]", "LEDchannel1 duty cycle [%]", "LEDchanel2 state", "LEDchannel2 frequency [Hz]", "LEDchannel2 duty cycle [%]", "LEDchanel3 state", "LEDchannel3 frequency [Hz]", "LEDchannel3 duty cycle [%]", "LEDchanel4 state", "LEDchannel4 frequency [Hz]", "LEDchannel4 duty cycle [%]", "LEDchanel5 state", "LEDchannel5 frequency [Hz]", "LEDchannel5 duty cycle [%]", "LEDchanel6 state", "LEDchannel6 frequency [Hz]", "LEDchannel6 duty cycle [%]", "LEDchanel7 state", "LEDchannel7 frequency [Hz]", "LEDchannel7 duty cycle [%]", "LEDchanel8 state", "LEDchannel8 frequency [Hz]", "LEDchannel8 duty cycle [%]", "LEDchanel9 state", "LEDchannel9 frequency [Hz]", "LEDchannel9 duty cycle [%]", "LEDchanel10 state", "LEDchannel10 frequency [Hz]", "LEDchannel10 duty cycle [%]", "LEDchanel11 state", "LEDchannel11 frequency [Hz]", "LEDchannel11 duty cycle [%]", "LEDchanel12 state", "LEDchannel12 frequency [Hz]", "LEDchannel12 duty cycle [%]"]], 'w')

        #switch on the LED stripes and set the channels that are "OFF" to a duty cycle of "0"
        for i in range(12):
            if settings_all_channels[i][1] == "ON":
                start_hardware_timed_software_pwm(pi, settings_all_channels[i][0], settings_all_channels[i][2], settings_all_channels[i][3], settings_all_channels[i][4])
        for i in range(12):
            if settings_all_channels[i][1] == "OFF":
                start_hardware_timed_software_pwm(pi, settings_all_channels[i][0], settings_all_channels[i][2], settings_all_channels[i][3], 0)

        #switch on the GPIO for the hardware PWM for fan speed controll
        pi.set_mode(18, pigpio.OUTPUT) #reactor fan
        
        #for as long as at least one of the LED-stripes is ON, check the reactiontimes, controll the temperatures and the fan speed and print & log the status
        while settings_all_channels[0][1] == "ON" or settings_all_channels[1][1] == "ON" or settings_all_channels[2][1] == "ON" or settings_all_channels[3][1] == "ON" or settings_all_channels[4][1] == "ON" or settings_all_channels[5][1] == "ON" or settings_all_channels[6][1] == "ON" or settings_all_channels[7][1] == "ON" or settings_all_channels[8][1] == "ON" or settings_all_channels[9][1] == "ON" or settings_all_channels[10][1] == "ON" or settings_all_channels[11][1]== "ON":

            time.sleep(1) #wait 1 second
            now = time.time() #get current time to calculate the passed reactiontime

            #When the reactiontime has passed, swith off the appropriate channel(s)
            for i in range(12):
                if settings_all_channels[i][1] == "ON" and startingtime + settings_all_channels[i][5] < now:
                    settings_all_channels[i][1] = stop_hardware_timed_software_pwm(pi, settings_all_channels[i][0])

            if controllIntervallstate >= controllIntervall: #after a specific time (controllintervall) measure temperatures and perform the next iteration of the PID controll 
                #measuring temperature, takes beween 0.5 and 1sec
                temperature1 = get_temperature(sensorpath1)
                reportintervallstate += 1 #add 1 to the reportintervall, as this is the measurement time of the temperature sensors and then regulate the temperatures
                fanspeed1 = regulate_reaction_temperature1(pi, controllerP, controllerI, reactiontemperature1, temperature1)
                controllIntervallstate = 0 #reset the counter for the controllintervall

            controllIntervallstate += 1 #add 1 to the counter for the controllintervall

            if reportintervallstate >= reportintervall: #after a specific time (reportintervall) print and log the current parameters 
                passedtime = round(now - overallstartingtime, 1) #calculate for how long the experiment is going on

                #print to console
                print('|  Reactiontime: {:10} sec | Temperature: {:5} °C | Speed Ractor-Fans: {:5} % |'.format(passedtime, round(temperature1, 1), round(fanspeed1, 1)))
                print("|-----------------------------------------------------------------|-----------------------------------------------------------------|")
                for i in range(12): #Print the status, the frequency and the duty cycle for each channel
                    if (i+1)%2 == 0:
                        print('|Channel {:2}: {:3} | Frequency: {:8} Hz | Dutycycle: {:5}%     |     Channel {:2}: {:3} | Frequency: {:8} Hz | Dutycycle: {:5}%|'.format(i, settings_all_channels[i-1][1], output_frequency(settings_all_channels[i-1][0], pi), calculate_duty_cycle_output(settings_all_channels[i-1][0], pi), i+1, settings_all_channels[i][1], output_frequency(settings_all_channels[i][0], pi), calculate_duty_cycle_output(settings_all_channels[i][0], pi) ))
                print("|-----------------------------------------------------------------|-----------------------------------------------------------------|")

                #write to logfile
                datarow = [str(passedtime), str(temperature1), str(fanspeed1)] #start the row with the global parameters
                for i in range(12): #fill the row with the status, the frequency and the duty cycle for each channel
                    datarow.extend([str(settings_all_channels[i][1]), str(output_frequency(settings_all_channels[i][0], pi)), str(calculate_duty_cycle_output(settings_all_channels[i][0], pi))])
                write_to_csv(logfilepath, datarow, 'a')

                #reset the counter for the reportintervall
                reportintervallstate = 0

            reportintervallstate += 1 #add 1 to the counter for the reportintervall

        #stop fans
        pi.hardware_PWM(18, 0, 0)
        pi.set_mode(18, pigpio.INPUT)
        print("Time after reaction:", time.time())

   except KeyboardInterrupt: #in case the experiment is aborted (Strg + C)
       #stop LEDs
       for i in range(12):
            stop_hardware_timed_software_pwm(pi, settings_all_channels[i][0])
       #stop fans
       pi.hardware_PWM(18, 0, 0)
       pi.set_mode(18, pigpio.INPUT)
       print("The experiment was stopped manually")
       print("Time after reaction:", time.time())