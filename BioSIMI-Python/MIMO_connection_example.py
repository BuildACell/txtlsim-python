import numpy as np
from libsbml import *
from modules.Subsystem import *
from modules.SimpleModel import *
from modules.System import *

cell = System('cell')
ListOfSharedResources = ['inp','X']

DP1 = cell.createSubsystem('models/DP.xml','DP1')
DP2 = cell.createSubsystem('models/DP.xml','DP2')
IFFL1 = cell.createSubsystem('models/IFFL.xml','1')
IFFL2 = cell.createSubsystem('models/IFFL.xml','2')

# sharing
shared_subsystem = cell.setSharedResources(ListOfSharedResources)

writeSBML(shared_subsystem.getSubsystemDoc(),'models/MIMO_shared.xml')


combined_subsystem_doc = createSubsystemDoc(3,1)
combined_subsystem = Subsystem(combined_subsystem_doc)
combined_subsystem.combineSubsystems([DP1, DP2, IFFL1, IFFL2], False)


writeSBML(combined_subsystem.getSubsystemDoc(),'models/MIMO_combined.xml')
# user specifies how the systems interact by defining the following map
connection_logic = {}
DP1.renameSName('inp','inp_DP1')
DP2.renameSName('inp','inp_DP2')
DP1.renameSName('out','out_DP1')
DP2.renameSName('out','out_DP2')
IFFL1.renameSName('inp_IFFL','inp_IFFL1')
IFFL2.renameSName('inp_IFFL','inp_IFFL2')
connection_logic['out_DP1'] = 'pA_IFFL'
connection_logic['out_DP2'] = 'pB_IFFL'
inputSpecies = ['inp_IFFL1','inp_IFFL2']

connected_subsystem_doc = createSubsystemDoc(3,1)
connected_subsystem = Subsystem(connected_subsystem_doc)
connected_subsystem.connectSubsystems([DP1, DP2, IFFL1, IFFL2], True, connection_logic, inputSpecies)

# Write the connected document to SBML file
writeSBML(connected_subsystem.getSubsystemDoc(),'models/MIMO_connected.xml')


# Simulate 
timepoints = np.linspace(0,50,1000)
plotSbmlWithBioscrape('models/MIMO_connected.xml',0,
timepoints,['inp_DP1','inp_DP2','pA_IFFL','pB_IFFL','out_IFFL'],'Time',
'Input and Output Species',14,14)