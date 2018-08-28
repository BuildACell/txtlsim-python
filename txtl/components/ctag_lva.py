# ctag_lva.py -  LVA ssrA degradation tag
# RMM, 12 Aug 2018
#
# This file contains the model for the LVA ssrA degradation tag.  It
# is a wrapper around the DegradationTag DNA element.  The parameter
# defining the degradation rate and other properties are contained in
# `ctag_lva.csv`.
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

from ..dna import DegradationTag

class ctag_lva(DegradationTag):
    "LVA degradation tag"

# Define a shorthand version for convenience
lva = ctag_lva

    
