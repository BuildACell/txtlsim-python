#%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib as mpl

#%config InlineBackend.figure_f.ormats=['svg']

mpl.rc('axes', prop_cycle=(mpl.cycler('color', ['r', 'k', 'b','g','y','m','c']) ))

mpl.rc('xtick', labelsize=12) 
mpl.rc('ytick', labelsize=12)


import numpy as np

# Code for simple gene expression without_IFFL delay

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

inp_IFFL = createNewSpecies(model,'inp_IFFL','inp_IFFL','cell',50,False,False,'count',False)
DA_IFFL = createNewSpecies(model,'DA_IFFL','DA_IFFL','cell',50,False,False,'count',False)
C1_IFFL = createNewSpecies(model,'C1_IFFL','C1_IFFL','cell',0,False,False,'count',False)

mA_IFFL = createNewSpecies(model,'mA_IFFL','mA_IFFL','cell',0,False,False,'count',False)

pA_IFFL = createNewSpecies(model,'pA_IFFL','pA_IFFL','cell',0,False,False,'count',False)

C2_IFFL = createNewSpecies(model,'C2_IFFL','C2_IFFL','cell',0,False,False,'count',False)
DB_IFFL = createNewSpecies(model,'DB_IFFL','DB_IFFL','cell',50,False,False,'count',False)

mB_IFFL = createNewSpecies(model,'mB_IFFL','mB_IFFL','cell',0,False,False,'count',False)
pB_IFFL = createNewSpecies(model,'pB_IFFL','pB_IFFL','cell',0,False,False,'count',False)

C3_IFFL = createNewSpecies(model,'C3_IFFL','C3_IFFL','cell',0,False,False,'count',False)
DC_IFFL = createNewSpecies(model,'DC_IFFL','DC_IFFL','cell',50,False,False,'count',False)

C4_IFFL = createNewSpecies(model,'C4_IFFL','C4_IFFL','cell',0,False,False,'count',False)

C5_IFFL = createNewSpecies(model,'C5_IFFL','C5_IFFL','cell',0,False,False,'count',False)

C6_IFFL = createNewSpecies(model,'C6_IFFL','C6_IFFL','cell',0,False,False,'count',False)

mC_IFFL = createNewSpecies(model,'mC_IFFL','mC_IFFL','cell',0,False,False,'count',False)

out_IFFL = createNewSpecies(model,'out_IFFL','out_IFFL','cell',0,False,False,'count',False)

k1f = createNewParameter(model,'k1f','k1f',1,False,'per_second')
k1r = createNewParameter(model,'k1r','k1r',1,False,'per_second')

k2f = createNewParameter(model,'k2f','k2f',1,False,'per_second')

k3f = createNewParameter(model,'k3f','k3f',1,False,'per_second')

k4f = createNewParameter(model,'k4f','k4f',1,False,'per_second')

k5f = createNewParameter(model,'k5f','k5f',1,False,'per_second')

k6f = createNewParameter(model,'k6f','k6f',1,False,'per_second')
k6r = createNewParameter(model,'k6r','k6r',1,False,'per_second')

k7f = createNewParameter(model,'k7f','k7f',1,False,'per_second')

k8f = createNewParameter(model,'k8f','k8f',1,False,'per_second')

k9f = createNewParameter(model,'k9f','k9f',1,False,'per_second')

k10f = createNewParameter(model,'k10f','k10f',1,False,'per_second')

k11f = createNewParameter(model,'k11f','k11f',1,False,'per_second')
k11r = createNewParameter(model,'k11r','k11r',1,False,'per_second')

k12f = createNewParameter(model,'k12f','k12f',1,False,'per_second')
k12r = createNewParameter(model,'k12r','k12r',1,False,'per_second')

k13f = createNewParameter(model,'k13f','k13f',1,False,'per_second')
k13r = createNewParameter(model,'k13r','k13r',1,False,'per_second')

k14f = createNewParameter(model,'k14f','k14f',1,False,'per_second')
k14r = createNewParameter(model,'k14r','k14r',1,False,'per_second')

k15f = createNewParameter(model,'k15f','k15f',1,False,'per_second')

