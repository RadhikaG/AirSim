import os 
from os import sys
import json 

class GameConfig:
    def __init__(self, input_file_addr):
        assert(os.path.isfile(input_file_addr)), input_file_addr + " doesnt exist"
        self.input_file_addr = input_file_addr 
        self.input_file_addr = input_file_addr #input file to parse
        self.populate();

    def populate(self):
        if not(os.path.isfile(self.input_file_addr)):
            print("file:" + self.input_file_addr+ " doesn't exist")
            sys.exit()
        with open(self.input_file_addr) as data_file:
            jstring = data_file.read().replace('nan', 'NaN')
            data = json.loads(jstring)
            self.config_data = data
   
    def find_all_keys_helper(self, in_val):
        #print in_val 
        if type(in_val) is list:
            res= map(lambda x: self.find_all_keys_helper(x), in_val)
            return sum(res,[]) #flattening the list
        if type(in_val) is dict:
            res = map(lambda x: [x] + self.find_all_keys_helper(in_val[x]), in_val)
            return sum(res,[]) #flattening the list
        return []  

    def find_all_keys(self):
        return self.find_all_keys_helper(self.get())
    
    def set_item_helper(self, in_val, key_to_compare,new_value):
        if type(in_val) is list:
            res = [] 
            for el in in_val:
                res.append(self.set_item_helper(el, key_to_compare, new_value))
        elif type(in_val) is dict:
            res = {} 
            for el in in_val:
                if (el == key_to_compare):
                    res[el] = new_value
                else: 
                   res[el] = self.set_item_helper(in_val[el], key_to_compare, new_value)
        else:
            res = in_val 
        return res
        
    def set_item(self, key_to_compare, new_value):
        self.config_data = self.set_item_helper(self.get(), key_to_compare, new_value)

    def get_item_helper(self, in_val, key_to_compare):
        res = [] 
        if type(in_val) is list:
            for el in in_val:
                res+=self.get_item_helper(el, key_to_compare)
        elif type(in_val) is dict:
            for el in in_val:
                if (el == key_to_compare):
                    res+=[in_val[el]]
                else: 
                   res += self.get_item_helper(in_val[el], key_to_compare)
        return res
        
    def get_item(self, key_to_compare):
        return self.get_item_helper(self.get(), key_to_compare)[0]

    def get(self):
        return self.config_data;
    
    
