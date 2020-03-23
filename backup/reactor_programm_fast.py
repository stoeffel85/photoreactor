# coding=utf-8
import time  #required to work with time.
import csv   #required to work with csv files.
import os    #import os module
os.system('sudo pigpiod') #switch on pigpiod in the console
import pigpio #import pigpio


#set the global variables for the PI(D) controller
controllerSum1and2 = 0
controllerSum3and4 = 0

#this function starts the PWM for the LED-stripes and can only be called after the pigpio has been initialized with pi = pigpio.pi()
def start_hardware_timed_software_pwm(pi, pin, frequency, range, duty_cycle):
    pi.set_mode(pin, pigpio.OUTPUT) #switch pin to output
    pi.set_PWM_frequency(pin, frequency)  #set_PWM_frequency(4, 1100) sets the frequency of pin 4 to the closest choosable frequency of t (check pigpio table)
    pi.set_PWM_range(pin, range) #sets the range of the gpio to the second number, e.g. 100 to work in %,
    pi.set_PWM_dutycycle(pin, duty_cycle) #sets the dutycycle of a pin according to pwmrange (if 100, then in %), also starts the pwm

#this stops the PWM for the LED stripes
def stop_hardware_timed_software_pwm(pi, pin):
    pi.set_PWM_dutycycle(pin, 0) #sets the dutycycle of a pin according to pwmrange (if 100, then in %), also stops the pwm
    pi.set_mode(pin, pigpio.INPUT) #switch pin back to output
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
    while lines[0].strip()[-3:] != 'YES':   #check if data
        time.sleep(0.2)
        lines = get_temperature_raw(sensorpath)  #get the tempeature data from the sensor file
    equals_pos = lines[1].find('t=')       #find temperature in the details
    if equals_pos != -1:                   #ignore first line of the file
        temp_string = lines[1][equals_pos+2:]
        temperature = float(temp_string) / 1000.0   #convert to Celsius
        return temperature

#PI(D)regulate the reactiontemperature for zone 1
def regulate_reaction_temperature1(pi, controllerP, controllerI, targettemperature, measuredtemperature):
    global controllerSum1and2 #get the global variables
    Tdifference = measuredtemperature - targettemperature #calculate the difference from the target temperature
    controllerSum1and2 = controllerSum1and2 + Tdifference
    pDiff = Tdifference * controllerP #calculate the P parameter
    iDiff = controllerSum1and2 * controllerI #calculate the I parametre
    fanSpeed = pDiff + iDiff #set the new fan-speed in %
    if fanSpeed > 100:
        fanSpeed = 100
    if fanSpeed < 15:
        fanSpeed = 15
    if controllerSum1and2 > 100: #set the controlersum for the next iteration of the regulation
        controllerSum1and2 = 100
    if controllerSum1and2 < -100:
        controllerSum1and2 = -100
    calcdutycycle = round(fanSpeed * 10000) #calculate the dutycyle for the PWM regulation of the fanspeed from the fanspeed in %
    pi.hardware_PWM(18, 25000, calcdutycycle) #  pin 18, 25000Hz and dutycycle,
    #For tuning etc. print the parameters
    #print("measured T1,2: " + str(measuredtemperature) + "°C; Target T1,4: " + str(targettemperature) + "°C; Fanspeed: " + str(fanSpeed) + "%; pDiff: " + str(pDiff) + "; iDiff:" + str(iDiff) + "; controllerSum1and2: "+ str(controllerSum1and2))
    return fanSpeed

#PI(D)regulate the reactiontemperature for zone 2
#def regulate_reaction_temperature2(pi, controllerP, controllerI, targettemperature, measuredtemperature):
#    global controllerSum3and4 #get the global variables
#    Tdifference = measuredtemperature - targettemperature #calculate the difference from the target temperature
#    controllerSum3and4 = controllerSum3and4 + Tdifference
#    pDiff = Tdifference * controllerP #calculate the P parameter
#    iDiff = controllerSum3and4 * controllerI #calculate the I parametre
#    fanSpeed = pDiff + iDiff #set the new fan-speed in %
#    if fanSpeed > 100:
#        fanSpeed = 100
#    if fanSpeed < 15:
#        fanSpeed = 15
#    if controllerSum3and4 > 100: #set the controlersum for the next iteration of the regulation
#        controllerSum3and4 = 100
#    if controllerSum3and4 < -100:
#        controllerSum3and4 = -100
#    calcdutycycle = round(fanSpeed * 10000) #calculate the dutycyle for the PWM regulation of the fanspeed from the fanspeed in %
#    pi.hardware_PWM(13, 25000, calcdutycycle) #  pin 13, 25000Hz and dutycycle,
    #For tuning etc. print the parameters
    #print("measured T3,4: " + str(measuredtemperature) + "°C; Target T3,4: " + str(targettemperature) + "°C; Fanspeed: " + str(fanSpeed) + "%; pDiff: " + str(pDiff) + "; iDiff:" + str(iDiff) + "; controllerSum3and4: "+ str(controllerSum3and4))
