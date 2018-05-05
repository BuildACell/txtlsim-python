from libsbml import *
from modules.CreateSubsystem import *

class NewReaction(object):
    """
        Attributes:
            reaction: A reaction object   
    """

    def __init__(self, reaction):
        """Return a Subsystem object whose model is "model"."""
        self.reaction = reaction

    def getReaction(self):
        """Return the model of the subsystem"""
        return self.reaction

    def setReaction(self, reaction):
        """Set the subsystem's model"""
        self.reaction = reaction

    def createNewReactant(self, rtSpeciesId, rtConstant, rtStoichiometry):
        """Return new reaction"""
        species_ref_obj_reactant = self.getReaction().createReactant()
        check(species_ref_obj_reactant,
              'created species_ref_obj_reactant reactant')
        check(species_ref_obj_reactant.setId(rtSpeciesId),
              'set id species_ref_obj_reactant ID')
        # check(species_ref_obj_reactant.setName(rtSpeciesId),
            #   'set name species_ref_obj_reactant ID')
        check(species_ref_obj_reactant.setSpecies(
            rtSpeciesId), 'set species_ref_obj_reactant ID')
        check(species_ref_obj_reactant.setConstant(rtConstant),
              'set species_ref_obj_reactant constant')
        check(species_ref_obj_reactant.setStoichiometry(rtStoichiometry),
              'set species_ref_obj_reactant stoichiometry')
        return species_ref_obj_reactant

    def createNewProduct(self, rtSpeciesId, rtConstant, rtStoichiometry):
        """Return new product"""
        species_ref_obj_product = self.getReaction().createProduct()
        check(species_ref_obj_product, 'created species_ref_obj_product produc')
        check(species_ref_obj_product.setId(rtSpeciesId),
              'set id species_ref_obj_product ID')
        # check(species_ref_obj_product.setName(rtSpeciesId),
            #   'set name species_ref_obj_product ID')
        check(species_ref_obj_product.setSpecies(rtSpeciesId), 'set species_ref_obj_product ID')
        check(species_ref_obj_product.setConstant(rtConstant),
              'set species_ref_obj_product constant')
        check(species_ref_obj_product.setStoichiometry(rtStoichiometry),
              'set species_ref_obj_product stoichiometry')
        return species_ref_obj_product

    def createRate(self, math_ast):
        """Return rate """
        kinetic_law_reaction = self.getReaction().createKineticLaw()
        check(kinetic_law_reaction, 'create kinetic law')
        check(kinetic_law_reaction.setMath(math_ast), 'set math on kinetic law')
        return kinetic_law_reaction


    def createMath(self, formulaString):
        """Return math formula"""
        math_ast = parseL3Formula(formulaString)
        check(math_ast, 'create AST for rate expression')
        # check(math_ast.setId(self.getReaction().getId()), 'set id AST for rate expression')
        return math_ast
