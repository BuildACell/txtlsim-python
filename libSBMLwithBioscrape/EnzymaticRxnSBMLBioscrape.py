#%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib as mpl

#%config InlineBackend.figure_f.ormats=['svg']

mpl.rc('axes', prop_cycle=(mpl.cycler('color', ['r', 'k', 'b','g','y','m','c']) ))

mpl.rc('xtick', labelsize=12) 
mpl.rc('ytick', labelsize=12)


import numpy as np

# Code for simple gene expression without delay

# Import relevant types
# from bioscrape.types import Model
# from bioscrape.simulator import DeterministicSimulator, SSASimulator
# from bioscrape.simulator import ModelCSimInterface

from libsbml import *
import libsbml 

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
 
try:
   sbmlDoc = SBMLDocument(3, 1)
except ValueError:
   print('Could not create SBMLDocument object')
   sys.exit(1)
 
 # Create a Model object inside the SBMLDocument object and set its
 # identifier, checking the returned values.  The call to setId() returns a
 # status code to indicate whether the assignment was successful.
 
model = sbmlDoc.createModel()
if model == None:
   # Do something to handle the error here.
   print('Unable to create Model object.')
   sys.exit(1)
 
status = model.setId('EnzymaticRxnModel')
if status != LIBSBML_OPERATION_SUCCESS:
   # Do something to handle the error here.
   print('Unable to set identifier on the Model object')
   sys.exit(1)

sbmlns = SBMLNamespaces(3,1)

check(model.setTimeUnits("second"), 'set model-wide time units')
check(model.setExtentUnits("mole"), 'set model units of extent')
check(model.setSubstanceUnits('mole'), 'set model substance units')


per_second = model.createUnitDefinition()
check(per_second, 'create unit definition')
check(per_second.setId('per_second'), 'set unit definition id')
unit = per_second.createUnit()
check(unit, 'create unit on per_second')
check(unit.setKind(UNIT_KIND_SECOND), 'set unit kind')
check(unit.setExponent(-1), 'set unit exponent')
check(unit.setScale(0), 'set unit scale')
check(unit.setMultiplier(1), 'set unit multiplier')

comp = model.createCompartment()
check(comp,'Create comp compartment')
check(comp.setId('cell'), 'Set comp id')
check(comp.setName('cell'),'Set comp name')
check(comp.setSize(1),'set comp size')
check(comp.setUnits('litre'),'set comp units')
check(comp.setConstant(True),'set comp constant')

E = model.createSpecies()
check(E,'created E species')
check(E.setId('E'),'set E ID')
check(E.setName('E'),'set E name')
check(E.setCompartment('cell'),'set E compartment')
check(E.setInitialAmount(5e-1),'set E initial amount')
check(E.setConstant(False),'set E constant')
check(E.setBoundaryCondition(False),'set boundary E condition false')
check(E.setSubstanceUnits('mole'),'set substance units E')
check(E.setHasOnlySubstanceUnits(False),'set has only substance units E')

S = model.createSpecies()
check(S,'created S species')
check(S.setId('S'),'set S ID')
check(S.setName('S'),'set S name')
check(S.setCompartment('cell'),'set S compartment')
check(S.setInitialAmount(1e-2),'set S initial amount')
check(S.setConstant(False),'set S constant')
check(S.setBoundaryCondition(False),'set boundary S condition false')
check(S.setSubstanceUnits('mole'),'set substance units S')
check(S.setHasOnlySubstanceUnits(False),'set has only substance units S')

ES = model.createSpecies()
check(ES,'created ES species')
check(ES.setId('ES'),'set ES ID')
check(ES.setName('ES'),'set ES name')
check(ES.setCompartment('cell'),'set ES compartment')
check(ES.setInitialAmount(0),'set ES initial amount')
check(ES.setConstant(False),'set ES constant')
check(ES.setBoundaryCondition(False),'set boundary ES condition false')
check(ES.setSubstanceUnits('mole'),'set substance units ES')
check(ES.setHasOnlySubstanceUnits(False),'set has only substance units ES')

P = model.createSpecies()
check(P,'created P species')
check(P.setId('P'),'set P ID')
check(P.setName('P'),'set P name')
check(P.setCompartment('cell'),'set P compartment')
check(P.setInitialAmount(0),'set P initial amount')
check(P.setConstant(False),'set P constant')
check(P.setBoundaryCondition(False),'set boundary P condition false')
check(P.setSubstanceUnits('mole'),'set substance units P')
check(P.setHasOnlySubstanceUnits(False),'set has only substance units P')

