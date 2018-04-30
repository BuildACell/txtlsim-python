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

inp_IFFL = sbmlDoc.createNewSpecies('inp_IFFL','inp_IFFL','cell',50,False,False,'count',False)
DA_IFFL = sbmlDoc.createNewSpecies('DA_IFFL','DA_IFFL','cell',50,False,False,'count',False)
C1_IFFL = sbmlDoc.createNewSpecies('C1_IFFL','C1_IFFL','cell',0,False,False,'count',False)

mA_IFFL = sbmlDoc.createNewSpecies('mA_IFFL','mA_IFFL','cell',0,False,False,'count',False)

pA_IFFL = sbmlDoc.createNewSpecies('pA_IFFL','pA_IFFL','cell',0,False,False,'count',False)

C2_IFFL = sbmlDoc.createNewSpecies('C2_IFFL','C2_IFFL','cell',0,False,False,'count',False)
DB_IFFL = sbmlDoc.createNewSpecies('DB_IFFL','DB_IFFL','cell',50,False,False,'count',False)

mB_IFFL = sbmlDoc.createNewSpecies('mB_IFFL','mB_IFFL','cell',0,False,False,'count',False)
pB_IFFL = sbmlDoc.createNewSpecies('pB_IFFL','pB_IFFL','cell',0,False,False,'count',False)

C3_IFFL = sbmlDoc.createNewSpecies('C3_IFFL','C3_IFFL','cell',0,False,False,'count',False)
DC_IFFL = sbmlDoc.createNewSpecies('DC_IFFL','DC_IFFL','cell',50,False,False,'count',False)

C4_IFFL = sbmlDoc.createNewSpecies('C4_IFFL','C4_IFFL','cell',0,False,False,'count',False)

C5_IFFL = sbmlDoc.createNewSpecies('C5_IFFL','C5_IFFL','cell',0,False,False,'count',False)

C6_IFFL = sbmlDoc.createNewSpecies('C6_IFFL','C6_IFFL','cell',0,False,False,'count',False)

mC_IFFL = sbmlDoc.createNewSpecies('mC_IFFL','mC_IFFL','cell',0,False,False,'count',False)

out_IFFL = sbmlDoc.createNewSpecies('out_IFFL','out_IFFL','cell',0,False,False,'count',False)

k1f = sbmlDoc.createNewParameter('k1f','k1f',1,False,'per_second')
k1r = sbmlDoc.createNewParameter('k1r','k1r',1,False,'per_second')

k2f = sbmlDoc.createNewParameter('k2f','k2f',1,False,'per_second')

k3f = sbmlDoc.createNewParameter('k3f','k3f',1,False,'per_second')

k4f = sbmlDoc.createNewParameter('k4f','k4f',1,False,'per_second')

k5f = sbmlDoc.createNewParameter('k5f','k5f',1,False,'per_second')

k6f = sbmlDoc.createNewParameter('k6f','k6f',1,False,'per_second')
k6r = sbmlDoc.createNewParameter('k6r','k6r',1,False,'per_second')

k7f = sbmlDoc.createNewParameter('k7f','k7f',1,False,'per_second')

k8f = sbmlDoc.createNewParameter('k8f','k8f',1,False,'per_second')

k9f = sbmlDoc.createNewParameter('k9f','k9f',1,False,'per_second')

k10f = sbmlDoc.createNewParameter('k10f','k10f',1,False,'per_second')

k11f = sbmlDoc.createNewParameter('k11f','k11f',1,False,'per_second')
k11r = sbmlDoc.createNewParameter('k11r','k11r',1,False,'per_second')

k12f = sbmlDoc.createNewParameter('k12f','k12f',1,False,'per_second')
k12r = sbmlDoc.createNewParameter('k12r','k12r',1,False,'per_second')

k13f = sbmlDoc.createNewParameter('k13f','k13f',1,False,'per_second')
k13r = sbmlDoc.createNewParameter('k13r','k13r',1,False,'per_second')

k14f = sbmlDoc.createNewParameter('k14f','k14f',1,False,'per_second')
k14r = sbmlDoc.createNewParameter('k14r','k14r',1,False,'per_second')

