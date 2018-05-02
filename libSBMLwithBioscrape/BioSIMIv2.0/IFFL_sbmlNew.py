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

IFFL_k1f = sbmlDoc.createNewParameter('IFFL_k1f','IFFL_k1f',1,False,'per_second')
IFFL_k1r = sbmlDoc.createNewParameter('IFFL_k1r','IFFL_k1r',1,False,'per_second')

IFFL_k2f = sbmlDoc.createNewParameter('IFFL_k2f','IFFL_k2f',1,False,'per_second')

IFFL_k3f = sbmlDoc.createNewParameter('IFFL_k3f','IFFL_k3f',1,False,'per_second')

IFFL_k4f = sbmlDoc.createNewParameter('IFFL_k4f','IFFL_k4f',1,False,'per_second')

IFFL_k5f = sbmlDoc.createNewParameter('IFFL_k5f','IFFL_k5f',1,False,'per_second')

IFFL_k6f = sbmlDoc.createNewParameter('IFFL_k6f','IFFL_k6f',1,False,'per_second')
IFFL_k6r = sbmlDoc.createNewParameter('IFFL_k6r','IFFL_k6r',1,False,'per_second')

IFFL_k7f = sbmlDoc.createNewParameter('IFFL_k7f','IFFL_k7f',1,False,'per_second')

IFFL_k8f = sbmlDoc.createNewParameter('IFFL_k8f','IFFL_k8f',1,False,'per_second')

IFFL_k9f = sbmlDoc.createNewParameter('IFFL_k9f','IFFL_k9f',1,False,'per_second')

IFFL_k10f = sbmlDoc.createNewParameter('IFFL_k10f','IFFL_k10f',1,False,'per_second')

IFFL_k11f = sbmlDoc.createNewParameter('IFFL_k11f','IFFL_k11f',1,False,'per_second')
IFFL_k11r = sbmlDoc.createNewParameter('IFFL_k11r','IFFL_k11r',1,False,'per_second')

IFFL_k12f = sbmlDoc.createNewParameter('IFFL_k12f','IFFL_k12f',1,False,'per_second')
IFFL_k12r = sbmlDoc.createNewParameter('IFFL_k12r','IFFL_k12r',1,False,'per_second')

IFFL_k13f = sbmlDoc.createNewParameter('IFFL_k13f','IFFL_k13f',1,False,'per_second')
IFFL_k13r = sbmlDoc.createNewParameter('IFFL_k13r','IFFL_k13r',1,False,'per_second')

IFFL_k14f = sbmlDoc.createNewParameter('IFFL_k14f','IFFL_k14f',1,False,'per_second')
IFFL_k14r = sbmlDoc.createNewParameter('IFFL_k14r','IFFL_k14r',1,False,'per_second')

IFFL_k15f = sbmlDoc.createNewParameter('IFFL_k15f','IFFL_k15f',1,False,'per_second')

IFFL_k16f = sbmlDoc.createNewParameter('IFFL_k16f','IFFL_k16f',1,False,'per_second')

IFFL_k17f = sbmlDoc.createNewParameter('IFFL_k17f','IFFL_k17f',1,False,'per_second')

IFFL_k18f = sbmlDoc.createNewParameter('IFFL_k18f','IFFL_k18f',1,False,'per_second')

IFFL_r1 = NewReaction(sbmlDoc.createNewReaction('IFFL_r1',True,False))
sref1_inp_IFFL = IFFL_r1.createNewReactant('inp_IFFL',False,1)
sref1_DA_IFFL = IFFL_r1.createNewReactant('DA_IFFL',False,1)
sref1_C1_IFFL = IFFL_r1.createNewProduct('C1_IFFL',False,1)
math_r1 = createMath('IFFL_k1f * inp_IFFL * DA_IFFL - IFFL_k1r * C1_IFFL')
r1_rate =  IFFL_r1.createRate(math_r1)


IFFL_r2 = NewReaction(sbmlDoc.createNewReaction('IFFL_r2',False,False))
sref2_C1_IFFL =  IFFL_r2.createNewReactant('C1_IFFL',False,1)
sref2_C1_IFFL = IFFL_r2.createNewProduct('C1_IFFL',False,1)
sref2_mA_IFFL = IFFL_r2.createNewProduct('mA_IFFL',False,1)
math_r2 = createMath('IFFL_k2f * C1_IFFL')
r2_rate = IFFL_r2.createRate(math_r2)

