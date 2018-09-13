# mixture.py - Mixture class and related functions
# RMM, 11 Aug 2018
#
# This file default the mixture class, which is used to hold a
# collection of components.  The docstring from the Mixture class
# describes the use of this function in more detail.
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

import libsbml
from .sbmlutil import create_sbml_model

class Mixture():
    """Container for components (extract, genes, etc)

    The Mixture class is used as a container for a set of components
    that define the species and reactions to implement a TX-TL system.
    Mixtures can be added and scaled to create new mixtures (not yet
    implemented).

    Data attributes
    ---------------
    name                Name of the mixture
    document            SBMLDocument containing the model
    model               SBML Model containing species, reactions
    components          List of components in the mixture (list of Components)
    concentrations      Concentration of each component (list of floats)
    default_mechanisms  Default mechanisms for this mixture (dict)
    custom_mechanisms   User-specified mechanisms for this mixture (dict)
    parameters          Global parameters for the mixture (dict)

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
    def __init__(self, name=None, mechanisms={}, config_file=None):
        "Create a new mixture"
        
        # Create an SBML document container and model
        document, model, compartment = create_sbml_model()

        # Initialize instance variables
        self.name = name                # Save the name of the mixture
        self._SBMLdoc = document        # SBML document container
        self.model = model              # SBML model object
        self.compartment = compartment  # SBML compartment
        self.components = []            # components contained in mixture
        self.concentrations = []        # concentrations of each component

        # Override the default mechanisms with anything we were passed
        # Note: These are overrwriten by create_extract()
        self.default_mechanisms = {
            # 'mechanism' : MechanismConstructor()
        }
        self.custom_mechanisms = mechanisms

        # Read the configuration parameters
        self.parameters = {}
        if (config_file != None):
            self.parameters.update(load_config(config_file))

    def _update_sbml_model(self):
        """Updating the internal SBML representation"""
        # Update all species in the mixture to make sure everything exists
        assert (len(self.concentrations) == len(self.components))
        for component, concentration in zip(self.components, self.concentrations):
            # Create all (global) parameters for this component
            # ! TODO: need to document this better; see extract.py
            component.update_parameters(self)

            # Create all of the species for this component
            component.update_species(self, concentration)



        # Now go through and add all of the reactions that are required
        for component in self.components:
            component.update_reactions(self)

    def print_report(self):
        self._update_sbml_model()
        # Now go through and add all of the reactions that are required
        for component in self.components:
            print(component)
            for mechanism_name, mechanism_implementation in component.default_mechanisms.items():
                print('\t' + mechanism_name + ": " + str(mechanism_implementation))

    def write_sbml(self, filename):
        "Generate an SBML file for the current mixture (model)"
        self._update_sbml_model()

        # Write the model to a file
        libsbml.writeSBMLToFile(self._SBMLdoc, filename)

    def __str__(self):
        """Returning the name of the mixture"""
        return self.name

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
    
    # Create a mixture for the results
    if name is None:
        name = 'Mix_of'

    outmixture = Mixture(name)

    # Keep track of the total amount of mixture we are creating (for scaling)
    # If no volumes are given, assume equal volumes of 1 unit each
    total_volume = sum(volumes) if volumes is not None else len(mixtures)

    # Add the components (and concentrations) of inputs to the output
    for i, mixture in enumerate(mixtures):
        # Combine the mechanisms
        #! TODO: issue a warning if there are conflicting mechanisms
        outmixture.default_mechanisms.update(mixture.default_mechanisms)
        outmixture.custom_mechanisms.update(mixture.custom_mechanisms)
        outmixture.name += '_' + str(mixture) # getting the name of a mixture
        # Components of new mixture are concatenation of mixture components
        outmixture.components += mixture.components

        # Concentrations are scaled by the volume
        scale = volumes[i]/total_volume if volumes is not None else 1/total_volume
        for concentration in mixture.concentrations:
            outmixture.concentrations += [concentration * scale]

        # Combine parameter dictionaries from each mixture
        #! TODO: issue a warning if there are conflicting parameters
        outmixture.parameters.update(mixtures[i].parameters)

    assert len(outmixture.concentrations) == len(outmixture.components)
    return outmixture

# Write out the SBML description of the contexts of a mixture
def write_sbml(mixture, file):
    return mixture.write_sbml(file)
