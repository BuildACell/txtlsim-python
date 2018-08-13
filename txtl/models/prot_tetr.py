# prot_tetr.py -  tetR protein definition
# RMM, 11 Aug 2018
#
# This file contains the model for the deGFP protein.
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

from ..dna import ProteinCDS

class Prot_tetr(ProteinCDS):
    def update_species(self, model):
        print("updating species for ", self.name)
