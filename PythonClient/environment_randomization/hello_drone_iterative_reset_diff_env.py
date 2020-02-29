import settings 
import AirSimClient as airsim

import numpy as np
import os
import tempfile
import pprint
import time
from EnvRandomizer import EnvRandomizer

env_rand = EnvRandomizer()

client = env_rand.get_airsim_client()

airsim.AirSimClientBase.wait_key('Press any key to start')

x = 0
try:
    while (1):
        x += 1
        env_rand.randomize_env()
        print("Resetting...")
        client = env_rand.airsim_reset()
        print("Done reset")
        state = client.getMultirotorState()
        s = pprint.pformat(state)
        print("state: %s" % s)
        airsim.AirSimClientBase.wait_key('Press any key to move')
        client.moveByVelocity(0, 0, -2, 2, drivetrain=0)
        airsim.AirSimClientBase.wait_key('Press any key to randomize')

        if x == 3:
            env_rand.init_difficulty_level("medium")
        if x == 6:
            env_rand.init_difficulty_level("hard")

        env_rand.tight_randomization()

except(KeyboardInterrupt):
    pass

exit(0)
