# ctag_lva.py -  LVA ssrA degradation tag
# RMM, 12 Aug 2018
#
# This file contains the model for the LVA ssrA degradation tag
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

from ..dna import Ctag

class Ctag_lva(Ctag):
    def update_species(self, assy, model):
        print("updating species for ", self.name)
