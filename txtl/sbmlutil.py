# sbmlutil.py - libsbml helper functions
# RMM, 14 Aug 2018
#
# Copyright (c) 2018, Build-A-Cell. All rights reserved.
# See LICENSE file in the project root directory for details.

import re

# Helper function to add a species to the model
def add_species(model, type, name):
    species = model.createSpecies()
    prefix = type + " " if type != None else ""
    species.setName(prefix + name)

    # Construct the species ID
    species_id = re.sub(" ", "_", prefix + name)
    species_id = re.sub("--", "_", species_id)
    species.setId(species_id)

    return species

# Helper function to add a reaction to a model
def add_reaction(model, reactants, products, kf, kr):
    reaction = model.createReaction()

    # Create the reactants
    for species in reactants:
        reactant = reaction.createReactant()
        reactant.setSpecies(species.getId())

    # Create the products
    for species in products:
        product = reaction.createProduct()
        product.setSpecies(species.getId())

    # Create the rate constants for forward and reverse reactions
    param = model.createParameter()
    param.setValue(kf)
    if (kr != None):
        reaction.setReversible(True)
        param = model.createParameter()
        param.setValue(kr)

    return reaction
