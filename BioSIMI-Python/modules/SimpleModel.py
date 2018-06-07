from libsbml import *

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
            Model : Model object  
    """

    def __init__(self, Model):
        self.Model = Model 

    def getModel(self):
        """ Returns the Model object """
        return self.Model

    def setModel(self, Model):
        """ Set the new Model object """
        self.Model = Model

    def createNewUnitDefinition(self, uid, ukind, exponent, scale, multiplier):
        ''' 
        Creates a new UnitDefinition inside the 
        Model with the given attributes and returns a pointer to the object created
        '''
        model = self.getModel()
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


    def createNewConstraint(self, formulaString, msg = 'Constraint not satisfied for the model', name = ''):
        '''
        Creates a new Constraint in the Model and returns a pointer to the object created
        '''
        model = self.getModel()
        check(model,'retreived model object')
        constr = model.createConstraint()
        check(constr, 'creating a new constraint inside the model')
        astMath = parseL3Formula(formulaString)
        check(constr.setMath(astMath), 'setting math to the constraint')
        check(constr.setMessage(msg, True), 'setting the message to the constraint')
        if name != '':
            check(constr.setName(name),'setting name of the constraint')
        
        return constr

    def createNewEvent(self, id, trigger_persistent, trigger_initialValue, 
        trigger_formula, variable_id, assignment_formula, delay_formula = '', 
        priority_formula = '', useValuesFromTriggerTime = True, name = ''):
        '''
        Creates a new Event in the Model and returns a pointer to the object created
        '''
        model = self.getModel()
        check(model,'retreived model object')
        e = model.createEvent()
        check(e,'creating new event in the model')
        check(e.setId(id), 'setting ID of the event created')
        if name != '':
            check(e.setName(name),'setting name of the event created')

        eTrig = e.createTrigger()
        check(eTrig,'creating trigger inside the event')
        check(eTrig.setPersistent(trigger_persistent), 'setting persistent value to the trigger')
        check(eTrig.setInitialValue(trigger_initialValue), 'setting initial value to the trigger')
        trig_math = parseL3Formula(trigger_formula)
        check(eTrig.setMath(trig_math), 'setting math to the trigger')

        eA = e.createEventAssignment()
        check(eA, 'creating event assignment inside the event')
        check(eA.setVariable(variable_id), 'setting variable in the event assignment')
        asmt_math = parseL3Formula(assignment_formula)
        check(eA.setMath(asmt_math), 'setting math to the event assignment')

        if delay_formula != '':
            eDel = e.createDelay()
            check(eDel, 'creating a new delay inside the event')
            del_math = parseL3Formula(delay_formula)
            check(eDel.setMath(del_math), 'setting the math to the delay')
        if priority_formula != '':
            eP = e.createPriority()
            check(eP, 'creating a new priority inside the event')
            prio_math = parseL3Formula(priority_formula)
            check(eP.setMath(prio_math), 'setting the math to the priority')
        e.setUseValuesFromTriggerTime(useValuesFromTriggerTime)
        return e

    def createNewInitialAssignment(self, symbol, initialAssignment_formula):
        '''
        Creates a new InitialAssignment in the Model and returns a pointer to the object created
        '''
        model = self.getModel()
        check(model,'retreived model object')
        init_asmt = model.createInitialAssignment()
        check(init_asmt,'creating new initial assignment inside the model')
        check(init_asmt.setSymbol(symbol),'setting the symbol to the initial assignment')
        initAsmt_math = parseL3Formula(initialAssignment_formula)
        check(init_asmt.setMath(initAsmt_math),'setting math to the initial assignment')
        return 

    def createNewAssignmentRule(self, variable_id, assignmentRule_formula):
        '''
        Creates a new AssignmentRule in the Model and returns a pointer to the object created
        '''
        model = self.getModel()
        check(model,'retreived model object')
        asmt = model.createAssignmentRule()
        check(asmt, 'creating new assignment rule in the model')
        check(asmt.setFormula(assignmentRule_formula), 'setting the formula to the assignment rule')
        check(asmt.setVariable(variable_id), 'setting the variable to the assignment rule')
        return 

    def createNewRateRule(self, variable_id, rateRule_formula):
        '''
        Creates a new RateRule in the Model and returns a pointer to the object created
        '''
        model = self.getModel()
        check(model,'retreived model object')
        rateRule = model.createRateRule()
        check(rateRule, 'creating a new rate rule inside the model')
        check(rateRule.setFormula(rateRule_formula), 'setting the formula for the rate rule')
        check(rateRule.setVariable(variable_id), 'setting the variable for the rate rule')
        return 

    def createNewAlgebraicRule(self, variable_id, algebraicRule_formula):
        '''
        Creates a new AlgebraicRule in the Model and returnsa pointer to the object created
        '''
        model = self.getModel()
        check(model,'retreived model object')
        algbRule = model.createAlgebraicRule()
        check(algbRule, 'creating new algebraic rule inside the model')
        check(algbRule.setFormula(algebraicRule_formula), 'setting the formula for the algebraic rule')
        check(algbRule.setVariable(variable_id), 'setting the variable for the algebraic rule')
        return 

    def createNewFunctionDefinition(self, id, functionDefinition_formula, name = ''):
        '''
        Creates a new FunctionDefinition in the Model and returns a pointer to the object created
        '''
        model = self.getModel()
        check(model,'retreived model object')
        func_def = model.createFunctionDefinition()
        check(func_def, 'creating a new function definition inside the model')
        check(func_def.setId(id), 'setting the id of the function definition')
        if name != '' :
            check(func_def.setName(name), 'setting the name of the function definition')
        func_math = parseL3Formula(functionDefinition_formula)
        check(func_def.setMath(func_math), 'setting the math for the function definition')
        return 

    def createNewCompartment(self, cId, cName, cSize, cUnits, cConstant):
        '''
        Creates a new Compartment in the Model and returns a pointer to the object created
        '''
        model = self.getModel()
        check(model,'retreived model object')
        comp_obj = model.createCompartment()
        check(comp_obj, 'Create comp_obj compartment')
        check(comp_obj.setId(cId), 'Set comp_obj id')
        check(comp_obj.setName(cName), 'Set comp_obj name')
        check(comp_obj.setSize(cSize), 'set comp_obj size')
        check(comp_obj.setUnits(cUnits), 'set comp_obj units')
        check(comp_obj.setConstant(cConstant), 'set comp_obj constant')
        return comp_obj

    def createNewSpecies(self, sId, sName, sComp, sInitial, sConstant, sBoundary, sSubstance, sHasOnlySubstance):
        ''' 
        Creates a new Species object inside the 
        Model with the given attributes and returns a pointer to the Species object created
        '''
        model = self.getModel()
        check(model,'retreived model object')
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
        ''' 
        Creates a new Reaction object inside the 
        Model with the given attributes and returns a pointer to the Reaction object created
        '''
        model = self.getModel()
        check(model,'retreived model object')
        r_obj = model.createReaction()
        check(r_obj, 'created r_obj reaction')
        check(r_obj.setId(rId), 'set r_obj ID')
        check(r_obj.setReversible(rReversible), 'set r_obj reversible')
        check(r_obj.setFast(rFast), 'set r_obj Fast')
        return r_obj

    def createNewParameter(self, pId, pName, pValue, pConstant, pUnit):
        ''' 
        Creates a new Parameter object inside the 
        Model with the given attributes and returns a pointer to the Parameter object created
        '''
        model = self.getModel()
        check(model,'retreived model object')
        p_obj = model.createParameter()
        check(p_obj, 'created p_obj species')
        check(p_obj.setId(pId), 'set p_obj ID')
        check(p_obj.setName(pName), 'set p_obj name')
        check(p_obj.setValue(pValue), 'set p_obj value')
        check(p_obj.setConstant(pConstant), 'set p_obj constant')
        check(p_obj.setUnits(pUnit), 'set p_obj units')
        return p_obj
    
    def getSpeciesByName(self, name):
        ''' 
        Returns a list of species in the Model with the given name
        '''
        model = self.getModel()
        check(model,'retreived model object')
        species_found =[]
        for species in model.getListOfSpecies():
            if species.getName() == name:
                species_found.append(species)
        if len(species_found) == 1:
            return species_found[0] 
        elif not species_found:
            print('WARNING -- The species ' + name + ' not found. The program may not work')
            return
        else:
            print('Multiple species with name ' + name + ' found. Returning a list')
            return species_found
    

