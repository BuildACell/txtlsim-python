# config.py - read and write configuration files
# RMM, 19 Aug 2018
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

import csv
import os
import sys

class ConfigParam:
    def __init__(self, name, type, value, comment, debug=False):
        self.name = name.strip()
        self.type = type.strip()
        self.comment = comment.strip()

        # Set the value of the parameter
        if debug: print("%s [%s] = %s" % (self.name, self.type, value))
        if type.strip() == 'Numeric':
            self.value = float(value)
        elif type.strip() == 'Expression':
            self.value = eval(value)
        else:
            raise TypeError("can't parse value of parameter %s" % name)
        
    def get_value(self):
        return float(self.value)

def load_config(name, extension=".csv"):
    # Find the configuration file
    #! TODO: update this to search along a path (in pathutil)
    path = os.path.dirname(sys.modules[__name__].__file__)    
    
    csvfile = open(path + "/config/" + name + extension)
    csvreader = csv.reader(csvfile)
    params = {}
    for row in csvreader:
        # Skip blank lines
        if row[0].strip() == "": continue
        
        # Create a new parameter object to keep track of this row
        param = ConfigParam(row[0], row[1], row[2], row[3])

        # Set up as dictionary for easy access
        params[param.name] = param

    return params
