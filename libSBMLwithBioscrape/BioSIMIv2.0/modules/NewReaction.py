from libsbml import * 
import libsbml
from modules.Subsystem import *
# def check(value, message):
#     """If 'value' is None, prints an error message constructed using
#     'message' and then exits with status code 1.  If 'value' is an integer,
#     it assumes it is a libSBML return status code.  If the code value is
#     LIBSBML_OPERATION_SUCCESS, returns without further action; if it is not,
#     prints an error message constructed using 'message' along with text from
#     libSBML explaining the meaning of the code, and exits with status code 1.
#     """
#     if value == None:
#             raise SystemExit('LibSBML returned a null value trying to ' + message + '.')
#     elif type(value) is int:
#         if value == LIBSBML_OPERATION_SUCCESS:
#             return
#         else:
#             err_msg = 'Error encountered trying to ' + message + '.' \
#                         + 'LibSBML returned error code ' + str(value) + ': "' \
#                         + OperationReturnValue_toString(value).strip() + '"'
#             raise SystemExit(err_msg)
#     else:
#         return

def createMath(formulaString):
    """Return math formula"""
    math_ast = parseFormula(formulaString)
    check(math_ast, 'create AST for rate expression')
    return math_ast


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

    def createNewReactant(self,rtSpeciesId,rtConstant,rtStoichiometry):
        """Return new reaction"""
        species_ref_obj_reactant = self.getReaction().createReactant()
        check(species_ref_obj_reactant,'created species_ref_obj_reactant reactant')
        check(species_ref_obj_reactant.setSpecies(rtSpeciesId),'set species_ref_obj_reactant ID')
        check(species_ref_obj_reactant.setConstant(rtConstant),'set species_ref_obj_reactant constant')
        check(species_ref_obj_reactant.setStoichiometry(rtStoichiometry),'set species_ref_obj_reactant stoichiometry')
        return species_ref_obj_reactant

    def createNewProduct(self,rtSpeciesId,rtConstant,rtStoichiometry):
        """Return new product"""
        species_ref_obj_product = self.getReaction().createProduct()
        check(species_ref_obj_product,'created species_ref_obj_product produc')
        check(species_ref_obj_product.setSpecies(rtSpeciesId),'set species_ref_obj_product ID')
        check(species_ref_obj_product.setConstant(rtConstant),'set species_ref_obj_product constant')
        check(species_ref_obj_product.setStoichiometry(rtStoichiometry),'set species_ref_obj_product stoichiometry')
        return species_ref_obj_product

    def createRate(self,math_ast):
        """Return rate """
        kinetic_law_reaction = self.getReaction().createKineticLaw()
        check(kinetic_law_reaction, 'create kinetic law')
        check(kinetic_law_reaction.setMath(math_ast), 'set math on kinetic law')
        return kinetic_law_reaction
