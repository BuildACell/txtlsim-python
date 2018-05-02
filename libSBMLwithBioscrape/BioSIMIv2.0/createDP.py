#%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib as mpl

#%config InlineBackend.figure_f.ormats=['svg']

mpl.rc('axes', prop_cycle=(mpl.cycler('color', ['r', 'k', 'b','g','y','m','c']) ))

mpl.rc('xtick', labelsize=12) 
mpl.rc('ytick', labelsize=12)


import numpy as np

# Code for simple gene expression without_DP delay

# Import relevant types
# from bioscrape.types import Model
# from bioscrape.simulator import DeterministicSimulator, SSASimulator
# from bioscrape.simulator import ModelCSimInterface

from libsbml import *
import libsbml 
from modules.Subsystem import *
from modules.NewReaction import *

try:
   sbmlDoc1 = SBMLDocument(3, 1)
except ValueError:
   print('Could not create SBMLDocument object')
   sys.exit(1)
 
 # Create a Model object inside the SBMLDocument object and set its
 # identifier, checking the returned values.  The call to setId() returns a
 # status code to indicate whether the assignment was successful.
sbmlDoc = Subsystem(sbmlDoc1)
model = sbmlDoc.createNewModel("seconds","mole","count")
per_second = model.createUnitDefinition()
check(per_second, 'create unit definition')
check(per_second.setId('per_second'), 'set unit definition id')
unit = per_second.createUnit()
check(unit, 'create unit on per_second')
check(unit.setKind(UNIT_KIND_SECOND), 'set unit kind')
check(unit.setExponent(-1), 'set unit exponent')
check(unit.setScale(0), 'set unit scale')
check(unit.setMultiplier(1), 'set unit multiplier')

comp = sbmlDoc.createNewCompartment('cell','cell',1,'litre',True)
comp = sbmlDoc.createNewCompartment('cell1','cell1',1,'litre',True)

inp_DP = sbmlDoc.createNewSpecies( 'inp_DP','inp_DP','cell',50,False,False,'count',False)
X_DP = sbmlDoc.createNewSpecies( 'X_DP','X_DP','cell',50,False,False,'count',False)
C1_DP = sbmlDoc.createNewSpecies( 'C1_DP','C1_DP','cell',0,False,False,'count',False)
Xp_DP = sbmlDoc.createNewSpecies( 'Xp_DP','Xp_DP','cell',0,False,False,'count',False)
E_DP = sbmlDoc.createNewSpecies( 'E_DP','E_DP','cell',50,False,False,'count',False)
C2_DP = sbmlDoc.createNewSpecies( 'C2_DP','C2_DP','cell',0,False,False,'count',False)
C3_DP = sbmlDoc.createNewSpecies( 'C3_DP','C3_DP','cell',0,False,False,'count',False)
out_DP = sbmlDoc.createNewSpecies( 'out_DP','out_DP','cell',0,False,False,'count',False)
C4_DP = sbmlDoc.createNewSpecies( 'C4_DP','C4_DP','cell',0,False,False,'count',False)

k1f = sbmlDoc.createNewParameter( 'k1f','k1f',1,False,'per_second')
k1r = sbmlDoc.createNewParameter( 'k1r','k1r',1,False,'per_second')

k2f = sbmlDoc.createNewParameter( 'k2f','k2f',1,False,'per_second')

k3f = sbmlDoc.createNewParameter( 'k3f','k3f',1,False,'per_second')
k3r = sbmlDoc.createNewParameter( 'k3r','k3r',1,False,'per_second')

k4f = sbmlDoc.createNewParameter( 'k4f','k4f',1,False,'per_second')

k5f = sbmlDoc.createNewParameter( 'k5f','k5f',1,False,'per_second')
k5r = sbmlDoc.createNewParameter( 'k5r','k5r',1,False,'per_second')

k6f = sbmlDoc.createNewParameter( 'k6f','k6f',1,False,'per_second')

k7f = sbmlDoc.createNewParameter( 'k7f','k7f',1,False,'per_second')
k7r = sbmlDoc.createNewParameter( 'k7r','k7r',1,False,'per_second')

k8f = sbmlDoc.createNewParameter( 'k8f','k8f',1,False,'per_second')

