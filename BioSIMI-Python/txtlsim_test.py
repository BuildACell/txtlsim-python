import numpy as np
from libsbml import *
from modules.Subsystem import *
from modules.SimpleModel import *
from modules.System import *

# Create system
cell = System('cell')
cell.ListOfSharedResources = ['RNAP','Ribo','AGTP','CUTP','AA']

# Create subsystems from SBML model files inside the system
S1 = cell.createSubsystem('models/txtlsimMATLAB_S1.xml','S1')
S2 = cell.createSubsystem('models/txtlsimMATLAB_S2.xml','S2')

# sharing
shared_subsystem = cell.setSharedResources()
writeSBML(shared_subsystem.getSubsystemDoc(),'models/txtl_shared.xml')

# combining
combined_subsystem = cell.createNewSubsystem(3,1)
combined_subsystem.combineSubsystems([S1,S2], True)
writeSBML(combined_subsystem.getSubsystemDoc(),'models/txtl_combined.xml')

# connecting
# user specifies how the systems interact by defining the following map
connection_logic = {}
# Use renameSName function to rename some species as desired
# S1.renameSName('protein deGFP','protein deGFP activated')
# S2.renameSName('RecBCD','activator')
# connection_logic['activator'] = 'protein deGFP activated'
# connected_subsystem = cell.createNewSubsystem(3,1)
# connected_subsystem.connectSubsystems([S1, S2], False, connection_logic)
# Write the connected document to SBML file
# writeSBML(connected_subsystem.getSubsystemDoc(),'models/txtl_connected.xml')


# # Simulate 
timepoints = np.linspace(0,10000,1000)
plotSbmlWithBioscrape('models/txtl_combined.xml',0,
# timepoints,['RNAP', 'Ribo', 'protein deGFP activated'],'Time',
timepoints,['RNAP', 'Ribo'],'Time',
'Input and Output Species',14,14)