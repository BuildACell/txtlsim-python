# sbmlutil.py - libsbml helper functions
# RMM, 14 Aug 2018
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

import libsbml
import re

# Reaction ID number
reaction_id = 0

# Helper function to add a species to the model
def add_species(model, type, name, ic=None, debug=False):
    # Construct the species name
    prefix = type + " " if type != None else ""
    species_name = prefix + name
    
    # Construct the species ID
    species_id = re.sub(" ", "_", species_name)
    species_id = re.sub("--", "_", species_id)
    species_id = re.sub(":", "_", species_id)
    
    # Check to see if this species is already present
    species = find_species(model, species_id)
    if species == None:
        if debug: print("Adding species %s" % species_name)
        species = model.createSpecies()
        prefix = type + " " if type != None else ""
        species.setName(species_name)
        species.setId(species_id)

    else:
        if debug: print("add_species: %s already exists", species.getId())
        
    # Set the initial concentration (if specified)
    #! TODO: Decide whether to warn if species is already present
    #! TODO: add initial concentrations if reaction is present
    if ic != None:
        if debug: print("    %s IC = %s" % (species_name, ic))
        species.setInitialConcentration(float(ic))

    return species

# Look for a species in the current model
def find_species(model, id):
    return model.getSpecies(id)

# Helper function to add a pameter to the model
def add_parameter(model, name, value=0, debug=False):
    # Check to see if this parameter is already present
    parameter = find_parameter(model, name)
    if parameter == None:
        if debug: print("Adding parameter %s" % name)
        parameter = model.createParameter()
        parameter.setId(name)

    else:
        if debug: print("add_parameter: %s already exists", parameter.getId())

    # Set the value of the parameter
    parameter.setValue(float(value))

    return parameter

# Look for a parameter in the current model
def find_parameter(model, id):
    return model.getParameter(id)

# Helper function to add a reaction to a model
def add_reaction(model, reactants, products, kf, kr=None,
                 debug=False, id=None):
    """Add a reaction to a model

    The `add_reaction` function is used to add a reaction to a model.
    It allows specifation for reaction rates as either symbolic or
    numeric entries, including the use of global symbolic names.
    Reactions can be unidirectional or reversible.

    Parameters
    ----------
    model       SBML model
    reactants   List of SBML species that are reactants in the reaction
    projects    List of SBML species that are products of the reaction
    kf          Forward rate constant (parameter, string, number, or list)
    kf          Reverse rate constant (None if non-reversible)
    id          Optional parameter to specify reaction id (otherwise numbered)

    Note: the current implementation requires that non-unitary
    stochiometries be represented by repeated entries in the reactants
    and/or products list.

    """
    reaction = model.createReaction()

    # Store the reaction id
    global reaction_id
    reaction.setId("r%d" % (reaction_id));
    reaction_id += 1

    if debug: print("Creating reaction: ",
                    reactants, "-->[", kf, "] ", products)

    #! Sort out the reaction rates and parameter names
    #
    # Reactions can be specified in multiple forms
    #
    #   "string"                Reaction is a global paramater
    #   ["string", float]       Local reaction rate, with initial value
    #   float                   Local reaction rate

    #
    # Create forward and reverse rate strings
    #
    # The rate expression for the kinetic law in the expression is
    # created by building up the string that specifies the kinetic
    # law.  If the parameter `kf` is a string, we assume it is a
    # global parameter value that will be set later.  if it is a
    # number, then we create a local parameter within this reaction.
    #
    kfname = kf if isinstance(kf, str) else "k"

    # Create the reactants
    ratestring = kfname
    for species in reactants:
        reactant = reaction.createReactant()
        reactant.setSpecies(species.getId())
        ratestring += " * " + species.getId()

    # Create the products
    for species in products:
        product = reaction.createProduct()
        product.setSpecies(species.getId())

    # Create a kinetic law for the reaction
    if debug: print("    Creating kinetic law: ", ratestring)
    ratelaw = reaction.createKineticLaw();
    if isinstance(kf, float):
        param = ratelaw.createParameter();
        param.setId(kfname)
        param.setValue(kf)
    ratelaw.setFormula(ratestring);

    # If the reverse rate is given, switch things around create reverse raaction
    if (kf != None):
        revreaction = add_reaction(model, products, reactants, kr, None)
        return (reaction, revreaction)

    return reaction
