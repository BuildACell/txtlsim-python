# tube.py - Tube class and related functions
# RMM, 11 Aug 2018
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

import libsbml

class Tube():
    def __init__(self, name=None):
        # Create an SBML document container and model
        document = libsbml.SBMLDocument(3, 1)
        model = document.createModel()

        # Set up required units and containers
        model.setTimeUnits("second")    # set model-wide time units
        model.setExtentUnits("mole")    # set model units of extent
        model.setSubstanceUnits('mole') # set model substance units

        # Decide on what mechanisms to include when creating reactions
        #! TODO: implement reactions
        mechanisms = None

        # Initialize instance variables
        self.name = name;               # Save the name of the tube
        self._SBMLdoc = document        # SBML document container
        self.model = model              # SBML model object
        self.contents = []              # list of DNA/species contained in tube
        self.concentrations = []        # concentrations of each component
        self.mechanisms = mechanisms    # list of mechanisms to invoke

    def write_sbml(self, filename):
        # Update all species in the tube to make sure everything exists
        for species in self.contents:
            species.update_species(self.model)

        # Now go through and create/update all reactions that we need
        for species in self.contents:
            species.update_reactions(self.model)

        # Write the model to a file
        libsbml.writeSBMLToFile(self._SBMLdoc, filename)

#
# Functions for interacting with tubes
#

# Create a new (empty) tube 
def newtube(name):
    #! TODO: check that name is a valid string (?)
    return Tube(name)

# Create a tube containing extract
def extract(name):
    # Create a tube to hold the extract
    tube = Tube(name)
    
    #! TODO: read extract specific parameters
    return tube

# Create a tube containing buffer
def buffer(name):
    # Create a tube to hold the buffer
    tube = Tube(name)
    
    #! TODO: read buffer specific parameters
    return tube

# Add DNA to a tube
def add_dna(tube, dna, conc, type=None):
    #! TODO: figure out how to keep track of DNA types (linear, plasmid)
    # Add the DNA to the contents (and concentrations) in the tube
    tube.contents.append(dna)
    tube.concentrations.append(conc)
    return None

# Combine the contents of two more more tubes
def combine_tubes(tubes, concentrations=None, name=None):
    # Create a name if we were sent done
    #! TODO: concatenate names of tubes
    
    # Create a tube for the results
    outtube = Tube(name)

    # Add the contents (and concentrations) of inputs to the output
    for i in range(len(tubes)):
        outtube.contents += tubes[i].contents
        #! TODO: scale concentrations 
        outtube.concentrations += tubes[i].concentrations
    
    return outtube

# Write out the SBML description of the contexts of a tube
def write_sbml(tube, file):
    return tube.write_sbml(file)
