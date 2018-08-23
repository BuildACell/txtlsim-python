# mixture.py - Mixture class and related functions
# RMM, 11 Aug 2018
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

import libsbml
from .dna import dna2rna_basic  #! TODO: move mechanisms to mechanisms/
from .dna import rna2prot_basic #! TODO: move mechanisms to mechanisms/

class Mixture():
    """The Mixture class is used as a container for a set of components.
    The components of a mixture define the species and reactions that
    are present in that mixture.  Mixtures can be added and scaled to
    create new mixtures (not yet implemented).

    """
    def __init__(self, name=None, mechanisms={}):
        # Create an SBML document container and model
        document = libsbml.SBMLDocument(3, 1)
        model = document.createModel()

        # Set up required units and containers
        model.setTimeUnits("second")    # set model-wide time units
        model.setExtentUnits("mole")    # set model units of extent
        model.setSubstanceUnits('mole') # set model substance units

        # Initialize instance variables
        self.name = name;               # Save the name of the mixture
        self._SBMLdoc = document        # SBML document container
        self.model = model              # SBML model object
        self.components = []            # components contained in mixture
        self.concentrations = []        # concentrations of each component

        # Default mechanisms to use
        self.mechanisms = {
            'transcription' : dna2rna_basic(),
            'translation'   : rna2prot_basic(),
        }

        # Override the default mechanisms with anything we were passed
        self.mechanisms.update(mechanisms)

    def write_sbml(self, filename):
        # Update all species in the mixture to make sure everything exists
        for component in self.components:
            #! TODO: figure out how concentrations should be handled
            component.update_species(self.model, self.mechanisms)

        # Now go through and add all of the reactions that are required
        for component in self.components:
            component.update_reactions(self.model, self.mechanisms)

        # Write the model to a file
        libsbml.writeSBMLToFile(self._SBMLdoc, filename)

#
# Functions for interacting with mixtures
#

# Create a new (empty) mixture 
def create_mixture(name):
    #! TODO: check that name is a valid string (?)
    return Mixture(name)

# Create a mixture containing buffer
def create_buffer(name):
    # Create a mixture to hold the buffer
    mixture = Mixture(name)
    
    #! TODO: read buffer specific parameters
    return mixture

# Add DNA to a mixture
def add_dna(mixture, dna, conc, type=None):
    #! TODO: figure out how to keep track of DNA types (linear, plasmid)
    # Add the DNA to the components (and concentrations) in the mixture
    mixture.components.append(dna)
    mixture.concentrations.append(conc)
    return None

# Combine the components of two more more mixtures
def combine_mixtures(mixtures, concentrations=None, name=None):
    # Create a name if we were sent done
    #! TODO: concatenate names of mixtures
    
    # Create a mixture for the results
    outmixture = Mixture(name)

    # Add the components (and concentrations) of inputs to the output
    for i in range(len(mixtures)):
        outmixture.components += mixtures[i].components
        #! TODO: scale concentrations 
        outmixture.concentrations += mixtures[i].concentrations
    
    return outmixture

# Write out the SBML description of the contexts of a mixture
def write_sbml(mixture, file):
    return mixture.write_sbml(file)
