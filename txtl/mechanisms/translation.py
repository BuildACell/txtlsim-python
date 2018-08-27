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

class basic(Mechanism):
    "Basic translation mechanism"
    def update_reactions(self, mixture, assy, debug=False):
        parameters = assy.utr5.parameters       # get parameter values

        # Create reaction that binds Ribo to RNA
        add_reaction(mixture,
                     [mixture.ribo, assy.rna], [assy.ribo_bound], 
                     kf = parameters['Ribosome_Binding_F'],
                     kr = parameters['Ribosome_Binding_R'],
                     prefix="tlb_")

        # Figure out the translation rate based on length of the protein
        tlrate = eval_parameter(
            mixture, 'Translation_Rate', {'Protein_Length' : assy.cds.length})
        tlparam = Parameter('TL_Rate', 'Numeric', tlrate)
                                          
        if debug:
            print("Translation rate for RBS %s of length %d = " %
                  (assy.utr5.name, assy.peplength), tlrate)

        # Create reaction that produces protein
        add_reaction(mixture, [assy.ribo_bound],
                     [mixture.ribo, assy.rna, assy.protein],
                     kf = tlparam, prefix="tlb_")
