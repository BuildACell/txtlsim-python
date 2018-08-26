# __init__.py - initialization of txtl toolbox
# RMM, 11 Aug 2018

# Core classes
from .mixture import *
from .mechanism import *
from .component import *
from .parameter import *

# Core components
from .extract import *
from .dna import *

# Additional functions
from .sbmlutil import *

# Some constants used through the library
minutes = 60                    # number of seconds in a minute
hours = 60 * 60                 # number of seconds in an hour

# Legacy support for "tubes" (= mixtures)
#! TODO: move to separate legacy submodule (use `from txtl.legacy import *`)
Tube = Mixture
newtube = create_mixture
extract = create_extract
buffer = create_buffer
combine_tubes = combine_mixtures
