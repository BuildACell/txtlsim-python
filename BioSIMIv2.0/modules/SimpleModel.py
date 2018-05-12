from libsbml import *
# from modules.Subsystem import check
    #%config InlineBackend.figure_f.ormats=['svg']

def check(value, message):
    """If 'value' is None, prints an error message constructed using
    'message' and then exits with status code 1.  If 'value' is an integer,
    it assumes it is a libSBML return status code.  If the code value is
    LIBSBML_OPERATION_SUCCESS, returns without further action; if it is not,
    prints an error message constructed using 'message' along with text from
    libSBML explaining the meaning of the code, and exits with status code 1.
    """
    if value == None:
            raise SystemExit(
                'LibSBML returned a null value trying to ' + message + '.')
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


class SimpleModel(object):
    """
       Attributes:
            NewModel : SBMLDocument object for a NewSubsystem
    """

    def __init__(self, NewModel):
        self.NewModel = NewModel 

    def getNewModel(self):
        """ Returns the SBMLDocument of the subsystem """
        return self.NewModel

    def setNewModel(self, NewModel):
        """ Set the new document SBMLDocument object """
        self.NewModel = NewModel

    def createNewUnit(self, uid, ukind, exponent, scale, multiplier):
        model = self.getNewModel()
        unitdef = model.createUnitDefinition()
        check(unitdef, 'create unit definition')
        check(unitdef.setId(uid), 'set unit definition id')
        unit = unitdef.createUnit()
        check(unit, 'create unit on unitdef')
        check(unit.setKind(ukind), 'set unit kind')
        check(unit.setExponent(exponent), 'set unit exponent')
        check(unit.setScale(scale), 'set unit scale')
        check(unit.setMultiplier(multiplier), 'set unit multiplier')
        return unitdef


    def createNewCompartment(self, cId, cName, cSize, cUnits, cConstant):
        """"Return the new compartment of the model"""
        model = self.getNewModel()
        comp_obj = model.createCompartment()
        check(comp_obj, 'Create comp_obj compartment')
        check(comp_obj.setId(cId), 'Set comp_obj id')
        check(comp_obj.setName(cName), 'Set comp_obj name')
        check(comp_obj.setSize(cSize), 'set comp_obj size')
        check(comp_obj.setUnits(cUnits), 'set comp_obj units')
        check(comp_obj.setConstant(cConstant), 'set comp_obj constant')
        return comp_obj

    def createNewSpecies(self, sId, sName, sComp, sInitial, sConstant, sBoundary, sSubstance, sHasOnlySubstance):
        """Return the new species of the model"""
        model = self.getNewModel()
        s_obj = model.createSpecies()
        check(s_obj, 'created s_obj species')
        check(s_obj.setId(sId), 'set s_obj ID')
        check(s_obj.setName(sName), 'set s_obj name')
        check(s_obj.setCompartment(sComp), 'set s_obj compartment')
        check(s_obj.setInitialAmount(sInitial), 'set s_obj initial amount')
        check(s_obj.setConstant(sConstant), 'set s_obj constant')
        check(s_obj.setBoundaryCondition(sBoundary),
              'set boundary s_obj condition false')
        check(s_obj.setSubstanceUnits(sSubstance), 'set substance units s_obj')
        check(s_obj.setHasOnlySubstanceUnits(sHasOnlySubstance),
              'set has only substance units s_obj')
        return s_obj

    def createNewReaction(self, rId, rReversible, rFast):
        """Return new reaction object"""
        model = self.getNewModel()
        r_obj = model.createReaction()
        check(r_obj, 'created r_obj reaction')
        check(r_obj.setId(rId), 'set r_obj ID')
        check(r_obj.setReversible(rReversible), 'set r_obj reversible')
        check(r_obj.setFast(rFast), 'set r_obj Fast')
        return r_obj

    def createNewParameter(self, pId, pName, pValue, pConstant, pUnit):
        model = self.getNewModel()
        p_obj = model.createParameter()
        check(p_obj, 'created p_obj species')
        check(p_obj.setId(pId), 'set p_obj ID')
        check(p_obj.setName(pName), 'set p_obj name')
        check(p_obj.setValue(pValue), 'set p_obj value')
        check(p_obj.setConstant(pConstant), 'set p_obj constant')
        check(p_obj.setUnits(pUnit), 'set p_obj units')
        return p_obj
    
    def getSpeciesByName(self, name):
        model = self.getNewModel()
        for species in model.getListOfSpecies():
            if species.getName() == name:
                return species


