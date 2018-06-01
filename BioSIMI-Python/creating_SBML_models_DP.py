##### Creating a Double Phosphorylation SBML model ####

from modules.System import *
from modules.Subsystem import *
from modules.SimpleModel import *
from modules.NewReaction import *

# Create a System to hold the Subsystems
cell = System('cell')

# Create a new SBML Document to hold the subsystem model
DP = cell.createNewSubsystem(3,1)

# Create a new model inside the document
model = DP.createNewModel('DP','second','mole','count')
# Creating the model object to use simple model creation commands that follow
model_obj = SimpleModel(model)

# Create a unit, arguments - id, unitKind, exponent, scale, multiplier
per_second = model_obj.createNewUnitDefinition('per_second',UNIT_KIND_SECOND,-1,0,1)
count = model_obj.createNewUnitDefinition('count',UNIT_KIND_DIMENSIONLESS, 1, 0, 1)


# createNewcompartment arguments - compartment ID, Name, Size, Units, isConstant
comp = model_obj.createNewCompartment('cell','cell',1,'litre',True)

# createNewSpecies arguments - id, name, compartment,
#  initial amount, isConstant, BoundaryCondition, Substance units, HasOnlySubstance

inp = model_obj.createNewSpecies( 'inp','inp','cell',50,False,False,'count',False)
X = model_obj.createNewSpecies( 'X','X','cell',50,False,False,'count',False)
C1 = model_obj.createNewSpecies( 'C1','C1','cell',0,False,False,'count',False)
Xp = model_obj.createNewSpecies( 'Xp','Xp','cell',0,False,False,'count',False)
E = model_obj.createNewSpecies( 'E','E','cell',50,False,False,'count',False)
C2 = model_obj.createNewSpecies( 'C2','C2','cell',0,False,False,'count',False)
C3 = model_obj.createNewSpecies( 'C3','C3','cell',0,False,False,'count',False)
out = model_obj.createNewSpecies( 'out','out','cell',0,False,False,'count',False)
C4 = model_obj.createNewSpecies( 'C4','C4','cell',0,False,False,'count',False)

# Create all parameters 
# arguments - id, name, value, isConstant, Unit id
k1f = model_obj.createNewParameter( 'k1f','k1f',1,False,'per_second')
k1r = model_obj.createNewParameter( 'k1r','k1r',1,False,'per_second')

k2f = model_obj.createNewParameter( 'k2f','k2f',1,False,'per_second')

k3f = model_obj.createNewParameter( 'k3f','k3f',1,False,'per_second')
k3r = model_obj.createNewParameter( 'k3r','k3r',1,False,'per_second')

k4f = model_obj.createNewParameter( 'k4f','k4f',1,False,'per_second')

k5f = model_obj.createNewParameter( 'k5f','k5f',1,False,'per_second')
k5r = model_obj.createNewParameter( 'k5r','k5r',1,False,'per_second')

k6f = model_obj.createNewParameter( 'k6f','k6f',1,False,'per_second')

k7f = model_obj.createNewParameter( 'k7f','k7f',1,False,'per_second')
k7r = model_obj.createNewParameter( 'k7r','k7r',1,False,'per_second')

k8f = model_obj.createNewParameter( 'k8f','k8f',1,False,'per_second')

# Create all reactions using the NewReaction class to call the simple commands to define Reactions
# Arguments - id, isReversible, isFast
r1 = NewReaction(model_obj.createNewReaction('r1',True,False))   
# Arguments - species id, isConstant, Stoichiometry
r1.createNewReactant('inp',False,1)
r1.createNewReactant('X',False,1)
r1.createNewProduct('C1',False,1)
math_r1 = r1.createMath('k1f * inp * X - k1r * C1')
r1.createRate(math_r1)


r2 = NewReaction(model_obj.createNewReaction('r2',False,False))
r2.createNewReactant('C1',False,1)
r2.createNewProduct('inp',False,1)
r2.createNewProduct('Xp',False,1)
math_r2 = r2.createMath('k2f * C1')
r2.createRate(math_r2)

r3 = NewReaction(model_obj.createNewReaction('r3',True,False))
r3.createNewReactant('E',False,1)
r3.createNewReactant('Xp',False,1)
r3.createNewProduct('C2',False,1)
math_r3 = r3.createMath('k3f * E * Xp - k3r * C2')
r3.createRate(math_r3)

r4 = NewReaction(model_obj.createNewReaction('r4',False,False))
r4.createNewReactant('C2',False,1)
r4.createNewProduct('E',False,1)
r4.createNewProduct('X',False,1)
math_r4 = r4.createMath('k4f * C2')
r4.createRate(math_r4)

r5 = NewReaction(model_obj.createNewReaction('r5',True,False))
r5.createNewReactant('inp',False,1)
r5.createNewReactant('Xp',False,1)
r5.createNewProduct('C3',False,1)
math_r5 = r5.createMath('k5f * inp * Xp - k5r * C3')
r5.createRate(math_r5)

r6 = NewReaction(model_obj.createNewReaction('r6',False,False))
r6.createNewReactant('C3',False,1)
r6.createNewProduct('out',False,1)
r6.createNewProduct('inp',False,1)
math_r6 = r6.createMath('k6f * C3')
r6.createRate(math_r6)

r7 = NewReaction(model_obj.createNewReaction('r7',True,False))
r7.createNewReactant('E',False,1)
r7.createNewReactant('out',False,1)
r7.createNewProduct('C4',False,1)
math_r7 = r7.createMath('k7f * E * out - k7r * C4')
r7.createRate(math_r7)

r8 = NewReaction(model_obj.createNewReaction('r8',False,False))
r8.createNewReactant('C4',False,1)
r8.createNewProduct('Xp',False,1)
r8.createNewProduct('E',False,1)
math_r8 = r8.createMath('k8f * C4')
r8.createRate(math_r8)

# Write to XML file 
writeSBML(DP.getSubsystemDoc(),'models/DP.xml')

# Simulate and plot using bioscrape
timepoints = np.linspace(0, 10, 1000)
plotSbmlWithBioscrape('models/DP.xml',0,timepoints,['inp','out'],'Time','Input/Output species',14,14)
