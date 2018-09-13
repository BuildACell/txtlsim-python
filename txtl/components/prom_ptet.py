# prom_ptet.py - ptet promoter definition
# RMM, 11 Aug 2018
#
# This file contains the model for the ptet promoter. 
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

from ..dna import RepressedPromoter

class prom_ptet(RepressedPromoter):
    "ptet promoter"
    def __init__(
        self, name='ptet', length=50,
        mechanisms={}, config_file='prom_ptet.csv', parameters={},
        rnapname="RNAP", **keywords
    ):
        RepressedPromoter.__init__(
            self, name=name, repressor='tetR', length=length,
            mechanisms=mechanisms, config_file=config_file,
            parameters=parameters, rnapname=rnapname, dimer=True, **keywords)

# Define a shorthand version for convenience
ptet = prom_ptet
