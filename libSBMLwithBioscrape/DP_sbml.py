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
from simpleSBMLfunctions import *


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
check(model.setSubstanceUnits('count'), 'set model substance units')


per_second = model.createUnitDefinition()
check(per_second, 'create unit definition')
check(per_second.setId('per_second'), 'set unit definition id')
unit = per_second.createUnit()
check(unit, 'create unit on per_second')
check(unit.setKind(UNIT_KIND_SECOND), 'set unit kind')
check(unit.setExponent(-1), 'set unit exponent')
check(unit.setScale(0), 'set unit scale')
check(unit.setMultiplier(1), 'set unit multiplier')

comp = createNewCompartment(model,'cell','cell',1,'litre',True)

inp = createNewSpecies(model,'inp','inp','cell',50,False,False,'count',False)
X = createNewSpecies(model,'X','X','cell',50,False,False,'count',False)
C1 = createNewSpecies(model,'C1','C1','cell',0,False,False,'count',False)
Xp = createNewSpecies(model,'Xp','Xp','cell',0,False,False,'count',False)
E = createNewSpecies(model,'E','E','cell',50,False,False,'count',False)
C2 = createNewSpecies(model,'C2','C2','cell',0,False,False,'count',False)
C3 = createNewSpecies(model,'C3','C3','cell',0,False,False,'count',False)
out = createNewSpecies(model,'out','out','cell',0,False,False,'count',False)
C4 = createNewSpecies(model,'C4','C4','cell',0,False,False,'count',False)

k1f = createNewParameter(model,'k1f','k1f',1,False,'per_second')
k1r = createNewParameter(model,'k1r','k1r',1,False,'per_second')

k2f = createNewParameter(model,'k2f','k2f',1,False,'per_second')

k3f = createNewParameter(model,'k3f','k3f',1,False,'per_second')
k3r = createNewParameter(model,'k3r','k3r',1,False,'per_second')

k4f = createNewParameter(model,'k4f','k4f',1,False,'per_second')

k5f = createNewParameter(model,'k5f','k5f',1,False,'per_second')
k5r = createNewParameter(model,'k5r','k5r',1,False,'per_second')

k6f = createNewParameter(model,'k6f','k6f',1,False,'per_second')

k7f = createNewParameter(model,'k7f','k7f',1,False,'per_second')
k7r = createNewParameter(model,'k7r','k7r',1,False,'per_second')

k8f = createNewParameter(model,'k8f','k8f',1,False,'per_second')

r1 = createNewReaction(model,'r1',True,False)
sref1_inp = createNewReactant(r1,'inp',False,1)
sref1_X = createNewReactant(r1,'X',False,1)
sref1_C1 = createNewProduct(r1,'C1',False,1)
math_r1 = createMath('k1f * inp * X - k1r * C1')
r1_rate = createRate(r1,math_r1)


r2 = createNewReaction(model,'r2',False,False)
sref2_C1 = createNewReactant(r2,'C1',False,1)
sref2_inp = createNewProduct(r2,'inp',False,1)
sref2_Xp = createNewProduct(r2,'Xp',False,1)
math_r2 = createMath('k2f * C1')
r2_rate = createRate(r2,math_r2)

r3 = createNewReaction(model,'r3',True,False)
sref3_E = createNewReactant(r3,'E',False,1)
sref3_Xp = createNewReactant(r3,'Xp',False,1)
sref3_C2 = createNewProduct(r3,'C2',False,1)
math_r3 = createMath('k3f * E * Xp - k3r * C2')
r3_rate = createRate(r3,math_r3)

r4 = createNewReaction(model,'r4',False,False)
sref4_C2 = createNewReactant(r4,'C2',False,1)
sref4_E = createNewProduct(r4,'E',False,1)
sref4_X = createNewProduct(r4,'X',False,1)
math_r4 = createMath('k4f * C2')
r4_rate = createRate(r4,math_r4)

r5 = createNewReaction(model,'r5',True,False)
sref5_inp = createNewReactant(r5,'inp',False,1)
sref5_Xp = createNewReactant(r5,'Xp',False,1)
sref5_C3 = createNewProduct(r5,'C3',False,1)
math_r5 = createMath('k5f * inp * Xp - k5r * C3')
r5_rate = createRate(r5,math_r5)

r6 = createNewReaction(model,'r6',False,False)
sref6_C3 = createNewReactant(r6,'C3',False,1)
sref6_out = createNewProduct(r6,'out',False,1)
sref6_inp = createNewProduct(r6,'inp',False,1)
math_r6 = createMath('k6f * C3')
r6_rate = createRate(r6,math_r6)

r7 = createNewReaction(model,'r7',True,False)
sref7_E = createNewReactant(r7,'E',False,1)
sref7_out = createNewReactant(r7,'out',False,1)
sref7_C4 = createNewProduct(r7,'C4',False,1)
math_r7 = createMath('k7f * E * out - k7r * C4')
r7_rate = createRate(r7,math_r7)

r8 = createNewReaction(model,'r8',False,False)
sref8_C4 = createNewReactant(r8,'C4',False,1)
sref8_Xp = createNewProduct(r8,'Xp',False,1)
sref8_E = createNewProduct(r8,'E',False,1)
math_r8 = createMath('k8f * C4')
r8_rate = createRate(r8,math_r8)

# Simulate 
writeSBML(sbmlDoc,"models/DP_sbml.xml")
import bioscrape
m = bioscrape.types.read_model_from_sbml('models/DP_sbml.xml')
s = bioscrape.simulator.ModelCSimInterface(m)
s.py_prep_deterministic_simulation()
s.py_set_initial_time(0)

inp_ind = m.get_species_index('inp')
out_ind = m.get_species_index('out')
sim = bioscrape.simulator.DeterministicSimulator()
timepoints = np.linspace(0,100,1000)
result = sim.py_simulate(s,timepoints)
# print(result.py_get_result()[1])
plt.xlabel('Time')
plt.ylabel('out/input species')
plt.plot(timepoints,result.py_get_result()[:,inp_ind])
plt.plot(timepoints,result.py_get_result()[:,out_ind])
plt.legend([m.get_species_list()[inp_ind],m.get_species_list()[out_ind]])
plt.show()