# component.py - component class for implementing TX-TL components
# RMM, 16 Aug 2018
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

from .sbmlutil import add_species, add_reaction

# Component class for core components
class Component:
    """Component class

    The Component class is used to impelement different core
    components in TX-TL.  All specific core components should be
    derived from this class.

    Data attributes
    ---------------
    mechanisms          Mechanism dictionary

    Required member functions
    -------------------------
    update_species()    create the species used by this component

    """
    def __init__(self):
        return None
