import settings
import AirSimClient as airsim

import os, sys
import json
from game_config import GameConfigHandler

class EnvRandomizer():
    def __init__(self):
        self.game_config_handler = GameConfigHandler()
        self.cur_zone_number_buff = 0

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
        time.sleep(5)

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
        client = self.airsim_client
        client.resetUnreal(20)
        client.confirmConnection()
        client.enableApiControl(True)
        client.armDisarm(True)

    def get_airsim_client(self):
        return self.airsim_client