k16f = createNewParameter(model,'k16f','k16f',1,False,'per_second')

k17f = createNewParameter(model,'k17f','k17f',1,False,'per_second')

k18f = createNewParameter(model,'k18f','k18f',1,False,'per_second')

r1 = createNewReaction(model,'r1',True,False)
sref1_inp_IFFL = createNewReactant(r1,'inp_IFFL',False,1)
sref1_DA_IFFL = createNewReactant(r1,'DA_IFFL',False,1)
sref1_C1_IFFL = createNewProduct(r1,'C1_IFFL',False,1)
math_r1 = createMath('k1f * inp_IFFL * DA_IFFL - k1r * C1_IFFL')
r1_rate = createRate(r1,math_r1)


r2 = createNewReaction(model,'r2',False,False)
sref2_C1_IFFL = createNewReactant(r2,'C1_IFFL',False,1)
sref2_C1_IFFL = createNewProduct(r2,'C1_IFFL',False,1)
sref2_mA_IFFL = createNewProduct(r2,'mA_IFFL',False,1)
math_r2 = createMath('k2f * C1_IFFL')
r2_rate = createRate(r2,math_r2)

r3 = createNewReaction(model,'r3',False,False)
sref3_mA_IFFL = createNewReactant(r3,'mA_IFFL',False,1)
sref3_mA_IFFL = createNewProduct(r3,'mA_IFFL',False,1)
sref3_pA_IFFL = createNewProduct(r3,'pA_IFFL',False,1)
math_r3 = createMath('k3f * mA_IFFL')
r3_rate = createRate(r3,math_r3)

r4 = createNewReaction(model,'r4',False,False)
sref4_mA_IFFL = createNewReactant(r4,'mA_IFFL',False,1)
math_r4 = createMath('k4f * mA_IFFL')
r4_rate = createRate(r4,math_r4)

r5 = createNewReaction(model,'r5',False,False)
sref4_pA_IFFL = createNewReactant(r5,'pA_IFFL',False,1)
math_r5 = createMath('k5f * pA_IFFL')
r5_rate = createRate(r5,math_r5)

r6 = createNewReaction(model,'r6',True,False)
sref5_pA_IFFL = createNewReactant(r6,'pA_IFFL',False,1)
sref5_DB_IFFL = createNewReactant(r6,'DB_IFFL',False,1)
sref5_C2_IFFL = createNewProduct(r6,'C2_IFFL',False,1)
math_r6 = createMath('k6f * pA_IFFL * DB_IFFL - k6r * C2_IFFL')
r6_rate = createRate(r6,math_r6)

r7 = createNewReaction(model,'r7',False,False)
sref6_C2_IFFL = createNewReactant(r7,'C2_IFFL',False,1)
sref6_C2_IFFL = createNewProduct(r7,'C2_IFFL',False,1)
sref6_mB_IFFL = createNewProduct(r7,'mB_IFFL',False,1)
math_r7 = createMath('k7f * C2_IFFL')
r7_rate = createRate(r7,math_r7)

r8 = createNewReaction(model,'r8',False,False)
sref6_mB_IFFL = createNewReactant(r8,'mB_IFFL',False,1)
sref6_mB_IFFL = createNewProduct(r8,'mB_IFFL',False,1)
sref6_pB_IFFL = createNewProduct(r8,'pB_IFFL',False,1)
math_r8 = createMath('k8f * mB_IFFL')
r8_rate = createRate(r8,math_r8)

r9 = createNewReaction(model,'r9',False,False)
sref6_mB_IFFL = createNewReactant(r9,'mB_IFFL',False,1)
math_r9 = createMath('k9f * mB_IFFL')
r9_rate = createRate(r9,math_r9)

r10 = createNewReaction(model,'r10',False,False)
sref6_pB_IFFL = createNewReactant(r10,'pB_IFFL',False,1)
math_r10 = createMath('k10f * pB_IFFL')
r10_rate = createRate(r10,math_r10)

