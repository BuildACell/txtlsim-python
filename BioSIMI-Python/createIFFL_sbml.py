from modules.Subsystem import *
from modules.SimpleModel import *
from modules.NewReaction import *

IFFL_doc = createSubsystemDoc(3,1)
# Create IFFL object of Subsystem class
IFFL = Subsystem(IFFL_doc)
# Create a Model object inside the Subsystem object 
# Usage - self.createNewModel(modelID, modelTimeUnits, modelExtentUnits, modelSubstanceUnits)

model = IFFL.createNewModel('IFFLmodel', 'second','mole','count')

# Create the model_obj of the SimpleModel class to use the functions helpful in creating the model from scratch easily
model_obj = SimpleModel(model)

# Create a unit definition for rate constants
# Usage - self.createNewUnitDefinition(unitId, unitKind, unitExponent, unitScale, unitMultiplier)
# Returns a UnitDefinition object
per_second = model_obj.createNewUnitDefinition('per_second',UNIT_KIND_SECOND, -1, 0, 1)
count = model_obj.createNewUnitDefinition('count',UNIT_KIND_DIMENSIONLESS, 1, 0, 1)

# Create a compartment for the species 
# Usage - self.createNewCompartment(Id, Name, Size, Units, isConstant)
# Returns a Compartment object
comp = model_obj.createNewCompartment('cell','cell',1,'litre',True)

# Create all species one by one. Only need one call to createNewSpecies to create a species 
# Usage - self.createNewSpecies(Id, Name, Compartment, InitialAmount,
#  IsConstant, IsBoundaryCondition, SubstanceUnit, HasOnlySubstanceUnits)
# Return a Species object.
inp_IFFL = model_obj.createNewSpecies('inp_IFFL','inp_IFFL','cell',50,False,False,'count',False)
DA_IFFL = model_obj.createNewSpecies('DA_IFFL','DA_IFFL','cell',50,False,False,'count',False)
C1_IFFL = model_obj.createNewSpecies('C1_IFFL','C1_IFFL','cell',0,False,False,'count',False)

mA_IFFL = model_obj.createNewSpecies('mA_IFFL','mA_IFFL','cell',0,False,False,'count',False)

pA_IFFL = model_obj.createNewSpecies('pA_IFFL','pA_IFFL','cell',0,False,False,'count',False)

C2_IFFL = model_obj.createNewSpecies('C2_IFFL','C2_IFFL','cell',0,False,False,'count',False)
DB_IFFL = model_obj.createNewSpecies('DB_IFFL','DB_IFFL','cell',50,False,False,'count',False)

mB_IFFL = model_obj.createNewSpecies('mB_IFFL','mB_IFFL','cell',0,False,False,'count',False)
pB_IFFL = model_obj.createNewSpecies('pB_IFFL','pB_IFFL','cell',0,False,False,'count',False)

C3_IFFL = model_obj.createNewSpecies('C3_IFFL','C3_IFFL','cell',0,False,False,'count',False)
DC_IFFL = model_obj.createNewSpecies('DC_IFFL','DC_IFFL','cell',50,False,False,'count',False)

C4_IFFL = model_obj.createNewSpecies('C4_IFFL','C4_IFFL','cell',0,False,False,'count',False)

C5_IFFL = model_obj.createNewSpecies('C5_IFFL','C5_IFFL','cell',0,False,False,'count',False)

C6_IFFL = model_obj.createNewSpecies('C6_IFFL','C6_IFFL','cell',0,False,False,'count',False)

mC_IFFL = model_obj.createNewSpecies('mC_IFFL','mC_IFFL','cell',0,False,False,'count',False)

out_IFFL = model_obj.createNewSpecies('out_IFFL','out_IFFL','cell',0,False,False,'count',False)

# Create all parameters 
# Usage - self.createNewParameter(Id, Name, Value, isConstant, Unit)
# Returns a Parameter object

k1f = model_obj.createNewParameter('k1f','k1f',1,False,'per_second')
k1r = model_obj.createNewParameter('k1r','k1r',1,False,'per_second')

k2f = model_obj.createNewParameter('k2f','k2f',1,False,'per_second')

k3f = model_obj.createNewParameter('k3f','k3f',1,False,'per_second')

k4f = model_obj.createNewParameter('k4f','k4f',1,False,'per_second')

k5f = model_obj.createNewParameter('k5f','k5f',1,False,'per_second')

k6f = model_obj.createNewParameter('k6f','k6f',1,False,'per_second')
k6r = model_obj.createNewParameter('k6r','k6r',1,False,'per_second')

k7f = model_obj.createNewParameter('k7f','k7f',1,False,'per_second')

