import settings 
import AirSimClient as airsim

import numpy as np
import os
import tempfile
import pprint
import time
from game_config_manipulator_class import *
import EnvRandomizer

env_rand = EnvRandomizer()
client = env_rand.get_airsim_client()

airsim.AirSimClientBase.wait_key('Press any key to start')

x = 0
try:
    while (1):
        x += 1
        env_rand.randomize_env()
        state = client.getMultirotorState()
        s = pprint.pformat(state)
        print("state: %s" % s)
        airsim.AirSimClientBase.wait_key('Press any key to move')
        client.moveByVelocity(0, 0, -2, 2, drivetrain=0)
        airsim.AirSimClientBase.wait_key('Press any key to randomize')

except(KeyboardInterrupt):
    pass

exit(0)
