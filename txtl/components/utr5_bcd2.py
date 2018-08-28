# utr5_bcd1.py -  BCD1 ribosome binding site
# RMM, 12 Aug 2018
#
# This file contains the model for the BCD2 ribosome binding site.  It
# is a wrapper for the ConstitituteRBS DNA sequence.  The parameters
# that define the RBS strength and other properties are in
# `utr5_bcd2.csv`.
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

from ..dna import ConstitutiveRBS

class utr5_bcd2(ConstitutiveRBS):
    "BCD2 RBS"

# Define a shorthand version for convenience
bcd2 = utr5_bcd2

