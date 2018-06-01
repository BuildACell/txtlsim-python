from libsbml import *
from modules.SimpleModel import *

class NewReaction(object):
    """
        Attributes:
            reaction: A reaction object   
    """

    def __init__(self, reaction):
        self.reaction = reaction

    def getReaction(self):
        '''Returns the Reaction object '''
        return self.reaction

    def setReaction(self, reaction):
        '''The Reaction object attribute is set '''
        self.reaction = reaction

    def createNewReactant(self, rtSpeciesId, rtConstant, rtStoichiometry):
        '''
        Creates a new Reactant inside the current Reaction object and returns the
        SpeciesReference object to it
        '''
        species_ref_obj_reactant = self.getReaction().createReactant()
        check(species_ref_obj_reactant,
              'created species_ref_obj_reactant reactant')
        check(species_ref_obj_reactant.setSpecies(
            rtSpeciesId), 'set species_ref_obj_reactant ID')
        check(species_ref_obj_reactant.setConstant(rtConstant),
              'set species_ref_obj_reactant constant')
        check(species_ref_obj_reactant.setStoichiometry(rtStoichiometry),
              'set species_ref_obj_reactant stoichiometry')
        return species_ref_obj_reactant

    def createNewProduct(self, rtSpeciesId, rtConstant, rtStoichiometry):
        '''
        Creates a new Product inside the current Reaction object and returns the
        SpeciesReference object to it
        '''
        species_ref_obj_product = self.getReaction().createProduct()
        check(species_ref_obj_product, 'created species_ref_obj_product produc')
        check(species_ref_obj_product.setSpecies(rtSpeciesId), 'set species_ref_obj_product ID')
        check(species_ref_obj_product.setConstant(rtConstant),
              'set species_ref_obj_product constant')
        check(species_ref_obj_product.setStoichiometry(rtStoichiometry),
              'set species_ref_obj_product stoichiometry')
        return species_ref_obj_product

    def createRate(self, math_ast):
        '''
        Creates a new KineticLaw object inside the current Reaction and returns it.
        The AST_Node object given as an argument in 
        math_ast is used to define the rate 
        '''
        kinetic_law_reaction = self.getReaction().createKineticLaw()
        check(kinetic_law_reaction, 'create kinetic law')
        check(kinetic_law_reaction.setMath(math_ast), 'set math on kinetic law')
        return kinetic_law_reaction


    def createMath(self, formulaString):
        ''' 
        Creates a new math AST_Node using the formulaString given and returns it 
        '''
        math_ast = parseL3Formula(formulaString)
        check(math_ast, 'create AST for rate expression')
        return math_ast
