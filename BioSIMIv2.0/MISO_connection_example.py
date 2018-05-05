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
writeSBML(DP1_doc,'models/DP1.xml')
# Read the original DP model 
DP_doc2 =  getFromXML('models/DP.xml')

# Create a new subsystem object to store the copy of the model
# The argument take
DPcopy2  = NewSubsystem(DP_doc2)
DP2_doc = DPcopy2.createNewSubsystem('2')
writeSBML(DP2_doc,'models/DP2.xml')
IFFL_doc = getFromXML('models/IFFL_sbmlNew.xml')

DP1_Subsystem = CreateSubsystem(DP1_doc)
DP2_Subsystem = CreateSubsystem(DP2_doc)
IFFL_Subsystem = CreateSubsystem(IFFL_doc)

# create a blank document for the final connected system
final_sbml_doc = createNewDocument(IFFL_doc.getLevel(),IFFL_doc.getVersion())
check(final_sbml_doc.createModel(),'creating model of final doc')
Final_subsystem = CreateSubsystem(final_sbml_doc)

# user specifies how the systems interact by defining the following map
connection_logic = {}
connection_logic['out_DP1'] = 'pA_IFFL'
connection_logic['out_DP2'] = 'pB_IFFL'

# Call the connect function by specifying the input and output subsystems and the logic map
Final_subsystem.connectInteraction([DP1_Subsystem, DP2_Subsystem],[IFFL_Subsystem], connection_logic)

# Write the connected document to SBML file

writeSBML(Final_subsystem.getNewDocument(),'models/DP_IFFL_connected.xml')


# Simulate 
timepoints = np.linspace(0,100,1000)
plotSbmlWithBioscrape('models/DP_IFFL_connected_2.xml',0,
timepoints,['inp_DP1','inp_DP2','out_IFFL'],'Time',
'Input and Output Species',14,14)