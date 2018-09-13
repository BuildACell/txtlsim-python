# maturation.py - TX-TL maturation mechanisms
# RMM, 26 Aug 2018
#
# This file contains the standard protein maturation mechanisms that are
# distributed with the txtl toolbox.
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

from ..mechanism import Mechanism
from ..sbmlutil import add_species, add_reaction

class protein_basic(Mechanism):
    "Basic protein maturation"
    def __init__(self):
        self.name = 'Basic protein maturation'

    def update_reactions(self, mixture, assy, debug=False):
        #! TODO: See if this protein is subject to maturation
        #! TODO: Create maturation reaction
        return None
