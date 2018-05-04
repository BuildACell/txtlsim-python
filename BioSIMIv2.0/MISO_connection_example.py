import numpy as np
from libsbml import *
from modules.CreateSubsystem import *
from modules.NewReaction import *

# read all SBML models (for this example - Two DP systems and one IFFL system)
reader = SBMLReader()
doc_DP1 = reader.readSBML('models/DP1_sbml.xml')
DP1_subsystem = CreateSubsystem(doc_DP1)

doc_DP2 = reader.readSBML('models/DP2_sbml.xml')
DP2_subsystem = CreateSubsystem(doc_DP2)

doc_IFFL = reader.readSBML('models/IFFL_sbmlNew.xml')
IFFL_Subsystem = CreateSubsystem(doc_IFFL)

# create a blank document for the final connected system
final_sbml_doc = createNewDocument(doc_IFFL.getLevel(),doc_IFFL.getVersion())
check(final_sbml_doc.createModel(),'creating model of final doc')
Final_subsystem = CreateSubsystem(final_sbml_doc)

# user specifies how the systems interact by defining the following map
connection_logic = {}
connection_logic["out_DP1"] = "pA_IFFL"
connection_logic["out_DP2"] = "pB_IFFL"

# Call the connect function by specifying the input and output subsystems and the logic map
Final_subsystem.connectInteraction([DP1_subsystem, DP2_subsystem],[IFFL_Subsystem], connection_logic)

# Write the connected document to SBML file

writeSBML(Final_subsystem.getNewDocument(),'models/DP_IFFL_connected.xml')


# Simulate 
timepoints = np.linspace(0,100,1000)
plotSbmlWithBioscrape('models/DP_IFFL_connected.xml',0,
timepoints,['inp_DP1','inp_DP2','out_IFFL'],'Time',
'Input and Output Species',14,14)