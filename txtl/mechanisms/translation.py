# transcription.py - TX-TL transcription mechanisms
# RMM, 26 Aug 2018
#
# This file contains the standard transcriptional mechanisms that are
# distributed with the txtl toolbox.
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

from ..mechanism import Mechanism
from ..sbmlutil import add_species, add_reaction

class basic(Mechanism):
    "Basic translation mechanism"
    def update_reactions(self, mixture, assy, debug=False):
        parameters = assy.utr5.parameters       # get parameter values

        # Create reaction that binds Ribo to RNA
        add_reaction(mixture,
                     [mixture.ribo, assy.rna], [assy.ribo_bound], 
                     kf = parameters['Ribosome_Binding_F'],
                     kr = parameters['Ribosome_Binding_R'])

        # Create reaction that produces protein
        #! TODO: figure out correct reaction rate
        if debug: print("dna2rna_basic: produce mRNA")
        add_reaction(mixture, [assy.ribo_bound],
                     [mixture.ribo, assy.rna, assy.protein],
                     kf=1)

        # RNA degradation
        #! TODO: include this as a submechanism to allow enzymatic action
        #! TODO: figure out correct reaction rate
        add_reaction(mixture, [assy.rna], [], kf=1)