koff = model.createParameter()
check(koff,'created koff parameter')
check(koff.setId('koff'),'set koff id')
check(koff.setName('koff'),'set koff name')
check(koff.setValue(0.2),'set koff value')
check(koff.setConstant(False),'set koff constant')
check(koff.setUnits('per_second'),'set unit koff')

kon = model.createParameter()
check(kon,'created  kon parameter')
check(kon.setId('kon'),'set  kon id')
check(kon.setName('kon'),'set kon name')
check(kon.setValue(100),'set kon value')
check(kon.setConstant(False),'set kon constant')
check(kon.setUnits('per_second'),'set unit kon')

kcat = model.createParameter()
check(kcat,'created kcat parameter')
check(kcat.setId('kcat'),'set kcat id')
check(kcat.setName('kcat'),'set kcat name')
check(kcat.setValue(0.1),'set kcat value')
check(kcat.setConstant(False),'set kcat constant')
check(kcat.setUnits('per_second'),'set unit kcat')

rxn_enz = ListOfReactions(sbmlns)
check(rxn_enz,'created a list of reactions for enzymatic reactions')

veq = model.createReaction()
check(veq, 'create reaction')
check(veq.setId('veq'), 'set reaction id')
check(veq.setReversible(True), 'set reaction reversibility flag')
check(veq.setFast(False), 'set reaction "fast" attribute')

species_ref1 = veq.createReactant()
check(species_ref1, 'create reactant')
check(species_ref1.setSpecies('E'), 'assign reactant species')
check(species_ref1.setConstant(False), 'set "constant" on species ref 1')
check(species_ref1.setStoichiometry(1), 'set stoich of ref1')

species_ref2 = veq.createReactant()
check(species_ref2, 'create reactant')
check(species_ref2.setSpecies('S'), 'assign reactant species')
check(species_ref2.setConstant(False), 'set "constant" on species ref 2')
check(species_ref2.setStoichiometry(1), 'set stoich of ref2')

species_ref3 = veq.createProduct()
check(species_ref3, 'create product')
check(species_ref3.setSpecies('ES'), 'assign product species')
check(species_ref3.setConstant(False), 'set "constant" on species ref 3')
check(species_ref3.setStoichiometry(1), 'set stoich of ref3')

math_ast = parseFormula('kon * E * S - koff * ES')
check(math_ast, 'create AST for rate expression')

kinetic_law_veq = veq.createKineticLaw()
check(kinetic_law_veq, 'create kinetic law')
check(kinetic_law_veq.setMath(math_ast), 'set math on kinetic law')

#Reaction vcat

vcat = model.createReaction()
check(vcat, 'create reaction')
check(vcat.setId('vcat'), 'set reaction id')
check(vcat.setReversible(False), 'set reaction reversibility flag')
check(vcat.setFast(False), 'set reaction "fast" attribute')

species_ref1_vcat = vcat.createReactant()
check(species_ref1_vcat, 'create reactant')
check(species_ref1_vcat.setSpecies('ES'), 'assign reactant species')
check(species_ref1_vcat.setConstant(False), 'set "constant" False on species ref 1_vcat')
check(species_ref1_vcat.setStoichiometry(1), 'set stoich of ref1_vcat')

species_ref2_vcat = vcat.createProduct()
check(species_ref2_vcat, 'create product')
check(species_ref2_vcat.setSpecies('E'), 'assign product species')
check(species_ref2_vcat.setConstant(False), 'set "constant" False on species ref 2_vcat')
check(species_ref2_vcat.setStoichiometry(1), 'set stoich of ref2_vcat')

species_ref3_vcat = vcat.createProduct()
check(species_ref3_vcat, 'create product')
check(species_ref3_vcat.setSpecies('P'), 'assign product species')
check(species_ref3_vcat.setConstant(False), 'set "constant" False on species ref 3_vcat')
check(species_ref3_vcat.setStoichiometry(1), 'set stoich of ref3_vcat')

math_ast_vcat = parseFormula('kcat * ES')
check(math_ast_vcat, 'create AST for rate expression')

kinetic_law_vcat = vcat.createKineticLaw()
check(kinetic_law_vcat, 'create kinetic law')
check(kinetic_law_vcat.setMath(math_ast_vcat), 'set math on kinetic law')


writeSBML(sbmlDoc,"models/EnzyModel.xml")
import bioscrape
m = bioscrape.types.read_model_from_sbml('models/EnzyModel.xml')
s = bioscrape.simulator.ModelCSimInterface(m)
s.py_prep_deterministic_simulation()
s.py_set_initial_time(0)

sim = bioscrape.simulator.DeterministicSimulator()
timepoints = np.linspace(0,100,1000)
result = sim.py_simulate(s,timepoints)
plt.plot(timepoints,result.py_get_result())
plt.legend(m.get_species_list())
plt.show()