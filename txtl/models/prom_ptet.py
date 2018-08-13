# prom_ptet.py - ptet promoter definition
# RMM, 11 Aug 2018
#
# This file contains the model for the ptet promoter. 
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

from ..dna import RepressedPromoter

class Prom_ptet(RepressedPromoter):
    "ptet promoter"
    def __init__(self, name, length):
        RepressedPromoter.__init__(self, name, 'tetR', dimer=True)
