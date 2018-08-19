# __init__.py - initialization of txtl toolbox
# RMM, 11 Aug2018

from .mixture import *
from .dna import *
from .mechanisms import *
from .extract import *

# Some constants used through the library
minutes = 60                    # number of seconds in a minute
hours = 60 * 60                 # number of seconds in an hour

# Legacy support for "tubes" (= mixtures)
Tube = Mixture
newtube = create_mixture
extract = create_extract
buffer = create_buffer
combine_tubes = combine_mixtures