r11 = createNewReaction(model,'r11',True,False)
sref7_pB_IFFL = createNewReactant(r11,'pB_IFFL',False,1)
sref7_DC_IFFL = createNewReactant(r11,'DC_IFFL',False,1)
sref7_C3_IFFL = createNewProduct(r11,'C3_IFFL',False,1)
math_r11 = createMath('k11f * pB_IFFL * DC_IFFL - k11r * C3_IFFL')
r11_rate = createRate(r11,math_r11)

r12 = createNewReaction(model,'r12',True,False)
sref7_pA_IFFL = createNewReactant(r12,'pA_IFFL',False,1)
sref7_DC_IFFL = createNewReactant(r12,'DC_IFFL',False,1)
sref7_C4_IFFL = createNewProduct(r12,'C4_IFFL',False,1)
math_r12 = createMath('k12f * pA_IFFL * DC_IFFL - k12r * C4_IFFL')
r12_rate = createRate(r12,math_r12)

r13 = createNewReaction(model,'r13',True,False)
sref7_pA_IFFL = createNewReactant(r13,'pA_IFFL',False,1)
sref7_C3_IFFL = createNewReactant(r13,'C3_IFFL',False,1)
sref7_C5_IFFL = createNewProduct(r13,'C5_IFFL',False,1)
math_r13 = createMath('k13f * pA_IFFL * C3_IFFL - k13r * C5_IFFL')
r13_rate = createRate(r13,math_r13)

r14 = createNewReaction(model,'r14',True,False)
sref7_pB_IFFL = createNewReactant(r14,'pB_IFFL',False,1)
sref7_C4_IFFL = createNewReactant(r14,'C4_IFFL',False,1)
sref7_C6_IFFL = createNewProduct(r14,'C6_IFFL',False,1)
math_r14 = createMath('k14f * pB_IFFL * C4_IFFL - k14r * C6_IFFL')
r14_rate = createRate(r14,math_r14)

r15 = createNewReaction(model,'r15',False,False)
sref8_C4_IFFL = createNewReactant(r15,'C4_IFFL',False,1)
sref8_C4_IFFL = createNewProduct(r15,'C4_IFFL',False,1)
sref8_mC_IFFL = createNewProduct(r15,'mC_IFFL',False,1)
math_r15 = createMath('k15f * C4_IFFL')
r15_rate = createRate(r15,math_r15)

r16 = createNewReaction(model,'r16',False,False)
sref8_mC_IFFL = createNewReactant(r16,'mC_IFFL',False,1)
sref8_mC_IFFL = createNewProduct(r16,'mC_IFFL',False,1)
sref8_out_IFFL = createNewProduct(r16,'out_IFFL',False,1)
math_r16 = createMath('k16f * mC_IFFL')
r16_rate = createRate(r16,math_r16)

r17 = createNewReaction(model,'r17',False,False)
sref8_mC_IFFL = createNewReactant(r17,'mC_IFFL',False,1)
math_r17 = createMath('k17f * mC_IFFL')
r17_rate = createRate(r17,math_r17)

r18 = createNewReaction(model,'r18',False,False)
sref8_out_IFFL = createNewReactant(r18,'out_IFFL',False,1)
math_r18 = createMath('k18f * out_IFFL')
r18_rate = createRate(r18,math_r18)

# Write SBML file in XML
writeSBML(sbmlDoc,"models/IFFL_sbml.xml")

# Simulate 
import bioscrape
m = bioscrape.types.read_model_from_sbml('models/IFFL_sbml.xml')
s = bioscrape.simulator.ModelCSimInterface(m)
s.py_prep_deterministic_simulation()
s.py_set_initial_time(0)

inp_IFFL_ind = m.get_species_index('inp_IFFL')
out_IFFL_ind = m.get_species_index('out_IFFL')
sim = bioscrape.simulator.DeterministicSimulator()
timepoints = np.linspace(0,100,1000)
result = sim.py_simulate(s,timepoints)
# print(result.py_get_result()[1])
plt.xlabel('Time')
plt.ylabel('out_IFFL/inp_IFFL species')
plt.plot(timepoints,result.py_get_result()[:,inp_IFFL_ind])
plt.plot(timepoints,result.py_get_result()[:,out_IFFL_ind])
plt.legend([m.get_species_list()[inp_IFFL_ind],m.get_species_list()[out_IFFL_ind]])
plt.show()