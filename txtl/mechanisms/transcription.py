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

# Convert DNA to RNA
class basic(Mechanism):
    "Basic transcription mechanism"
    def update_reactions(self, mixture, assy, debug=False):
        parameters = assy.promoter.parameters   # get parameter values
        
        # Figure out the reaction rates
        kf = parameters['RNAPbound_Forward']
        kr = parameters['RNAPbound_Reverse']
        
        # Create reaction that binds RNAP to DNA
        add_reaction(mixture, [mixture.rnap, assy.dna], [assy.rnap_bound],
                     kf, kr)

        # Create reaction that produces mRNA
        #! TODO: figure out correct reaction rate
        if debug: print("dna2rna_basic: produce mRNA")
        add_reaction(mixture, [assy.rnap_bound],
                     [mixture.rnap, assy.rna, assy.dna], kf=1)
        