r1 = NewReaction(sbmlDoc.createNewReaction('r1',True,False))   
sref1_inp_DP = r1.createNewReactant('inp_DP',False,1)
sref1_X_DP = r1.createNewReactant('X_DP',False,1)
sref1_C1_DP = r1.createNewProduct('C1_DP',False,1)
math_r1 = createMath('k1f * inp_DP * X_DP - k1r * C1_DP')
r1_rate = r1.createRate(math_r1)


r2 = NewReaction(sbmlDoc.createNewReaction('r2',False,False))
sref2_C1_DP = r2.createNewReactant('C1_DP',False,1)
sref2_inp_DP = r2.createNewProduct('inp_DP',False,1)
sref2_Xp_DP = r2.createNewProduct('Xp_DP',False,1)
math_r2 = createMath('k2f * C1_DP')
r2_rate = r2.createRate(math_r2)

r3 = NewReaction(sbmlDoc.createNewReaction('r3',True,False))
sref3_E_DP = r3.createNewReactant('E_DP',False,1)
sref3_Xp_DP = r3.createNewReactant('Xp_DP',False,1)
sref3_C2_DP = r3.createNewProduct('C2_DP',False,1)
math_r3 = createMath('k3f * E_DP * Xp_DP - k3r * C2_DP')
r3_rate = r3.createRate(math_r3)

r4 = NewReaction(sbmlDoc.createNewReaction('r4',False,False))
sref4_C2_DP = r4.createNewReactant('C2_DP',False,1)
sref4_E_DP = r4.createNewProduct('E_DP',False,1)
sref4_X_DP = r4.createNewProduct('X_DP',False,1)
math_r4 = createMath('k4f * C2_DP')
r4_rate = r4.createRate(math_r4)

r5 = NewReaction(sbmlDoc.createNewReaction('r5',True,False))
sref5_inp_DP = r5.createNewReactant('inp_DP',False,1)
sref5_Xp_DP = r5.createNewReactant('Xp_DP',False,1)
sref5_C3_DP = r5.createNewProduct('C3_DP',False,1)
math_r5 = createMath('k5f * inp_DP * Xp_DP - k5r * C3_DP')
r5_rate = r5.createRate(math_r5)

r6 = NewReaction(sbmlDoc.createNewReaction('r6',False,False))
sref6_C3_DP = r6.createNewReactant('C3_DP',False,1)
sref6_out_DP = r6.createNewProduct('out_DP',False,1)
sref6_inp_DP = r6.createNewProduct('inp_DP',False,1)
math_r6 = createMath('k6f * C3_DP')
r6_rate = r6.createRate(math_r6)

r7 = NewReaction(sbmlDoc.createNewReaction('r7',True,False))
sref7_E_DP = r7.createNewReactant('E_DP',False,1)
sref7_out_DP = r7.createNewReactant('out_DP',False,1)
sref7_C4_DP = r7.createNewProduct('C4_DP',False,1)
math_r7 = createMath('k7f * E_DP * out_DP - k7r * C4_DP')
r7_rate = r7.createRate(math_r7)

r8 = NewReaction(sbmlDoc.createNewReaction('r8',False,False))
sref8_C4_DP = r8.createNewReactant('C4_DP',False,1)
sref8_Xp_DP = r8.createNewProduct('Xp_DP',False,1)
sref8_E_DP = r8.createNewProduct('E_DP',False,1)
math_r8 = createMath('k8f * C4_DP')
r8_rate = r8.createRate(math_r8)

# Simulate 
writeSBML(sbmlDoc.getNewDocument(),'models/DP_sbml.xml')
# print(sbmlDoc.getNewDocument().getModel().getListOfReactions())
import bioscrape
m = bioscrape.types.read_model_from_sbml('models/DP_sbml.xml')
s = bioscrape.simulator.ModelCSimInterface(m)
s.py_prep_deterministic_simulation()
s.py_set_initial_time(0)

inp_DP_ind = m.get_species_index('inp_DP')
out_DP_ind = m.get_species_index('out_DP')
sim = bioscrape.simulator.DeterministicSimulator()
timepoints = np.linspace(0,100,1000)
result = sim.py_simulate(s,timepoints)
# print(result.py_get_result()[1])
plt.xlabel('Time')
plt.ylabel('out_DP/inp_DP species')
plt.plot(timepoints,result.py_get_result()[:,inp_DP_ind])
plt.plot(timepoints,result.py_get_result()[:,out_DP_ind])
plt.legend([m.get_species_list()[inp_DP_ind],m.get_species_list()[out_DP_ind]])
plt.show()