from libsbml import * 
import libsbml
import numpy as np

def check(value, message):
   """If 'value' is None, prints an error message constructed using
   'message' and then exits with status code 1.  If 'value' is an integer,
   it assumes it is a libSBML return status code.  If the code value is
   LIBSBML_OPERATION_SUCCESS, returns without further action; if it is not,
   prints an error message constructed using 'message' along with text from
   libSBML explaining the meaning of the code, and exits with status code 1.
   """
   if value == None:
     raise SystemExit('LibSBML returned a null value trying to ' + message + '.')
   elif type(value) is int:
     if value == LIBSBML_OPERATION_SUCCESS:
       return
     else:
       err_msg = 'Error encountered trying to ' + message + '.' \
                 + 'LibSBML returned error code ' + str(value) + ': "' \
                 + OperationReturnValue_toString(value).strip() + '"'
       raise SystemExit(err_msg)
   else:
     return

def createNewCompartment(model, cId, cName, cSize, cUnits, cConstant):
    comp_obj = model.createCompartment()
    check(comp_obj,'Create comp_obj compartment')
    check(comp_obj.setId(cId), 'Set comp_obj id')
    check(comp_obj.setName(cName),'Set comp_obj name')
    check(comp_obj.setSize(cSize),'set comp_obj size')
    check(comp_obj.setUnits(cUnits),'set comp_obj units')
    check(comp_obj.setConstant(cConstant),'set comp_obj constant')
    return comp_obj

def createNewSpecies(model,sId,sName,sComp,sInitial,sConstant,sBoundary,sSubstance,sHasOnlySubstance):
    s_obj = model.createSpecies()
    check(s_obj,'created s_obj species')
    check(s_obj.setId(sId),'set s_obj ID')
    check(s_obj.setName(sName),'set s_obj name')
    check(s_obj.setCompartment(sComp),'set s_obj compartment')
    check(s_obj.setInitialAmount(sInitial),'set s_obj initial amount')
    check(s_obj.setConstant(sConstant),'set s_obj constant')
    check(s_obj.setBoundaryCondition(sBoundary),'set boundary s_obj condition false')
    check(s_obj.setSubstanceUnits(sSubstance),'set substance units s_obj')
    check(s_obj.setHasOnlySubstanceUnits(sHasOnlySubstance),'set has only substance units s_obj')
    return s_obj


def createNewParameter(model,pId,pName,pValue,pConstant,pUnit):
    p_obj = model.createParameter()
    check(p_obj,'created p_obj species')
    check(p_obj.setId(pId),'set p_obj ID')
    check(p_obj.setName(pName),'set p_obj name')
    check(p_obj.setValue(pValue),'set p_obj value')
    check(p_obj.setConstant(pConstant),'set p_obj constant')
    check(p_obj.setUnits(pUnit),'set p_obj units')
    return p_obj

def createNewReaction(model,rId,rReversible,rFast):
    r_obj = model.createReaction()
    check(r_obj,'created r_obj reaction')
    check(r_obj.setId(rId),'set r_obj ID')
    check(r_obj.setReversible(rReversible),'set r_obj reversible')
    check(r_obj.setFast(rFast),'set r_obj Fast')
    return r_obj

def createNewReactant(reaction,rtSpeciesId,rtConstant,rtStoichiometry):
    species_ref_obj_reactant = reaction.createReactant()
    check(species_ref_obj_reactant,'created species_ref_obj_reactant reactant')
    check(species_ref_obj_reactant.setSpecies(rtSpeciesId),'set species_ref_obj_reactant ID')
    check(species_ref_obj_reactant.setConstant(rtConstant),'set species_ref_obj_reactant constant')
    check(species_ref_obj_reactant.setStoichiometry(rtStoichiometry),'set species_ref_obj_reactant stoichiometry')
    return species_ref_obj_reactant

def createNewProduct(reaction,rtSpeciesId,rtConstant,rtStoichiometry):
    species_ref_obj_product = reaction.createProduct()
    check(species_ref_obj_product,'created species_ref_obj_product produc')
    check(species_ref_obj_product.setSpecies(rtSpeciesId),'set species_ref_obj_product ID')
    check(species_ref_obj_product.setConstant(rtConstant),'set species_ref_obj_product constant')
    check(species_ref_obj_product.setStoichiometry(rtStoichiometry),'set species_ref_obj_product stoichiometry')
    return species_ref_obj_product

def createRate(reaction,math_ast):
    kinetic_law_reaction = reaction.createKineticLaw()
    check(kinetic_law_reaction, 'create kinetic law')
    check(kinetic_law_reaction.setMath(math_ast), 'set math on kinetic law')
    return kinetic_law_reaction

def createMath(formulaString):
    math_ast = parseFormula(formulaString)
    check(math_ast, 'create AST for rate expression')
    return math_ast