IFFL_r3 = NewReaction(sbmlDoc.createNewReaction('IFFL_r3',False,False))
sref3_mA_IFFL = IFFL_r3.createNewReactant('mA_IFFL',False,1)
sref3_mA_IFFL = IFFL_r3.createNewProduct('mA_IFFL',False,1)
sref3_pA_IFFL = IFFL_r3.createNewProduct('pA_IFFL',False,1)
math_r3 = createMath('IFFL_k3f * mA_IFFL')
r3_rate = IFFL_r3.createRate(math_r3)

IFFL_r4 = NewReaction(sbmlDoc.createNewReaction('IFFL_r4',False,False))
sref4_mA_IFFL = IFFL_r4.createNewReactant('mA_IFFL',False,1)
math_r4 = createMath('IFFL_k4f * mA_IFFL')
r4_rate = IFFL_r4.createRate(math_r4)

IFFL_r5 = NewReaction(sbmlDoc.createNewReaction('IFFL_r5',False,False))
sref4_pA_IFFL = IFFL_r5.createNewReactant('pA_IFFL',False,1)
math_r5 = createMath('IFFL_k5f * pA_IFFL')
r5_rate = IFFL_r5.createRate(math_r5)

IFFL_r6 = NewReaction(sbmlDoc.createNewReaction('IFFL_r6',True,False))
sref5_pA_IFFL = IFFL_r6.createNewReactant('pA_IFFL',False,1)
sref5_DB_IFFL = IFFL_r6.createNewReactant('DB_IFFL',False,1)
sref5_C2_IFFL = IFFL_r6.createNewProduct('C2_IFFL',False,1)
math_r6 = createMath('IFFL_k6f * pA_IFFL * DB_IFFL - IFFL_k6r * C2_IFFL')
r6_rate = IFFL_r6.createRate(math_r6)

IFFL_r7 = NewReaction(sbmlDoc.createNewReaction('IFFL_r7',False,False))
sref6_C2_IFFL = IFFL_r7.createNewReactant('C2_IFFL',False,1)
sref6_C2_IFFL = IFFL_r7.createNewProduct('C2_IFFL',False,1)
sref6_mB_IFFL = IFFL_r7.createNewProduct('mB_IFFL',False,1)
math_r7 = createMath('IFFL_k7f * C2_IFFL')
r7_rate = IFFL_r7.createRate(math_r7)

IFFL_r8 = NewReaction(sbmlDoc.createNewReaction('IFFL_r8',False,False))
sref6_mB_IFFL = IFFL_r8.createNewReactant('mB_IFFL',False,1)
sref6_mB_IFFL = IFFL_r8.createNewProduct('mB_IFFL',False,1)
sref6_pB_IFFL = IFFL_r8.createNewProduct('pB_IFFL',False,1)
math_r8 = createMath('IFFL_k8f * mB_IFFL')
r8_rate = IFFL_r8.createRate(math_r8)

IFFL_r9 = NewReaction(sbmlDoc.createNewReaction('IFFL_r9',False,False))
sref6_mB_IFFL = IFFL_r9.createNewReactant('mB_IFFL',False,1)
math_r9 = createMath('IFFL_k9f * mB_IFFL')
r9_rate = IFFL_r9.createRate(math_r9)

IFFL_r10 = NewReaction(sbmlDoc.createNewReaction('IFFL_r10',False,False))
sref6_pB_IFFL = IFFL_r10.createNewReactant('pB_IFFL',False,1)
math_r10 = createMath('IFFL_k10f * pB_IFFL')
r10_rate = IFFL_r10.createRate(math_r10)

IFFL_r11 = NewReaction(sbmlDoc.createNewReaction('IFFL_r11',True,False))
sref7_pB_IFFL = IFFL_r11.createNewReactant('pB_IFFL',False,1)
sref7_DC_IFFL = IFFL_r11.createNewReactant('DC_IFFL',False,1)
sref7_C3_IFFL = IFFL_r11.createNewProduct('C3_IFFL',False,1)
math_r11 = createMath('IFFL_k11f * pB_IFFL * DC_IFFL - IFFL_k11r * C3_IFFL')
r11_rate = IFFL_r11.createRate(math_r11)

