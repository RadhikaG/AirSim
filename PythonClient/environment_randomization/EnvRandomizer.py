import roborun_settings
import AirSimClient as airsim

import os, sys
import json
from game_config import AirlearningGameConfigHandler

class EnvRandomizer():
    def __init__(self):
        self.game_config_handler = AirlearningGameConfigHandler()
        self.cur_zone_number_buff = 0
        # tracks number of times randomized till now
        self.episodeN = 0

        self.airsim_client = airsim.MultirotorClient(ip="127.0.0.1")
        client = self.airsim_client
        client.confirmConnection()
        client.enableApiControl(True)
        client.armDisarm(True)

    def setConfigHandlerRange(self, range_dic):
        self.game_config_handler.set_range(*[el for el in range_dic.items()])
        self.game_config_handler.populate_zones()

    def init_again(self, range_dic): #need this cause we can't pass arguments to
                                     # the main init function easily
        self.game_config_handler.set_range(*[el for el in range_dic.items()])
        self.game_config_handler.populate_zones()
        self.sampleGameConfig()
    
    def setRangeAndSampleAndReset(self, range_dic):
        self.game_config_handler.set_range(*[el for el in range_dic.items()])
        self.game_config_handler.populate_zones()
        self.sampleGameConfig()
        self.airsim_reset()

    def ease_randomization(self):
        for k, v in settings.environment_change_frequency.items():
            settings.environment_change_frequency[k] += settings.ease_constant

    def tight_randomization(self):
        for k, v in settings.environment_change_frequency.items():
            settings.environment_change_frequency[k] = max(
                settings.environment_change_frequency[k] - settings.ease_constant, 1)

    def randomize_env(self):
        vars_to_randomize = []
        for k, v in settings.environment_change_frequency.items():
            if (self.episodeN+1) %  v == 0:
                vars_to_randomize.append(k)

        if (len(vars_to_randomize) > 0):
            self.sampleGameConfig(*vars_to_randomize)
            print("Randomizing env...")

    def updateJson(self, *args):
        self.game_config_handler.update_json(*args)

    def getItemCurGameConfig(self, key):
        return self.game_config_handler.get_cur_item(key)

    def setRangeGameConfig(self, *args):
        self.game_config_handler.set_range(*args)

    def getRangeGameConfig(self, key):
        return self.game_config_handler.get_range(key)

    def sampleGameConfig(self, *arg):
        self.game_config_handler.sample(*arg)

    def airsim_reset(self):
        self.airsim_client = self.airsim_client.resetUnreal(5)

        client = self.airsim_client
        client.confirmConnection()
        client.enableApiControl(True)
        client.armDisarm(True)

        self.episodeN += 1

        return self.airsim_client

    def get_airsim_client(self):
        return self.airsim_client

    def init_difficulty_level(self, difficulty_level):
        #print("EnvRandomizer: " + difficulty_level)
        self.init_again(eval("settings." + difficulty_level + "_range_dic"))
