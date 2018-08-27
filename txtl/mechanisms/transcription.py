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
from ..parameter import Parameter, eval_parameter

# Convert DNA to RNA
class basic(Mechanism):
    "Basic transcription mechanism"
    def update_reactions(self, mixture, assy, debug=False):
        parameters = assy.promoter.parameters   # get parameter values
        
        # Figure out the reaction rates
        kf = parameters['RNAPbound_F']
        kr = parameters['RNAPbound_R']
        
        # Create reaction that binds RNAP to DNA
        add_reaction(mixture, [mixture.rnap, assy.dna], [assy.rnap_bound],
                     kf, kr, prefix="txb_")

        # Figure out the transcription rate based on length of the protein
        txrate = eval_parameter(
            mixture, 'Transcription_Rate', {'RNA_Length' : assy.rnalength})
        txparam = Parameter('TX_Rate', 'Numeric', txrate)

        if debug:
            print("Transcription rate for RNA %s of length %d = " %
                  (assy.utr5.name, assy.rnalength), transcription_rate)

        # Create reaction that produces mRNA
        add_reaction(mixture, [assy.rnap_bound],
                     [mixture.rnap, assy.rna, assy.dna],
                     kf=txparam, prefix="txb_")