k8f = model_obj.createNewParameter('k8f','k8f',1,False,'per_second')

k9f = model_obj.createNewParameter('k9f','k9f',1,False,'per_second')

k10f = model_obj.createNewParameter('k10f','k10f',1,False,'per_second')

k11f = model_obj.createNewParameter('k11f','k11f',1,False,'per_second')
k11r = model_obj.createNewParameter('k11r','k11r',1,False,'per_second')

k12f = model_obj.createNewParameter('k12f','k12f',1,False,'per_second')
k12r = model_obj.createNewParameter('k12r','k12r',1,False,'per_second')

k13f = model_obj.createNewParameter('k13f','k13f',1,False,'per_second')
k13r = model_obj.createNewParameter('k13r','k13r',1,False,'per_second')

k14f = model_obj.createNewParameter('k14f','k14f',1,False,'per_second')
k14r = model_obj.createNewParameter('k14r','k14r',1,False,'per_second')

k15f = model_obj.createNewParameter('k15f','k15f',1,False,'per_second')

k16f = model_obj.createNewParameter('k16f','k16f',1,False,'per_second')

k17f = model_obj.createNewParameter('k17f','k17f',1,False,'per_second')

k18f = model_obj.createNewParameter('k18f','k18f',1,False,'per_second')

# Create all reactions. To create a reaction there are 3 steps - createReactants, createProducts, createRateExpression
# Usage - Create an object of NewReaction class which allows the use of 
# createReactant, createProduct and other Reaction related member functions
# self.createNewReactant(species_id, isConstant, Stoichiometry)
# self.createMath(math_expression_as_a_string)

r1 = NewReaction(model_obj.createNewReaction('r1',True,False))
sref1_inp_IFFL = r1.createNewReactant('inp_IFFL',False,1)
sref1_DA_IFFL = r1.createNewReactant('DA_IFFL',False,1)
sref1_C1_IFFL = r1.createNewProduct('C1_IFFL',False,1)
math_r1 = r1.createMath('k1f * inp_IFFL * DA_IFFL - k1r * C1_IFFL')
r1_rate =  r1.createRate(math_r1)


r2 = NewReaction(model_obj.createNewReaction('r2',False,False))
sref2_C1_IFFL =  r2.createNewReactant('C1_IFFL',False,1)
sref2_C1_IFFL = r2.createNewProduct('C1_IFFL',False,1)
sref2_mA_IFFL = r2.createNewProduct('mA_IFFL',False,1)
math_r2 = r2.createMath('k2f * C1_IFFL')
r2_rate = r2.createRate(math_r2)

r3 = NewReaction(model_obj.createNewReaction('r3',False,False))
sref3_mA_IFFL = r3.createNewReactant('mA_IFFL',False,1)
sref3_mA_IFFL = r3.createNewProduct('mA_IFFL',False,1)
sref3_pA_IFFL = r3.createNewProduct('pA_IFFL',False,1)
math_r3 = r3.createMath('k3f * mA_IFFL')
r3_rate = r3.createRate(math_r3)

r4 = NewReaction(model_obj.createNewReaction('r4',False,False))
sref4_mA_IFFL = r4.createNewReactant('mA_IFFL',False,1)
math_r4 = r4.createMath('k4f * mA_IFFL')
r4_rate = r4.createRate(math_r4)

r5 = NewReaction(model_obj.createNewReaction('r5',False,False))
sref4_pA_IFFL = r5.createNewReactant('pA_IFFL',False,1)
math_r5 = r5.createMath('k5f * pA_IFFL')
r5_rate = r5.createRate(math_r5)

r6 = NewReaction(model_obj.createNewReaction('r6',True,False))
sref5_pA_IFFL = r6.createNewReactant('pA_IFFL',False,1)
sref5_DB_IFFL = r6.createNewReactant('DB_IFFL',False,1)
sref5_C2_IFFL = r6.createNewProduct('C2_IFFL',False,1)
math_r6 = r6.createMath('k6f * pA_IFFL * DB_IFFL - k6r * C2_IFFL')
r6_rate = r6.createRate(math_r6)

r7 = NewReaction(model_obj.createNewReaction('r7',False,False))
sref6_C2_IFFL = r7.createNewReactant('C2_IFFL',False,1)
sref6_C2_IFFL = r7.createNewProduct('C2_IFFL',False,1)
sref6_mB_IFFL = r7.createNewProduct('mB_IFFL',False,1)
math_r7 = r7.createMath('k7f * C2_IFFL')
r7_rate = r7.createRate(math_r7)

