# mixture.py - Mixture class and related functions
# RMM, 11 Aug 2018
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

import libsbml

class Mixture():
    def __init__(self, name=None):
        # Create an SBML document container and model
        document = libsbml.SBMLDocument(3, 1)
        model = document.createModel()

        # Set up required units and containers
        model.setTimeUnits("second")    # set model-wide time units
        model.setExtentUnits("mole")    # set model units of extent
        model.setSubstanceUnits('mole') # set model substance units

        # Decide on what mechanisms to include as default for a mixture (if any)
        #! TODO: implement mechanisms
        mechanisms = []

        # Initialize instance variables
        self.name = name;               # Save the name of the mixture
        self._SBMLdoc = document        # SBML document container
        self.model = model              # SBML model object
        self.components = []            # components contained in mixture
        self.concentrations = []        # concentrations of each component
        self.mechanisms = mechanisms    # list of mechanisms to invoke

    def add_mechanisms(self, mechanisms):
        self.mechanisms += mechanisms

    def write_sbml(self, filename):
        # Update all species in the mixture to make sure everything exists
        for component in self.components:
            component.update_species(self.model)

        # Go through each mechanism and add any species they require
        for mechanism in self.mechanisms:
            mechanism.update_species(self.model)

        # Now go through and create/update all reactions that we need
        for component in self.components:
            component.update_reactions(self.model)

        # Go through each mechanism and add any species they require
        for mechanism in self.mechanisms:
            mechanism.update_reactions(self.model)

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

