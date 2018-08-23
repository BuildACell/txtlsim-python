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
            self.value = float(value)           # store as float
        elif type.strip() == 'Expression':
            self.value = value;                 # store as string
        else:
            raise TypeError("can't parse value of parameter %s" % name)
        
    def get_value(self):
        return float(self.value)

def load_config(name, extension=".csv", debug=False):
    # Find the configuration file
    #! TODO: update this to search along a path (in pathutil)
    module_path = os.path.dirname(sys.modules[__name__].__file__)    

    # Look for the config file in a list of paths
    csvfile = None
    for path in (module_path + "/models/", module_path + "/config/"):
        try:
            filename = path + name + extension
            csvfile = open(filename)
            break
        except:
            continue

    # If we didn't find the file, return None
    if csvfile == None: return None

    # Open up the CSV file for reaching
    csvreader = csv.reader(csvfile)
    params = {}
    for row in csvreader:
        # Skip blank lines
        if row[0].strip() == "": continue
        
        # Create a new parameter object to keep track of this row
        #                   name    type    value   comment
        param = ConfigParam(row[0], row[1], row[2], row[3])

        # Set up as dictionary for easy access
        params[param.name] = param

    return params

def eval_parameter(param, parameters):
    # See if we already have a floating point number
    if isinstance(param.value, (float, int)): return float(param.value)

    #! TODO: evaluate the expression using `parameters` as a dictionary

    return eval(param.value)