#    return fanSpeed

#print the status as table in the console
def show_status_formated(tup):
    formated = u'{:<11} {:<6} {:<3} {:6} {:4} {:<6} {:<3} {:6} {:4} {:<7} {:6} {:4} {:<4} {:<6} {:<3} {:6} {:4} {:<6} {:<3} {:6} {:4} {:<7} {:6} {:4} {:<4}'.format(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12], tup[13], tup[14], tup[15], tup[16], tup[17], tup[18], tup[19], tup[20], tup[21], tup[22], tup[23], tup[24])
    print(formated)
    return formated

#write the status to the CSV-logfile
def write_to_csv(logfilepath, datarow, mode):
   logfile = open(logfilepath, mode)
   with logfile:
       writer = csv.writer(logfile, delimiter=',', lineterminator='\n')
       for row in datarow:
           writer.writerow(row)


#starts an experiment with one set of parameters.
def run_experiment(controllerP, controllerI, controllIntervall, LEDchannel1, LEDchannel2, LEDchannel3, LEDchannel4, LEDchannel5, LEDchannel6, LEDchannel7, LEDchannel8, LEDchannel9, LEDchannel10, LEDchannel11, LEDchannel12, reactiontime1, reactiontime2, reactiontime3, reactiontime4, reactiontime5, reactiontime6, reactiontime7, reactiontime8, reactiontime9, reactiontime10, reactiontime11, reactiontime12, reactiontemperature1, reactiontemperature2, dutycycle_channel1, dutycycle_channel2, dutycycle_channel3, dutycycle_channel4, dutycycle_channel5, dutycycle_channel6, dutycycle_channel7, dutycycle_channel8, dutycycle_channel9, dutycycle_channel10, dutycycle_channel11, dutycycle_channel12, duty_range1, duty_range2, duty_range3, duty_range4, duty_range5, duty_range6, duty_range7, duty_range8, duty_range9, duty_range10, duty_range11, duty_range12, frequency_channel1, frequency_channel2, frequency_channel3, frequency_channel4, frequency_channel5, frequency_channel6, frequency_channel7, frequency_channel8, frequency_channel9, frequency_channel10, frequency_channel11, frequency_channel12, reportintervall, experimentmode, overallstartingtime, logfilepath, sensorpath1, sensorpath2):

   try:
        startingtime = time.time() #measure startingtime for control of the reactiontime
"""        controllIntervall -= 2 #substract 2 seconds from the controllintervall, as this is the time that is consumed by the temperature measurement
        controllIntervallstate = controllIntervall #start counter of the controllintervall in a way, that the cotroll starts already at the experiments start
        reportintervallstate = reportintervall #start counter of the reportintervall in a way, that the report starts right at the begining of the experiment
"""
        pi = pigpio.pi()  # connect pigpio to the gpio of the pi

        print("The startingtime of the experiment is", startingtime) #starting time of the call of this run_experiment() function
        print("The overall startingtime is", overallstartingtime) #starting time of the first call of this run_experiment() function; differs from startingtime when this funciton is called several times to generate changing conditions over time (e.g. reaction temperature gradient, experimentmode = seq)

        #start logfile if this is the first call of the run_experiment() function
        if experimentmode == "single":
            write_to_csv(logfilepath, [["time in [sec]", "LEDchanel1 state", "LEDchannel1 frequency [Hz]", "LEDchannel1 duty cycle [%]", "LEDchanel2 state", "LEDchannel2 frequency [Hz]", "LEDchannel2 duty cycle [%]", "temperature 1 [°C]", "speed fan 1 [%]", "LEDchanel3 state", "LEDchannel3 frequency [Hz]", "LEDchannel3 duty cycle [%]", "LEDchanel4 state", "LEDchannel4 frequency [Hz]", "LEDchannel4 duty cycle [%]", "temperature 2 [°C]", "speed fan 2 [%]"]], 'w')

        #switch on the LED stripes
        if LEDchannel1 == "ON":
            start_hardware_timed_software_pwm(pi, 24, frequency_channel1, duty_range1, dutycycle_channel1)
        if LEDchannel2 == "ON":
            start_hardware_timed_software_pwm(pi, 10, frequency_channel2, duty_range2, dutycycle_channel2)
        if LEDchannel3 == "ON":
            start_hardware_timed_software_pwm(pi, 9, frequency_channel3, duty_range3, dutycycle_channel3)
        if LEDchannel4 == "ON":
            start_hardware_timed_software_pwm(pi, 25, frequency_channel4, duty_range4, dutycycle_channel4)
        if LEDchannel5 == "ON":
            start_hardware_timed_software_pwm(pi, 11, frequency_channel5, duty_range5, dutycycle_channel5)
        if LEDchannel6 == "ON":
            start_hardware_timed_software_pwm(pi, 8, frequency_channel6, duty_range6, dutycycle_channel6)
        if LEDchannel7 == "ON":
            start_hardware_timed_software_pwm(pi, 7, frequency_channel7, duty_range7, dutycycle_channel7)
        if LEDchannel8 == "ON":
            start_hardware_timed_software_pwm(pi, 5, frequency_channel8, duty_range8, dutycycle_channel8)
        if LEDchannel9 == "ON":
            start_hardware_timed_software_pwm(pi, 17, frequency_channel9, duty_range9, dutycycle_channel9)
        if LEDchannel10 == "ON":
            start_hardware_timed_software_pwm(pi, 27, frequency_channel10, duty_range10, dutycycle_channel10)
        if LEDchannel11 == "ON":
            start_hardware_timed_software_pwm(pi, 22, frequency_channel11, duty_range11, dutycycle_channel11)
        if LEDchannel12 == "ON":
            start_hardware_timed_software_pwm(pi, 23, frequency_channel12, duty_range12, dutycycle_channel12)

        #switch on the channels for the hardware PWM for fan speed controll
