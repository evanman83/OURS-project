# OURS Project - DIY Open-Source Linux Smartphone

## MISSION:

I wanted to give people more options and control over their most personal device, so I created an **O**pen-source, **U**pgradable, **R**epairable **S**martphone, that is also completely free of Big Tech. It's not theirs, it's O.U.R.S. 

Below are the complete hardware and software instructions to build your own OURphone. Please enjoy, upgrade, tinker, improve and evolve my original design as you see fit, and share your upgrades here. Find me on [LinkedIn](https://www.linkedin.com/in/boyofthefuture/) if you have any questions / ideas.

Want to work together on version 2? Join us on our [Telegram group](https://t.me/ourphonechat).

<img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_1454.JPG" width="400" /> <img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_1453.JPG" width="400" />

<img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_20230501_111658.jpg" height="180" /> <img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_20230501_111903.jpg" height="180" /> <img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_20230501_112025.jpg" height="180" /> <img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_20230501_112237.jpg" height="180" /> <img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_20230501_114113.jpg" height="180" /> <img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_20230501_114557.jpg" height="180" /> <img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_20230501_115055.jpg" height="180" />

## SPECS LIST

- 4G LTE internet
- Call, SMS, Contacts book (contains a SIM7600 with sim card)
- Quad Core 1.2GHz Broadcom BCM2837 64bit CPU
- 1 GB RAM
- Running Raspbian - a Debian Linux OS with installable app store
- Capable of running Facebook, WhatsApp, YouTube etc in browser
- 4 inch 480 x 800 colour touch screen
- 5MP colour camera
- GPS (in browser)
- Wifi
- Bluetooth audio
- 1 watt onboard audio speaker
- 3 USB ports
- "Convergent": HDMI port to plug in external monitor, USB to plug in keyboard and mouse
- Screen lock switch
- 9cm x 16cm x 3cm
- 5 hours battery life

<img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_1455.JPG" width="400" /> <img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_1460.JPG" width="400" />
<img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_1458.JPG" width="400" /> <img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_1461.JPG" width="400" />


## HOW IT WORKS
The Raspberry Pi provides the basic functions of a computer, now made portable by the two 3.6v batteries, down-converted to 5.1V DC. Telephony (calls and SMS) is made possibly via the Waveshare 4G HAT with a normal mobile network SIM card contained therein. The Pi communicates with the 4G HAT via ordinary AT commands. The startup.sh script runs the configuration necessary to activate a 4G mobile internet connection. The phone.py app provides a UI for dialling and calling, sending, receiving and replying to SMS, adding and removing records from a simple Address Book. The built-in microphone and speaker allow normal voice calls.


## GUIDING PRINCIPLES

- Low cost, off-the-shelf electronic components
- Less soldering / destroying, more connecting / assembling
- Share everything required to replicate
- Modular, standardised parts
- Browser-based PWAs are the future of installable apps

<img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_20230125_102156.jpg" width="400" />


## IMPROVEMENTS TO MAKE

- Use a faster Raspberry Pi with more RAM, or another SBC, or the super small RPi 4 Compute Module
- Use a capacitative touch screen, not resistive touch
- A bigger screen would be nice
- Eliminate audio whining / cracking (I think this is an RPi 3 problem, or audio amp needs isolation)
- Use shielded cables for audio carrying wires
- Add a microphone / USB audio card to enable audio on video recordings
- Connect phone call audio into Bluetooth (not just device audio)
- Audio jack
- Make less brick-like
- Customise Raspbian so the UI is more usable by finger (perhaps flash another OS)
- Detect and display remaining battery life
- Extend battery life, perhaps convert DC voltage UP instead of DOWN, or down-clock the RPi CPU temporarily


## HOW TO BUILD

Buy all the parts in *parts-list.xls*. Connect them based on *schematic.ppt*.

You can snap together a working version quite quickly with just the following (no soldering required):
- Raspberry Pi
- 4G HAT + GSM and GPS antennas
- Raspberry Pi power supply
- Waveshare touchscreen
- Raspberry Pi camera (optional)
- Headphones with built-in mic
- Some USB cables
- Operational mobile phone SIM card with airtime and data

Copy the files below into the Raspberry Pi home directory:
- startup.sh (auto-start script to turn on internet)
- phone.py (the app that allows calls, SMS, Contacts)
- location-provider.py (presents stored GPS coordinates at a URL for web-based location providers)
- ringtone.wav (your phone's ringtone - replace as you wish!)
- mobile-keyboard.xml (a custom keyboard based on the match keyboard software)

Follow the instructions listed in *setup_commands.txt* to ready the Raspberry Pi, setup internet, and get the phone.py app working.


### Making the cables smaller
There are many USB and audio plugs being used in the project. These are too big to allow packaging the phone's components into the wooden phone cover (box) designed for it. To make these smaller, I used thin wire to make new cables, with custom plugs on the ends. I made the plugs by using radically stripped down versions of the male plugs, taking off extra plastic housing, grinding off unnecessary bits and even bending some parts at right angles. Then I soldered on new leads and covered it with hot glue so that they are robust enough to force into tight spaces.

<img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_20230429_123637.jpg" height="400" /> <img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_20230429_123650.jpg" height="400" />

To save even more space I soldered USB connections directly to the back side of the Raspberry Pi. This was the plug going to the 4G HAT.

<img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_20230215_225042.jpg" width="400" />


### Making the Waveshare 4G HAT smaller
This is a challenge because the 4G HAT sits in between the touch screen and the Raspberry Pi itself. It is a tight, tight squeeze. I used a combination of a Dremel tool (small rotary grinder) and miniature steel cutters to painstakingly cut off the large USB ports and the two thick metal pins. These proved useless for carrying USB data, so I couldn't use them anyway - only the micro USB port seemed to work (despite many messages to their Customer Support). Be EXTREMELY careful removing these big items because it is very easy to cause massive physical destruction by lifting a track off the PCB, and then your module (the most expensive part of the build) is dead and unusable :( Only attempt if you have a surgeon's hand.

<img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_20230215_224848.jpg" width="400" />

Once these items are removed and the whole device is now slim, I hot glued the GSM and GPS antenna plugs and wires in place so they are not so fragile, and wrapped the whole thing in insulation tape.

<img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_20230218_202118.jpg" height="400" /> <img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_20230429_123734.jpg" height="400" /> 

The GSM antenna provided is too big. So I purchased a PCB GSM antenna and soldered that onto the cable instead. It works ok, but signal is never 100%, only good-ish.

The GPS antenna is also too big. So I crushed it slowly in a clamp and used a screwdriver to prise off the plastic casing. This revealed a much smaller GSM antenna chip, like a hard metal square. I soldered this onto the cable instead and replaced the whole plug system with just one little neat cable.

<img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_20230215_224147.jpg" width="400" /> 


### Laser cut the phone cover ###

Email the file *laser-cut-cover.dxf* to your nearest laser cutting facility. Use 3mm MDF board - that is what the design has been made to use. You won't be able to use a thinner board without modifying the design.

You can also 3D print all the parts, here's the link : https://www.thingiverse.com/thing:6063147

<img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_20230215_173732.jpg" width="400" />


### Assembly and construction
This is best described with pictures, but the main steps are:

1. Make new male plugs for the micro USB and male 3.5mm TRRS / stereo plugs (as described above).
2. Solder all the wires for the charger, power switch and power supply. Set the DC/DC converter to 5.1 VDC. Charge the batteries up for the first time, with the power switch in OFF / charging mode. Test whether the system can boot up and connect to the web - outbound calls and internet use a lot of current / make current spikes.
3. Solder in the audio amp, speaker and volume knob. Play a test mp3 (I downloaded the RhythymBox app) and see how loud it plays over the speaker.
4. Solder in the relay and screen lock switch. When the phone app is running, switching the screen lock switch should turn off the LCD screen and disable the touch controls. When a phone call begins, the relay should switch off the default Raspberry Pi audio and instead connect the phone call audio to the loudspeaker.
5. Connect all the batteries, wires and plugs and test: Internet, phone call, SMS, GPS, music playing. There is a lot of guidance for troubleshooting in the file setup_commands.txt (provided above).
6. Insert the 4G HAT between the touchscreen and Raspberry Pi, with audio and power cables pointing out the bottom right hand corner of the screen (facing the screen).
7. Fold the camera ribbon cable under the 4G HAT and over and under the batteries - stick the camera in place with Prestick putty. (this system was annoying because every time I needed to remove the electronics from the cover I had to unwrap the camera - rather implement some kind of snap plug for the ribbon cable to make this easier)
8. Stick the speaker with putty over the top right-hand grill (9 holes).
9. Place the GPS antenna next to the top left-hand grill (9 holes). GSM antenna can go down the left-hand side of the cover.
10. Start glueing the case together, starting from the bottom upwards, finishing with the front cover.

<img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_20230217_234640.jpg" height="400" /> <img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_20230311_210201.jpg" height="400" /> <img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_20230429_123553.jpg" height="400" /> <img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_20230429_123617.jpg" height="400" /> <img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_20230429_123708.jpg" height="400" /> <img src="https://github.com/evanman83/OURS-project/blob/main/photos/IMG_20230429_130914.jpg" height="400" />

See more construction photos in the /photos folder.


© Evan Robinson, 2023