IFFL_r12 = NewReaction(sbmlDoc.createNewReaction('IFFL_r12',True,False))
sref7_pA_IFFL = IFFL_r12.createNewReactant('pA_IFFL',False,1)
sref7_DC_IFFL = IFFL_r12.createNewReactant('DC_IFFL',False,1)
sref7_C4_IFFL = IFFL_r12.createNewProduct('C4_IFFL',False,1)
math_r12 = createMath('IFFL_k12f * pA_IFFL * DC_IFFL - IFFL_k12r * C4_IFFL')
r12_rate = IFFL_r12.createRate(math_r12)

IFFL_r13 = NewReaction(sbmlDoc.createNewReaction('IFFL_r13',True,False))
sref7_pA_IFFL = IFFL_r13.createNewReactant('pA_IFFL',False,1)
sref7_C3_IFFL = IFFL_r13.createNewReactant('C3_IFFL',False,1)
sref7_C5_IFFL = IFFL_r13.createNewProduct('C5_IFFL',False,1)
math_r13 = createMath('IFFL_k13f * pA_IFFL * C3_IFFL - IFFL_k13r * C5_IFFL')
r13_rate = IFFL_r13.createRate(math_r13)

IFFL_r14 = NewReaction(sbmlDoc.createNewReaction('IFFL_r14',True,False))
sref7_pB_IFFL = IFFL_r14.createNewReactant('pB_IFFL',False,1)
sref7_C4_IFFL = IFFL_r14.createNewReactant('C4_IFFL',False,1)
sref7_C6_IFFL = IFFL_r14.createNewProduct('C6_IFFL',False,1)
math_r14 = createMath('IFFL_k14f * pB_IFFL * C4_IFFL - IFFL_k14r * C6_IFFL')
r14_rate = IFFL_r14.createRate(math_r14)

IFFL_r15 = NewReaction(sbmlDoc.createNewReaction('IFFL_r15',False,False))
sref8_C4_IFFL = IFFL_r15.createNewReactant('C4_IFFL',False,1)
sref8_C4_IFFL = IFFL_r15.createNewProduct('C4_IFFL',False,1)
sref8_mC_IFFL = IFFL_r15.createNewProduct('mC_IFFL',False,1)
math_r15 = createMath('IFFL_k15f * C4_IFFL')
r15_rate = IFFL_r15.createRate(math_r15)

IFFL_r16 = NewReaction(sbmlDoc.createNewReaction('IFFL_r16',False,False))
sref8_mC_IFFL = IFFL_r16.createNewReactant('mC_IFFL',False,1)
sref8_mC_IFFL = IFFL_r16.createNewProduct('mC_IFFL',False,1)
sref8_out_IFFL = IFFL_r16.createNewProduct('out_IFFL',False,1)
math_r16 = createMath('IFFL_k16f * mC_IFFL')
r16_rate = IFFL_r16.createRate(math_r16)

IFFL_r17 = NewReaction(sbmlDoc.createNewReaction('IFFL_r17',False,False))
sref8_mC_IFFL = IFFL_r17.createNewReactant('mC_IFFL',False,1)
math_r17 = createMath('IFFL_k17f * mC_IFFL')
r17_rate = IFFL_r17.createRate(math_r17)

IFFL_r18 = NewReaction(sbmlDoc.createNewReaction('IFFL_r18',False,False))
sref8_out_IFFL = IFFL_r18.createNewReactant('out_IFFL',False,1)
math_r18 = createMath('IFFL_k18f * out_IFFL')
r18_rate = IFFL_r18.createRate(math_r18)

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
timepoints = np.linspace(0,10,1000)
result = sim.py_simulate(s,timepoints)
# print(result.py_get_result()[1])
plt.xlabel('Time')
plt.ylabel('out_IFFL/inp_IFFL species')
plt.plot(timepoints,result.py_get_result()[:,inp_IFFL_ind])
plt.plot(timepoints,result.py_get_result()[:,out_IFFL_ind])
plt.legend([m.get_species_list()[inp_IFFL_ind],m.get_species_list()[out_IFFL_ind]])
plt.show()