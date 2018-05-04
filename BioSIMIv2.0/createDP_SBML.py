from modules.CreateSubsystem import *
from modules.NewReaction import *

# Create a new SBML Document to hold the subsystem model
sbmlDoc1 = createNewDocument(3,1)
sbmlDoc = CreateSubsystem(sbmlDoc1)

# Create a new model inside the document
model = sbmlDoc.createNewModel("seconds","mole","count")

# Create a unit 
per_second = sbmlDoc.createNewUnit('per_second',UNIT_KIND_SECOND,-1,0,1)

# Create compartment 
comp = sbmlDoc.createNewCompartment('cell','cell',1,'litre',True)

# Create all species 
inp_DP1 = sbmlDoc.createNewSpecies( 'inp_DP1','inp_DP1','cell',50,False,False,'count',False)
X_DP1 = sbmlDoc.createNewSpecies( 'X_DP1','X_DP1','cell',50,False,False,'count',False)
C1_DP1 = sbmlDoc.createNewSpecies( 'C1_DP1','C1_DP1','cell',0,False,False,'count',False)
Xp_DP1 = sbmlDoc.createNewSpecies( 'Xp_DP1','Xp_DP1','cell',0,False,False,'count',False)
E_DP1 = sbmlDoc.createNewSpecies( 'E_DP1','E_DP1','cell',50,False,False,'count',False)
C2_DP1 = sbmlDoc.createNewSpecies( 'C2_DP1','C2_DP1','cell',0,False,False,'count',False)
C3_DP1 = sbmlDoc.createNewSpecies( 'C3_DP1','C3_DP1','cell',0,False,False,'count',False)
out_DP1 = sbmlDoc.createNewSpecies( 'out_DP1','out_DP1','cell',0,False,False,'count',False)
C4_DP1 = sbmlDoc.createNewSpecies( 'C4_DP1','C4_DP1','cell',0,False,False,'count',False)

# Create all parameters 
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

# Create all reactions

r1 = NewReaction(sbmlDoc.createNewReaction('r1',True,False))   
sref1_inp_DP1 = r1.createNewReactant('inp_DP1',False,1)
sref1_X_DP1 = r1.createNewReactant('X_DP1',False,1)
sref1_C1_DP1 = r1.createNewProduct('C1_DP1',False,1)
math_r1 = r1.createMath('k1f * inp_DP1 * X_DP1 - k1r * C1_DP1')
r1_rate = r1.createRate(math_r1)


r2 = NewReaction(sbmlDoc.createNewReaction('r2',False,False))
sref2_C1_DP1 = r2.createNewReactant('C1_DP1',False,1)
sref2_inp_DP1 = r2.createNewProduct('inp_DP1',False,1)
sref2_Xp_DP1 = r2.createNewProduct('Xp_DP1',False,1)
math_r2 = r2.createMath('k2f * C1_DP1')
r2_rate = r2.createRate(math_r2)

r3 = NewReaction(sbmlDoc.createNewReaction('r3',True,False))
sref3_E_DP1 = r3.createNewReactant('E_DP1',False,1)
sref3_Xp_DP1 = r3.createNewReactant('Xp_DP1',False,1)
sref3_C2_DP1 = r3.createNewProduct('C2_DP1',False,1)
math_r3 = r3.createMath('k3f * E_DP1 * Xp_DP1 - k3r * C2_DP1')
r3_rate = r3.createRate(math_r3)

r4 = NewReaction(sbmlDoc.createNewReaction('r4',False,False))
sref4_C2_DP1 = r4.createNewReactant('C2_DP1',False,1)
sref4_E_DP1 = r4.createNewProduct('E_DP1',False,1)
sref4_X_DP1 = r4.createNewProduct('X_DP1',False,1)
math_r4 = r4.createMath('k4f * C2_DP1')
r4_rate = r4.createRate(math_r4)

r5 = NewReaction(sbmlDoc.createNewReaction('r5',True,False))
sref5_inp_DP1 = r5.createNewReactant('inp_DP1',False,1)
sref5_Xp_DP1 = r5.createNewReactant('Xp_DP1',False,1)
sref5_C3_DP1 = r5.createNewProduct('C3_DP1',False,1)
math_r5 = r5.createMath('k5f * inp_DP1 * Xp_DP1 - k5r * C3_DP1')
r5_rate = r5.createRate(math_r5)

r6 = NewReaction(sbmlDoc.createNewReaction('r6',False,False))
sref6_C3_DP1 = r6.createNewReactant('C3_DP1',False,1)
sref6_out_DP1 = r6.createNewProduct('out_DP1',False,1)
sref6_inp_DP1 = r6.createNewProduct('inp_DP1',False,1)
math_r6 = r6.createMath('k6f * C3_DP1')
r6_rate = r6.createRate(math_r6)

r7 = NewReaction(sbmlDoc.createNewReaction('r7',True,False))
sref7_E_DP1 = r7.createNewReactant('E_DP1',False,1)
sref7_out_DP1 = r7.createNewReactant('out_DP1',False,1)
sref7_C4_DP1 = r7.createNewProduct('C4_DP1',False,1)
math_r7 = r7.createMath('k7f * E_DP1 * out_DP1 - k7r * C4_DP1')
r7_rate = r7.createRate(math_r7)

r8 = NewReaction(sbmlDoc.createNewReaction('r8',False,False))
sref8_C4_DP1 = r8.createNewReactant('C4_DP1',False,1)
sref8_Xp_DP1 = r8.createNewProduct('Xp_DP1',False,1)
sref8_E_DP1 = r8.createNewProduct('E_DP1',False,1)
math_r8 = r8.createMath('k8f * C4_DP1')
r8_rate = r8.createRate(math_r8)

# Write to XML file 
writeSBML(sbmlDoc.getNewDocument(),'models/DP1_sbml.xml')

# Simulate and plot using bioscrape
timepoints = np.linspace(0, 10, 1000)
plotSbmlWithBioscrape('models/DP1_sbml.xml',0,timepoints,['inp_DP1','out_DP1'],'Time','Input/Output species',14,14)
