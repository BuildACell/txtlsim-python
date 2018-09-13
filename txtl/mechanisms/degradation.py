# degradation.py - TX-TL degradation mechanisms
# RMM, 26 Aug 2018
#
# This file contains the standard degradation mechanisms (DNA, RNA and
# protein) that are distributed with the txtl toolbox.
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

from ..mechanism import Mechanism
from ..sbmlutil import add_species, add_reaction

class dna_basic(Mechanism):
    "Basic DNA degradation"
    def __init__(self):
        self.name = 'Basic DNA degradation'

    #! TODO: not implemented

class rna_basic(Mechanism):
    "Basic RNA degradation"
    def __init__(self):
        self.name = 'Basic RNA degradation'

    def update_reactions(self, mixture, assy):
        parameters = mixture.parameters         # get parameter values
        add_reaction(mixture, [assy.rna], [], kf=parameters['RNA_deg'],
                     prefix="degradation_rna_basic_")

class protein_basic(Mechanism):
    "Basic protein degradation"
    def __init__(self):
        self.name = 'Basic protein degradation'
    #! TODO: not implemented

    
