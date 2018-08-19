# pathutil.py - path utilities
# RMM, 16 Aug 2018
#
# This file contains some utility functions for manipulating and using
# paths for finding models and configuration files.
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

# Load a model from a file
def load_model(prefix, name, length):
    # Look to see if we have a model for this component
    #! Expand this to look in other locations
    try:
        from importlib import import_module
        module = import_module("txtl.models.%s_%s" %
                               (prefix.lower(), name.lower()))
        model = eval("module.%s_%s('%s', %d)" %
                     (prefix, name.lower(), name, length))
    except:
        raise ValueError("couldn't find model %s_%s" % (prefix, name))

    return model
