# mixture.py - Mixture class and related functions
# RMM, 11 Aug 2018
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

import libsbml

class Mixture():
    """Container for components (extract, genes, etc)

    The Mixture class is used as a container for a set of components.
    The components of a mixture define the species and reactions that
    are present in that mixture.  Mixtures can be added and scaled to
    create new mixtures (not yet implemented).

    Data attributes
    ---------------
    name            Name of the mixture
    document        SBMLDocument containing the model
    model           SBML Model containing species, reactions
    components      List of components in the mixture (list of Components)
    concentrations  Concentration of each component (list of floats)
    mechanisms      Default mechanisms for this mixture (dict)
    parameters      Global parameters for the mixture (dict)

    The mechanisms and parameters dictionaries are established by the
    create_extract() and create_buffer() functions, using the
    properties of the Extract and Buffer components.

    Operations on mixtures
    ----------------------
    # create a new mixture
    mix = create_mixture("name")

    # add a DNA assembly to a mixture
    add_dna(mix, dna_assy, conc)        
    mix += conc * dna_assy

    # Combine mixtures at scaled concentrations
    mix = combine_mixtures([mix1, mix2, ...], [conc1, conc2, ...]
    mix = conc1 * mix1 + conc2 * mix2 + conc3 * mix3

    # Add a component to a mixture
    mix = mix + conc * component
    mix += conc * component

    # Generate an SMBL file for the model represented in a mixture
    write_sbml(mix, filename)
    mix.write_sbml(filename)

    """
    def __init__(self, name=None):
        "Create a new mixture"
        
        # Create an SBML document container and model
        document = libsbml.SBMLDocument(3, 1)
        model = document.createModel()

        # Define units for area (not used, but keeps COPASI from complaining)
        unitdef = model.createUnitDefinition()
        unitdef.setId('square_metre')
        unit = unitdef.createUnit()
        unit.setKind(libsbml.UNIT_KIND_METRE)
        unit.setExponent(2)
        unit.setScale(0)
        unit.setMultiplier(1)

        # Set up required units and containers
        model.setTimeUnits('second')            # set model-wide time units
        model.setExtentUnits('mole')            # set model units of extent
        model.setSubstanceUnits('mole')         # set model substance units
        model.setLengthUnits('metre')           # area units (never used?)
        model.setAreaUnits('square_metre')      # area units (never used?)
        model.setVolumeUnits('litre')           # default volume unit

        # Define the default compartment
        compartment = model.createCompartment()
        compartment.setId('txtl')
        compartment.setConstant(True)           # keep compartment size constant
        compartment.setSpatialDimensions(3)     # 3 dimensional compartment
        compartment.setVolume(1e-6)             # 1 microliter

        # Initialize instance variables
        self.name = name;               # Save the name of the mixture
        self._SBMLdoc = document        # SBML document container
        self.model = model              # SBML model object
        self.compartment = compartment  # SBML compartment
        self.components = []            # components contained in mixture
        self.concentrations = []        # concentrations of each component

        # Mixture level variables (set by special components)
        self.parameters = {}

        # Override the default mechanisms with anything we were passed
        self.mechanisms = {}

    def write_sbml(self, filename):
        "Generate an SBML file for the current mixture (model)"
        
        # Update all species in the mixture to make sure everything exists
        for i in range(len(self.components)):
            concentration = self.concentrations[i]
            component = self.components[i]

            # Create all of the species for this component
            component.update_species(self, concentration, self.mechanisms)

        # Now go through and add all of the reactions that are required
        for component in self.components:
            component.update_reactions(self, self.mechanisms, self.parameters)

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
def combine_mixtures(mixtures, volumes=None, name=None):
    # Create a name if we were sent done
    #! TODO: concatenate names of mixtures
    
    # Create a mixture for the results
    outmixture = Mixture(name)

    # Keep track of the total amount of mixture we are creating (for scaling)
    # If no volumes are given, assume equal volumes of 1 unit each
    total_volume = sum(volumes) if volumes != None else len(mixtures)

    # Add the components (and concentrations) of inputs to the output
    for i in range(len(mixtures)):
        # Combine the mechanisms
        #! TODO: issue a warning if there are conflicting mechanisms
        outmixture.mechanisms.update(mixtures[i].mechanisms)

        # Components of new mixture are concatenation of mixture components
        outmixture.components += mixtures[i].components

        # Concentrations are scaled by the volume
        scale = volume[i]/total_volume if volumes != None else 1/total_volume
        for j in range(len(mixtures[i].concentrations)):
            outmixture.concentrations += [mixtures[i].concentrations[j] * scale]

    return outmixture

# Write out the SBML description of the contexts of a mixture
def write_sbml(mixture, file):
    return mixture.write_sbml(file)
