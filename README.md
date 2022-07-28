# grandturismo-srs-proxy

This app is a proxy to collects telemetry from the Grand Turismo Series (GT Sport and GT7) 
and send to the Sim Racing Studio API (https://gitlab.com/simracingstudio/srsapi/).

We can now finally use Wind Simulators, Shakers, Leds, Rumble and Motion platforms from
DOFReality, ProSimu, PT-Actuator, SFX-100 (With Thanos Controller) and YawVR

All the credits go to Nenkai to that was able to figure out how to decrypt the telemetry
packets from the game:
https://github.com/Nenkai/PDTools/tree/master/PDTools.SimulatorInterface
I encourage you to donate for him!

To run the script you need python 3.9 installed.
Then you just execute as the following
python main.py --playstation_ip 192.168.0.89

The script pulls the data all the time, but only sends to SRS when the car is on the track and 
the game is not in pause menu, I have added this for safety.

Please note that I am not affiliated to SimRacingStudio and I am not responsible for 
any damage that this could case to you or your equipment

Keep in mind that this is an undocumented API from Grand Turismo Series, the game developer
might patch the game and close the door in the future.

Enjoy!

![alt text](https://raw.githubusercontent.com/gt7coder/grandturismo-srs-proxy/main/imgs/srs_screenshot.png)
