# component.py - component class for implementing TX-TL components
# RMM, 16 Aug 2018
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

from .sbmlutil import add_species, add_reaction
from warnings import warn

# Component class for core components
class Component:
    """Component class

    The Component class is used to impelement different core
    components in TX-TL.  All specific core components should be
    derived from this class.

    Data attributes
    ---------------
    mechanisms          Mechanism dictionary
    config_file         Configuration file (str)
    parameters          Parameter dictionary

    Required member functions
    -------------------------
    update_species()    create the species used by this component
    read_config_file()  read parameter values from configuration file
    write_config_file() write parametr value to configuration file

    """
    def __init__(self, name, config_file=None, mechanisms={}):
        warn("component: default __init__ called for " + name)
        return None

    #! TODO: think about argument order
    def update_species(self, model, mechanisms={}, parameters={}):
        warn("component: default __init__ called for " + name)

    def update_reactions(self, model, mechanisms={}, parameters={}):
        warn("component: default __init__ called for " + name)