k15f = sbmlDoc.createNewParameter('k15f','k15f',1,False,'per_second')

k16f = sbmlDoc.createNewParameter('k16f','k16f',1,False,'per_second')

k17f = sbmlDoc.createNewParameter('k17f','k17f',1,False,'per_second')

k18f = sbmlDoc.createNewParameter('k18f','k18f',1,False,'per_second')

r1 = NewReaction(sbmlDoc.createNewReaction('r1',True,False))
sref1_inp_IFFL = r1.createNewReactant('inp_IFFL',False,1)
sref1_DA_IFFL = r1.createNewReactant('DA_IFFL',False,1)
sref1_C1_IFFL = r1.createNewProduct('C1_IFFL',False,1)
math_r1 = createMath('k1f * inp_IFFL * DA_IFFL - k1r * C1_IFFL')
r1_rate =  r1.createRate(math_r1)


r2 = NewReaction(sbmlDoc.createNewReaction('r2',False,False))
sref2_C1_IFFL =  r2.createNewReactant('C1_IFFL',False,1)
sref2_C1_IFFL = r2.createNewProduct('C1_IFFL',False,1)
sref2_mA_IFFL = r2.createNewProduct('mA_IFFL',False,1)
math_r2 = createMath('k2f * C1_IFFL')
r2_rate = r2.createRate(math_r2)

r3 = NewReaction(sbmlDoc.createNewReaction('r3',False,False))
sref3_mA_IFFL = r3.createNewReactant('mA_IFFL',False,1)
sref3_mA_IFFL = r3.createNewProduct('mA_IFFL',False,1)
sref3_pA_IFFL = r3.createNewProduct('pA_IFFL',False,1)
math_r3 = createMath('k3f * mA_IFFL')
r3_rate = r3.createRate(math_r3)

r4 = NewReaction(sbmlDoc.createNewReaction('r4',False,False))
sref4_mA_IFFL = r4.createNewReactant('mA_IFFL',False,1)
math_r4 = createMath('k4f * mA_IFFL')
r4_rate = r4.createRate(math_r4)

r5 = NewReaction(sbmlDoc.createNewReaction('r5',False,False))
sref4_pA_IFFL = r5.createNewReactant('pA_IFFL',False,1)
math_r5 = createMath('k5f * pA_IFFL')
r5_rate = r5.createRate(math_r5)

r6 = NewReaction(sbmlDoc.createNewReaction('r6',True,False))
sref5_pA_IFFL = r6.createNewReactant('pA_IFFL',False,1)
sref5_DB_IFFL = r6.createNewReactant('DB_IFFL',False,1)
sref5_C2_IFFL = r6.createNewProduct('C2_IFFL',False,1)
math_r6 = createMath('k6f * pA_IFFL * DB_IFFL - k6r * C2_IFFL')
r6_rate = r6.createRate(math_r6)

r7 = NewReaction(sbmlDoc.createNewReaction('r7',False,False))
sref6_C2_IFFL = r7.createNewReactant('C2_IFFL',False,1)
sref6_C2_IFFL = r7.createNewProduct('C2_IFFL',False,1)
sref6_mB_IFFL = r7.createNewProduct('mB_IFFL',False,1)
math_r7 = createMath('k7f * C2_IFFL')
r7_rate = r7.createRate(math_r7)

r8 = NewReaction(sbmlDoc.createNewReaction('r8',False,False))
sref6_mB_IFFL = r8.createNewReactant('mB_IFFL',False,1)
sref6_mB_IFFL = r8.createNewProduct('mB_IFFL',False,1)
sref6_pB_IFFL = r8.createNewProduct('pB_IFFL',False,1)
math_r8 = createMath('k8f * mB_IFFL')
r8_rate = r8.createRate(math_r8)

r9 = NewReaction(sbmlDoc.createNewReaction('r9',False,False))
sref6_mB_IFFL = r9.createNewReactant('mB_IFFL',False,1)
math_r9 = createMath('k9f * mB_IFFL')
r9_rate = r9.createRate(math_r9)

