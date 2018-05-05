import numpy as np
from libsbml import *
from modules.CreateSubsystem import *
from modules.NewReaction import *

# Read the original DP model 
DP_doc1 =  getFromXML('models/DP.xml')

# Create a new subsystem object to store the copy of the model
# The argument take
DPcopy1  = NewSubsystem(DP_doc1)

# Call the createNewSubsystem model with the object created 
# In the arguments, any string can be given. 
# This string will be used to suffix the model elements
# In this case, it's just "1" and "2", so a DP 1 and DP 2 will be created 
DP1_doc = DPcopy1.createNewSubsystem('1')
#
# writeSBML(DP1_doc,'models/DP1.xml')
# Read the original DP model 
DP_doc2 =  getFromXML('models/DP.xml')

# Create a new subsystem object to store the copy of the model
# The argument take
DPcopy2  = NewSubsystem(DP_doc2)
DP2_doc = DPcopy2.createNewSubsystem('2')
# writeSBML(DP2_doc,'models/DP2.xml')
IFFL_doc1 = getFromXML('models/IFFL_sbmlNew.xml')
IFFLcopy1 = NewSubsystem(IFFL_doc1)
IFFL_doc2 = IFFLcopy1.createNewSubsystem('1')

IFFL_doc1 = getFromXML('models/IFFL_sbmlNew.xml')

writeSBML(IFFL_doc1,'models/IFFL1.xml')
writeSBML(IFFL_doc2,'models/IFFL2.xml')

DP1_Subsystem = CreateSubsystem(DP1_doc)
DP2_Subsystem = CreateSubsystem(DP2_doc)
IFFL1_Subsystem = CreateSubsystem(IFFL_doc1)
IFFL2_Subsystem = CreateSubsystem(IFFL_doc2)

# create a blank document for the final connected system
final_sbml_doc = createNewDocument(IFFL_doc1.getLevel(),IFFL_doc1.getVersion())
check(final_sbml_doc.createModel(),'creating model of final doc')
Final_subsystem = CreateSubsystem(final_sbml_doc)

# user specifies how the systems interact by defining the following map
connection_logic = {}
connection_logic['out_DP1'] = 'pA_IFFL'
connection_logic['out_DP2'] = 'pA_IFFL1'

# Call the connect function by specifying the input and output subsystems and the logic map
Final_subsystem.connectInteraction([DP1_Subsystem, DP2_Subsystem],[IFFL1_Subsystem, IFFL2_Subsystem], connection_logic)

# Write the connected document to SBML file

writeSBML(Final_subsystem.getNewDocument(),'models/DP_IFFL_connected_MIMO.xml')


# Simulate 
timepoints = np.linspace(0,50,1000)
plotSbmlWithBioscrape('models/DP_IFFL_connected_MIMO.xml',0,
timepoints,['inp_DP1','inp_DP2','out_IFFL','out_IFFL1'],'Time',
'Input and Output Species',14,14)