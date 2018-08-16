# mechanisms.py - mechanism class for implementing TX-TL mechanisms
# RMM, 16 Aug 2018
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

from .sbmlutil import add_species, add_reaction

# Mechanism class for core mechanisms
class Mechanism:
    """Mechanism class

    The Mechanism class is used to impelement different core
    mechanisms in TX-TL.  All specific core mechanisms should be
    derived from this class.

    """
    def __init__(self):
        return None

