# mechanism.py - mechanism class for implementing TX-TL mechanisms
# RMM, 16 Aug 2018
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

# Mechanism class for core mechanisms
class Mechanism:
    """Mechanism class

    The Mechanism class is used to impelement different core
    mechanisms in TX-TL.  All specific core mechanisms should be
    derived from this class.

    """
    def __init__(self): return None
    def update_species(self, model, component, mechanisms,
                       parameters={}): return None
    def update_reactions(self, model, component, mechanisms,
                         parameters={}): return None
