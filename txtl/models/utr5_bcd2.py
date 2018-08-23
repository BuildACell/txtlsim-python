# utr5_bcd1.py -  BCD1 ribosome binding site
# RMM, 12 Aug 2018
#
# This file contains the model for the BCD1 ribosome binding site
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

from ..dna import UTR5

class UTR5_bcd2(UTR5):
    def update_species(self, model, mechanism, parameters={}):
        print("updating species for ", self.name)