r8 = NewReaction(model_obj.createNewReaction('r8',False,False))
sref6_mB_IFFL = r8.createNewReactant('mB_IFFL',False,1)
sref6_mB_IFFL = r8.createNewProduct('mB_IFFL',False,1)
sref6_pB_IFFL = r8.createNewProduct('pB_IFFL',False,1)
math_r8 = r8.createMath('k8f * mB_IFFL')
r8_rate = r8.createRate(math_r8)

r9 = NewReaction(model_obj.createNewReaction('r9',False,False))
sref6_mB_IFFL = r9.createNewReactant('mB_IFFL',False,1)
math_r9 = r9.createMath('k9f * mB_IFFL')
r9_rate = r9.createRate(math_r9)

r10 = NewReaction(model_obj.createNewReaction('r10',False,False))
sref6_pB_IFFL = r10.createNewReactant('pB_IFFL',False,1)
math_r10 = r10.createMath('k10f * pB_IFFL')
r10_rate = r10.createRate(math_r10)

r11 = NewReaction(model_obj.createNewReaction('r11',True,False))
sref7_pB_IFFL = r11.createNewReactant('pB_IFFL',False,1)
sref7_DC_IFFL = r11.createNewReactant('DC_IFFL',False,1)
sref7_C3_IFFL = r11.createNewProduct('C3_IFFL',False,1)
math_r11 = r11.createMath('k11f * pB_IFFL * DC_IFFL - k11r * C3_IFFL')
r11_rate = r11.createRate(math_r11)

r12 = NewReaction(model_obj.createNewReaction('r12',True,False))
sref7_pA_IFFL = r12.createNewReactant('pA_IFFL',False,1)
sref7_DC_IFFL = r12.createNewReactant('DC_IFFL',False,1)
sref7_C4_IFFL = r12.createNewProduct('C4_IFFL',False,1)
math_r12 = r12.createMath('k12f * pA_IFFL * DC_IFFL - k12r * C4_IFFL')
r12_rate = r12.createRate(math_r12)

r13 = NewReaction(model_obj.createNewReaction('r13',True,False))
sref7_pA_IFFL = r13.createNewReactant('pA_IFFL',False,1)
sref7_C3_IFFL = r13.createNewReactant('C3_IFFL',False,1)
sref7_C5_IFFL = r13.createNewProduct('C5_IFFL',False,1)
math_r13 = r13.createMath('k13f * pA_IFFL * C3_IFFL - k13r * C5_IFFL')
r13_rate = r13.createRate(math_r13)

r14 = NewReaction(model_obj.createNewReaction('r14',True,False))
sref7_pB_IFFL = r14.createNewReactant('pB_IFFL',False,1)
sref7_C4_IFFL = r14.createNewReactant('C4_IFFL',False,1)
sref7_C6_IFFL = r14.createNewProduct('C6_IFFL',False,1)
math_r14 = r14.createMath('k14f * pB_IFFL * C4_IFFL - k14r * C6_IFFL')
r14_rate = r14.createRate(math_r14)

r15 = NewReaction(model_obj.createNewReaction('r15',False,False))
sref8_C4_IFFL = r15.createNewReactant('C4_IFFL',False,1)
sref8_C4_IFFL = r15.createNewProduct('C4_IFFL',False,1)
sref8_mC_IFFL = r15.createNewProduct('mC_IFFL',False,1)
math_r15 = r15.createMath('k15f * C4_IFFL')
r15_rate = r15.createRate(math_r15)

r16 = NewReaction(model_obj.createNewReaction('r16',False,False))
sref8_mC_IFFL = r16.createNewReactant('mC_IFFL',False,1)
sref8_mC_IFFL = r16.createNewProduct('mC_IFFL',False,1)
sref8_out_IFFL = r16.createNewProduct('out_IFFL',False,1)
math_r16 = r16.createMath('k16f * mC_IFFL')
r16_rate = r16.createRate(math_r16)

r17 = NewReaction(model_obj.createNewReaction('r17',False,False))
sref8_mC_IFFL = r17.createNewReactant('mC_IFFL',False,1)
math_r17 = r17.createMath('k17f * mC_IFFL')
r17_rate = r17.createRate(math_r17)

r18 = NewReaction(model_obj.createNewReaction('r18',False,False))
sref8_out_IFFL = r18.createNewReactant('out_IFFL',False,1)
math_r18 = r18.createMath('k18f * out_IFFL')
r18_rate = r18.createRate(math_r18)

# Write SBML file in XML
writeSBML(IFFL.getSubsystemDoc(),'models/IFFL.xml')

# Simulate 
timepoints = np.linspace(0,10,1000)
plotSbmlWithBioscrape('models/IFFL.xml',0,
timepoints, ['inp_IFFL', 'out_IFFL'], 'Time', 'Species',14,14)