r10 = NewReaction(sbmlDoc.createNewReaction('r10',False,False))
sref6_pB_IFFL = r10.createNewReactant('pB_IFFL',False,1)
math_r10 = createMath('k10f * pB_IFFL')
r10_rate = r10.createRate(math_r10)

r11 = NewReaction(sbmlDoc.createNewReaction('r11',True,False))
sref7_pB_IFFL = r11.createNewReactant('pB_IFFL',False,1)
sref7_DC_IFFL = r11.createNewReactant('DC_IFFL',False,1)
sref7_C3_IFFL = r11.createNewProduct('C3_IFFL',False,1)
math_r11 = createMath('k11f * pB_IFFL * DC_IFFL - k11r * C3_IFFL')
r11_rate = r11.createRate(math_r11)

r12 = NewReaction(sbmlDoc.createNewReaction('r12',True,False))
sref7_pA_IFFL = r12.createNewReactant('pA_IFFL',False,1)
sref7_DC_IFFL = r12.createNewReactant('DC_IFFL',False,1)
sref7_C4_IFFL = r12.createNewProduct('C4_IFFL',False,1)
math_r12 = createMath('k12f * pA_IFFL * DC_IFFL - k12r * C4_IFFL')
r12_rate = r12.createRate(math_r12)

r13 = NewReaction(sbmlDoc.createNewReaction('r13',True,False))
sref7_pA_IFFL = r13.createNewReactant('pA_IFFL',False,1)
sref7_C3_IFFL = r13.createNewReactant('C3_IFFL',False,1)
sref7_C5_IFFL = r13.createNewProduct('C5_IFFL',False,1)
math_r13 = createMath('k13f * pA_IFFL * C3_IFFL - k13r * C5_IFFL')
r13_rate = r13.createRate(math_r13)

r14 = NewReaction(sbmlDoc.createNewReaction('r14',True,False))
sref7_pB_IFFL = r14.createNewReactant('pB_IFFL',False,1)
sref7_C4_IFFL = r14.createNewReactant('C4_IFFL',False,1)
sref7_C6_IFFL = r14.createNewProduct('C6_IFFL',False,1)
math_r14 = createMath('k14f * pB_IFFL * C4_IFFL - k14r * C6_IFFL')
r14_rate = r14.createRate(math_r14)

r15 = NewReaction(sbmlDoc.createNewReaction('r15',False,False))
sref8_C4_IFFL = r15.createNewReactant('C4_IFFL',False,1)
sref8_C4_IFFL = r15.createNewProduct('C4_IFFL',False,1)
sref8_mC_IFFL = r15.createNewProduct('mC_IFFL',False,1)
math_r15 = createMath('k15f * C4_IFFL')
r15_rate = r15.createRate(math_r15)

r16 = NewReaction(sbmlDoc.createNewReaction('r16',False,False))
sref8_mC_IFFL = r16.createNewReactant('mC_IFFL',False,1)
sref8_mC_IFFL = r16.createNewProduct('mC_IFFL',False,1)
sref8_out_IFFL = r16.createNewProduct('out_IFFL',False,1)
math_r16 = createMath('k16f * mC_IFFL')
r16_rate = r16.createRate(math_r16)

r17 = NewReaction(sbmlDoc.createNewReaction('r17',False,False))
sref8_mC_IFFL = r17.createNewReactant('mC_IFFL',False,1)
math_r17 = createMath('k17f * mC_IFFL')
r17_rate = r17.createRate(math_r17)

r18 = NewReaction(sbmlDoc.createNewReaction('r18',False,False))
sref8_out_IFFL = r18.createNewReactant('out_IFFL',False,1)
math_r18 = createMath('k18f * out_IFFL')
r18_rate = r18.createRate(math_r18)

# Write SBML file in XML
writeSBML(sbmlDoc.getNewDocument(),"models/IFFL_sbmlNew.xml")

# Simulate 
import bioscrape
m = bioscrape.types.read_model_from_sbml('models/IFFL_sbmlNew.xml')
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