#        pi.set_mode(18, pigpio.OUTPUT)
        pi.set_mode(13, pigpio.OUTPUT)
        
        #for as long as at least one of the LED-stripes is On, check the reactiontimes, controll the temperatures and the fan speed and print & log the status
        while LEDchannel1 == "ON" or LEDchannel2 == "ON" or LEDchannel3 == "ON" or LEDchannel4 == "ON" or LEDchannel5 == "ON" or LEDchannel6 == "ON" or LEDchannel7 == "ON" or LEDchannel8 == "ON" or LEDchannel9 == "ON" or LEDchannel10 == "ON" or LEDchannel11 == "ON" or LEDchannel12 == "ON":
            time.sleep(0.1) #wait 0.1 second
            now = time.time() #measure currend time to calculate the passed reactiontime

            #If the reactiontime passed, swith off the appropriate channel
            if LEDchannel1 == "ON" and startingtime + reactiontime1 < now:
                LEDchannel1 = stop_hardware_timed_software_pwm(pi, 24)
            if LEDchannel2 == "ON" and startingtime + reactiontime2 < now:
                LEDchannel2 = stop_hardware_timed_software_pwm(pi, 10)
            if LEDchannel3 == "ON" and startingtime + reactiontime3 < now:
                LEDchannel3 = stop_hardware_timed_software_pwm(pi, 9)
            if LEDchannel4 == "ON" and startingtime + reactiontime4 < now:
                LEDchannel4 = stop_hardware_timed_software_pwm(pi, 25)
            if LEDchannel5 == "ON" and startingtime + reactiontime1 < now:
                LEDchannel5 = stop_hardware_timed_software_pwm(pi, 11)
            if LEDchannel6 == "ON" and startingtime + reactiontime2 < now:
                LEDchannel6 = stop_hardware_timed_software_pwm(pi, 8)
            if LEDchannel7 == "ON" and startingtime + reactiontime3 < now:
                LEDchannel7 = stop_hardware_timed_software_pwm(pi, 7)
            if LEDchannel8 == "ON" and startingtime + reactiontime4 < now:
                LEDchannel8 = stop_hardware_timed_software_pwm(pi, 5)
            if LEDchannel9 == "ON" and startingtime + reactiontime1 < now:
                LEDchannel9 = stop_hardware_timed_software_pwm(pi, 17)
            if LEDchannel10 == "ON" and startingtime + reactiontime2 < now:
                LEDchannel10 = stop_hardware_timed_software_pwm(pi, 27)
            if LEDchannel11 == "ON" and startingtime + reactiontime3 < now:
                LEDchannel11 = stop_hardware_timed_software_pwm(pi, 22)
            if LEDchannel12 == "ON" and startingtime + reactiontime4 < now:
                LEDchannel12 = stop_hardware_timed_software_pwm(pi, 23)

