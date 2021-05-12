# Open Source Photoreactor for Parallel Evaluation of Small-Scale Reactions

![Open Source Photoreactor for Parallel Evaluation of Small-Scale Reactions](/schemes_and_circuits/GitHub.jpg "Open Source Photoreactor for Parallel Evaluation of Small-Scale Reactions")

## Table of Contents

[Short Description](#short-description)

[Installation and Raspberry Pi Setup](#installation-and-raspberry-pi-setup)

[Reactor Dimensions](#reactor-dimensions)

[Parts List](#parts-list)

[Electronics](#electronics)

[Python Scripts](#python-scripts)

[Usage](#usage)

[Credits (Paper)](#credits-paper)

[License](#license)

## Short Description

Here the plans, scripts and electronic schemes required to build a custom open source photoreactor that is designed to run several small-scale photoreactions in parallel are collected. The reactor has the following features that can be controlled via a python script on a Raspberry Pi minicomputer:

- Has space for up to 24 reaction vials (1.5 mL HPLC vials)
- Allows investigation of four different illumination conditions in parallel (four rows of six vials, each row has space for up to two light sources)
- Allows using different light sources (quick exchange of different light sources with different wavelengths or light color by simple plugging in)
- Allows control of the light intensity (PWM control of the light intensity for each light source with a Raspberry Pi)
- Allows logging and controlling the reaction temperature (measurement of the reaction temperature inside a reaction vial using a digital temperature sensor and temperature control by controlling the speed of external high-power cooling fans)
- Allows controlling shaking speed (with a commercial benchtop shaker)
- Logs all parameters throughout the experiment.

In total the costs of the electronic components with one set of high-power LED bars sums up to ca. EUR 400 (without the commercial benchtop shaker and, if required, an external incubator for better temperature control). The photochemical and thermal features were carefully evaluated and were made available in a publication in a peer-reviewed journal (*to be published*).

## Installation and Raspberry Pi Setup

The photoreactor is controlled by a Raspberry Pi 3B+ running on current Raspbian Stretch ([https://www.raspberrypi.org/software/](https://www.raspberrypi.org/software/)) and is accessed using SSH via LAN or WLAN (SSH needs to be enabled and for better use, a static IP address is recommended).

The following settings need to be made and libraries need to be installed:

### Python

The reactor is controlled via a python script. If not already installed, use the following command to install the libraries:

```
sudo apt-get install python-dev python-pip
```

### Pigpio

This pigpio daemon ([http://abyz.me.uk/rpi/pigpio/pigpiod.html](http://abyz.me.uk/rpi/pigpio/pigpiod.html)) allows control of the Raspberry Pi&#39;s GPIO pins and supports hardware based PWM. To install use the following command:

```
sudo apt-get install pigpio python-pigpio python3-pigpio
```

To start or stop the daemon use:

```
sudo pigpiod

sudo killall pigpiod
```

The available PWM frequencies depend on the set sample rate ([http://abyz.me.uk/rpi/pigpio/python.html#set\_PWM\_frequency](http://abyz.me.uk/rpi/pigpio/python.html#set_PWM_frequency)). For changing the sample rate see: [http://abyz.me.uk/rpi/pigpio/pigpiod.html](http://abyz.me.uk/rpi/pigpio/pigpiod.html)

### 1-Wire

The temperature sensor (DS18B20) is controlled via the 1-wire protocol on the GPIO BCM 4. This needs to be enabled in the config.txt:

```
sudo nano /boot/config.txt
```

The following line needs to be added and the system rebooted:

```
dtoverlay=w1-gpio,gpiopin=4
```

After reboot, the modules need to be loaded:

```
sudo modprobe w1-gpio pullup=1

sudo modprobe w1-therm
```

and added to /etc/modules by running:

```
sudo nano /etc/modules
```

and adding the lines:

```
w1-gpio pullup=1

w1-therm
```

If this was successful, and the sensor is properly connected it should appear at:

```
/sys/bus/w1/devices/
```

### GPIO serial port

The UART port (GPIO BCM 14) needs to be enabled to allow functioning of the status LED. Therefore, the config file needs to be edited:

```
sudo nano /boot/config.txt
```

and the following line added:

```
enable\_uart=1
```

### Adding the shutdown script to crontab

To run the shutdown\_script.py script, that checks for the shutdown command of the on/off button, after each boot, it needs to be added to crontab. First the script needs to be made executable:

```
sudo chmod 755 shutdown\_script.py
```

Then crontab is started:

```
sudo crontab -e
```

and the following line is added (this executes the script after each boot and puts the logs to the cronlog file)

```
@reboot sudo python3 /home/pi/shutdown_script.py >/home/pi/logs/cronlog 2>&1 &
```

Finally, the folder for the logs is made:

```
mkdir logs
```

## Reactor Dimensions

![Figure 1: Reactor dimensions – view from top.](/schemes_and_circuits/Figure1.jpg "Figure 1: Reactor dimensions – view from top.")

*Figure 1: Reactor dimensions – view from top.*

![Figure 2: Reactor dimensions – photo from top.](/schemes_and_circuits/Figure2.jpg "Figure 2: Reactor dimensions – photo from top.")

*Figure 2: Reactor dimensions – photo from top.*

![Figure 3: Reactor dimensions – side view.](/schemes_and_circuits/Figure3.jpg "Figure 3: Reactor dimensions – side view.")
*Figure 3: Reactor dimensions – side view.*

![Figure 4: Reactor dimensions – view from top, sides A, B and C.](/schemes_and_circuits/Figure4.jpg "Figure 4: Reactor dimensions – view from top, sides A, B and C.")

*Figure 4: Reactor dimensions – view from top, sides A, B and C.*

![Figure 5: Reactor dimensions – electronics box, side A.](/schemes_and_circuits/Figure5.jpg "Figure 5: Reactor dimensions – electronics box, side A.")

*Figure 5: Reactor dimensions – electronics box, side A.*

![Figure 6: Reactor dimensions – photo from side A.](/schemes_and_circuits/Figure6.jpg "Figure 6: Reactor dimensions – photo from side A.")

*Figure 6: Reactor dimensions – photo from side A.*

![Figure 7: Reactor dimensions – electronics box, side B.](/schemes_and_circuits/Figure7.jpg "Figure 7: Reactor dimensions – electronics box, side B.")

*Figure 7: Reactor dimensions – electronics box, side B.*

![Figure 8: Reactor dimensions – photo from side B.](/schemes_and_circuits/Figure8.jpg "Figure 8: Reactor dimensions – photo from side B.")

*Figure 8: Reactor dimensions – photo from side B.*

![Figure 9: Reactor dimensions – electronics box, side C.](/schemes_and_circuits/Figure9.jpg "Figure 9: Reactor dimensions – electronics box, side C.")

*Figure 9: Reactor dimensions – electronics box, side C.*

![Figure 10: Reactor dimensions – photo from side C.](/schemes_and_circuits/Figure10.jpg "Figure 10: Reactor dimensions – photo from side C.")

*Figure 10: Reactor dimensions – photo from side C.*

## Parts List

| **Application** | **Part** | **Number** |
| --- | --- | --- |
| Raspberry Pi | voltage converter for Raspberry Pi power supply (24 V DC to 5V/3A DC, DEBO) | 1 |
| | USB-A to micro-USB cable for Pi power supply | 1 |
| | Raspberry Pi 3B+ (+ SD card and case) | 1 |
| power | 24V Power source \&gt;180W | 1 |
| lighting | 4 channel MOSFET with optocoupler | 1 |
| | high power LED bar 3000 K (Lumitronix) | as needed |
| | high power LED bar 4000 K (Lumitronix) | as needed |
| | high power LED bar 5700 K (Lumitronix) | as needed |
| | high power LED bar 365 nm (Lumitronix) | as needed |
| | high power LED bar 385 nm (Lumitronix) | as needed |
| | high power LED bar 405 nm (Lumitronix) | as needed |
| | high power LED bar 455 nm (Lumitronix) | as needed |
| | high power LED bar 470 nm (Lumitronix) | as needed |
| | high power LED bar 528 nm (Lumitronix) | as needed |
| | high power LED bar 590 nm (Lumitronix) | as needed |
| | high power LED bar 617 nm (Lumitronix) | as needed |
| | high power LED bar 623 nm (Lumitronix) | as needed |
| | high power LED bar 660 nm (Lumitronix) | as needed |
| | high power LED bar 730 nm (Lumitronix) | as needed |
| | high power LED bar 850 nm (Lumitronix) | as needed |
| | cable with 5.5 x 2.1 mm male plug (0.3 m; Delock 85740) | as needed |
| | 700 mA constant current LED driver (MW LDD-700HW) | 8 |
| status LED | low current LED (red, 5mm, 2 MA) | 1 |
| | LED holder (8 mm diameter for 5 mm LED) | 1 |
| | patch panel cover with 8 mm hole (Delock 86403) | 1 |
| | 800 Ohm resistor for LED | 1 |
| internal temperature management | 24V high power fan (24V, 4 cm x 4 cm, PWM controllable; EBM Papst 424J/2HP) | 4 |
| temperature sensor | 4.7 kOhm Resistor for T-sensor | 1 |
| | DS18B20 T-Sensor with cable | 1 |
| patchpanel | 12 port patchpanel (Delock 43259) | 1 |
| | patchpanel module DC 5.5 x 2.1 mm socket (Delock 86355) | 12 |
| | 6 port patchpanel (Delock 86274) | 1 |
| | patchpanel module push-button (Delock 86402) | 1 |
| | USB A to USB A extension (0.15 m) | 1 |
| | HDMI cable (0.25 m) | 1 |
| | patchpanel module HDMI type A \&gt; HDMI type A (KS EB520V2 Keystone) | 1 |
| | short patch (LAN) cable (0.15 m) | 1 |
| | Raspberry Pi microSD extension (0.15 m) | 1 |
| | patchpanel cover (Delock 86314) | 1 |
| | patchpanel module USB type A female \&gt; type A female | 1 |
| | gender changer USB-A male - USB-A male | 1 |
| | patchpanel module RJ45 socket \&gt; RJ45 socket (DELOCK 86204 ) | 1 |
| cables, miscellaneous | cable 1.5 mm2 red | 1 |
| | cable 1.5 mm2 black | 1 |
| | 2-conductor connection terminal | as needed |
| | 3-conductor connection terminal | as needed |
| | 5-conductor connection terminal | as needed |
| | shrinking tube (3:1, 3 mm) | 1 |
| | shrinking tube (3:1, 6 mm) | 1 |
| | twin cable 1.5 mm2 | 1 |
| | twin cable 0.15 mm2 | 1 |
| | cord switch | 1 |
| | switch | 1 |
| | jumper cable set for GPIO (10 cm) | 1 |
| | jumper cable set for GPIO (20 cm) | 1 |
| | 2-component glue | 1 |
| electronics case and LED mount | reactor construction material (screws, plates, passive coolers) | 1 |
| shaking | benchtop shaker (VWR 444-0268) | 1 |
| external temperature management | incubator (Aqualytic TC 135 S) | if needed |

## Electronics

The breadboard scheme of the electronics is below and can be downloaded [here](/schemes_and_circuits/breadboard_scheme.pdf). The circuits are [here](/schemes_and_circuits/circuit_diagram.pdf).

![Figure 11: Electronics.](/schemes_and_circuits/breadboard_scheme.png "Figure 11: Electronics.")

*Figure 11: Electronics.*

In the following the different systems are shortly described:

The power is from a 24 V power supply (close to 180 W are required if the reactor runs at full power). The 24 V are converted to 5 V to supply the Raspberry Pi using a voltage converter.

An on/off button is connected to the GPIO BCM 3 and to the ground.

A status LED is connected to the serial port GPIO BCM 14 and to the ground.

The temperature sensor (DS18B20) is connected to GPIO BCM 4, to the ground and to a 3.3 V pin. The temperature data is then used to calculate the appropriate rotation speed of the cooling fans via an PI(D)-controller script.

The fan speed is controlled via hardware based PWM (25 MHZ) from the GPIO BCM 18 (PWM0). The fans (Pabst 424 JH, 24V DC) are further connected to the 24 V power supply and the ground.

Constant current for channels 1-8 is provided via constant current sources (MW LDD-700HW) that are connected to the 24 V power supply and the ground and controlled directly by the eight GPIOs (BCM numbers: 24, 10, 9, 25, 11, 8, 7, 5) according to the scheme.

Constant voltage for channels 9-12 is provided via a 4 channel MOSFET with optocoupler (IRF540 MOSFETS), that is connected to the 24 V power supply and the ground and are controlled directly by the four GPIOs (BCM numbers: 17, 27, 22, 23) according to the scheme.

For better usability, the current to the fans and the light sources can be interrupted using a switch.

## Python Scripts

Three scripts are required:

The python script to run the reactions is set up in two different files. [**&quot;reactor\_programm.py&quot;**](/reactor_programm.py).
 containing the program code and [**&quot;start\_experiment.py&quot;**](/start_experiment.py) which is used to set all the parameters for a given experiment. When the parameters in [**&quot;start\_experiment.py&quot;**](/start_experiment.py) were set using a text editor, e.g.:

```
nano start_experiment.py
```

and saved, the experiment can be started as follows:

```
python3 start_experiment.py
```

Throughout the experiment all parameters are printed to the console and logged in CSV logging file.

A third script [**&quot;shutdown\_script.py&quot;**](/shutdown_script.py) is started after any boot and checks the status of the on/off switch. If the switch is pressed for 5 sec, the Raspberry Pi shuts down and all GPIO are put to their standard state.

## Usage

For the usage and tuning as well as characterization of the illumination conditions as well as the temperature distribution see the publication below. In the paper also a selection of different photo(bio)catalytic reactions are presented.

## Credits (Paper)

Please cite the following paper:

*Accelerated Reaction Engineering of Photo(bio)catalytic Reactions through Parallelization with an Open-Source Photoreactor; Christoph K. Winkler, Stefan Simić, Valentina Jurkaš, Sarah Bierbaumer, Luca Schmermund, Silvan Poschenrieder, Sarah Berger, Elisa Kulterer, Robert Kourist and Wolfgang Kroutil; 2021; (submitted)*

## License

The photoreactor designs and scripts are provided as [Open Source Hardware](https://www.oshwa.org/definition/) under a [Creative Commons Attribution, Share-Alike (BY-SA)](http://creativecommons.org/licenses/by-sa/3.0/) license (see below).

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Open Source Photoreactor for Parallel Evaluation of Small-Scale Reactions</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/stoeffel85/photoreactor" property="cc:attributionName" rel="cc:attributionURL">Christoph Winkler and Wolfgang Kroutil</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.<br />Permissions beyond the scope of this license may be available at <a xmlns:cc="http://creativecommons.org/ns#" href="http://biocatalysis.uni-graz.at" rel="cc:morePermissions">http://biocatalysis.uni-graz.at</a>
