import setup 
import AirSimClient as airsim

import numpy as np
import os
import tempfile
import pprint
import time
from game_config_manipulator_class import *

# connect to the AirSim simulator
client = airsim.MultirotorClient(host_ip_addr)
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

airsim.AirSimClientBase.wait_key('Press any key to start')

game_config_manipulator = GameConfigManipulator() 

x = 0
try:
    x += 1
    game_config_manipulator.set(("NumberOfObjects", 7*x))
    client = client.resetUnreal(7)#.3, .5);
    state = client.getMultirotorState()
    s = pprint.pformat(state)
    print("state: %s" % s)
    airsim.AirSimClientBase.wait_key('Press any key to move')
    client.moveByVelocity(0, 0, -2, 2, drivetrain=0)
    airsim.AirSimClientBase.wait_key('Press any key to randomize')

except(KeyboardInterrupt):
    pass

exit(0)