"""            if controllIntervallstate >= controllIntervall: #after a specific time (controllintervall) measure temperatures and perform the next iteration of the PID controll 
                #measure temperatures, takes beween 0.5 and 1sec
                temperature1 = get_temperature(sensorpath1)
                temperature2 = get_temperature(sensorpath1)
#                temperature2 = get_temperature(sensorpath2)
                reportintervallstate += 2 #add two to the reportintervall, as this is the measurement time of the temperature sensors and then regulate the temperatures
                fanspeed1 = regulate_reaction_temperature1(pi, controllerP, controllerI, reactiontemperature1, temperature1)
                fanspeed2 = regulate_reaction_temperature1(pi, controllerP, controllerI, reactiontemperature1, temperature1)
#                fanspeed2 = regulate_reaction_temperature2(pi, controllerP, controllerI, reactiontemperature2, temperature2)
                controllIntervallstate = 0 #reset the counter for the controllintervall

            controllIntervallstate += 1 #add 1 to the counter for the controllintrevall

            if reportintervallstate >= reportintervall: #after a specific time (reportintervall) print and log the current parameters 
                pasttime = round(now - overallstartingtime, 1) #calculate for how long the experiment is going on
                #print to console
                show_status_formated((str(pasttime) + "sec", '| Ch1:', LEDchannel1, str(output_frequency(17, pi)) + "Hz", str(round(calculate_duty_cycle_output(17, pi))) + "%", '| Ch2:', LEDchannel2, str(output_frequency(27, pi)) + "Hz", str(round(calculate_duty_cycle_output(27, pi))) + "%", '| T1&2:', str(round(temperature1, 1))+"°C", 'Fan:', str(round(fanspeed1)) + "%", '| Ch3:', LEDchannel3, str(output_frequency(22, pi)) + "Hz", str(round(calculate_duty_cycle_output(22, pi))) + "%", '| Ch4:', LEDchannel4, str(output_frequency(23, pi)) + "Hz", str(round(calculate_duty_cycle_output(23, pi))) + "%", '| T3&4:', str(round(temperature2, 1))+"°C", 'Fan:', str(round(fanspeed2)) + "%"))
                #write to logfile
                write_to_csv(logfilepath, [[pasttime, LEDchannel1, output_frequency(17, pi), calculate_duty_cycle_output(17, pi), LEDchannel2, output_frequency(27, pi), calculate_duty_cycle_output(27, pi), temperature1, fanspeed1, LEDchannel3, output_frequency(22, pi), calculate_duty_cycle_output(22, pi), LEDchannel4, output_frequency(23, pi), calculate_duty_cycle_output(23, pi), temperature2, fanspeed2]], 'a')
                #reset the counter for the reportintervall
                reportintervallstate = 0

            reportintervallstate += 1 #add 1 to the counter for the reportintervall
"""
        #stop fans
        pi.hardware_PWM(18, 0, 0)
        pi.set_mode(18, pigpio.INPUT)
        pi.hardware_PWM(13, 0, 0)
        pi.set_mode(13, pigpio.INPUT)
        pi.stop()  #stop connection
        print("after reaction", time.time())
        print("time passed:", time.time()-startingtime)

   except KeyboardInterrupt: #in case the experiment is abortet (Strg + C
       #stop LEDs
       pi.set_PWM_dutycycle(24, 0)
       pi.set_mode(24, pigpio.INPUT)
       pi.set_PWM_dutycycle(10, 0)
       pi.set_mode(10, pigpio.INPUT)
       pi.set_PWM_dutycycle(9, 0)
       pi.set_mode(9, pigpio.INPUT)
       pi.set_PWM_dutycycle(25, 0)
       pi.set_mode(25, pigpio.INPUT)
       pi.set_PWM_dutycycle(11, 0)
       pi.set_mode(11, pigpio.INPUT)
       pi.set_PWM_dutycycle(8, 0)
       pi.set_mode(8, pigpio.INPUT)
       pi.set_PWM_dutycycle(7, 0)
       pi.set_mode(7, pigpio.INPUT)
       pi.set_PWM_dutycycle(5, 0)
       pi.set_mode(5, pigpio.INPUT)
       pi.set_PWM_dutycycle(17, 0)
       pi.set_mode(17, pigpio.INPUT)
       pi.set_PWM_dutycycle(27, 0)
       pi.set_mode(27, pigpio.INPUT)
       pi.set_PWM_dutycycle(22, 0)
       pi.set_mode(22, pigpio.INPUT)
       pi.set_PWM_dutycycle(23, 0)
       pi.set_mode(23, pigpio.INPUT)
       #stop fans
#       pi.hardware_PWM(18, 0, 0)
#       pi.set_mode(18, pigpio.INPUT)
       pi.hardware_PWM(13, 0, 0)
       pi.set_mode(13, pigpio.INPUT)
       pi.stop() #stop connection
       #stop the pigpiod
       os.system('sudo killall pigpiod')
       print("The experiment was stopped manually")