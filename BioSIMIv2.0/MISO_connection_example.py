import numpy as np
from libsbml import *
from modules.Subsystem import *
from modules.SimpleModel import *
from modules.System import *
# Create a system. Example - A cell system which acts as a container for 
# all the different subsystems 
cell = System('cell')
# ListOfSharedResources = ['RNAP','Ribo','ATP']
ListOfSharedResources = ['inp','Xp']
cell.setSharedResources(ListOfSharedResources)
# Steps to create a subsystem: 
DP1 = cell.createSubsystem('models/DP.xml','DP1')

# Two optional steps -
# 3. Give a string to suffix all components of the model. 
# By default, the names are suffixed by the keyword given to make the Subsystem object.
# 4. Give a compartment to add the subsystem to. 
# By default, the subsystem is kept in a compartment called "cell"

# (Optional) Step 3 - 
# This string will be used to suffix the model elements
# DP1_doc = DP1.suffixAllElementIds('DPx')
DP1_doc = DP1.getSubsystemDoc()
# (Optional) Step 4 -
# Which compartment do you want to put the subsystem in?
# newCompartmnet = []
# newCompartment = ['cell_new']
# DP1.setSubsystemCompartments(newCompartment)

# (Optional) Write the Subsystem model created to output an SBML file
writeSBML(DP1_doc,'models/DP1.xml')

# Creating another Double Phosphorylation subsystem, DP2 (with same steps)
DP2 = cell.createSubsystem('models/DP.xml','DP2')

# newCompartment = ['cell_new']
# DP2.setSubsystemCompartments(newCompartment)
writeSBML(DP2.getSubsystemDoc(),'models/DP2.xml')

# Creating an Incoherent Feedforward Loop subsystem 
IFFL = cell.createSubsystem('models/IFFL_sbmlNew.xml','IFFL')

# newCompartment = ['cell_new']
# IFFL.setSubsystemCompartments(newCompartment)
IFFL_doc = IFFL.getSubsystemDoc()
writeSBML(IFFL_doc,'models/IFFL.xml')
# create a blank document for the final connected system
final_sbml_doc = createSubsystemDoc(IFFL_doc.getLevel(),IFFL_doc.getVersion())
Final_subsystem = Subsystem(final_sbml_doc)

# Final_subsystem.shareSubsystems([DP1, DP2, IFFL], ListOfSharedResources)
# Final_subsystem.combineSubsystems([DP1, DP2, IFFL], True)

# user specifies how the systems interact by defining the following map
connection_logic = {}
connection_logic['out'] = 'pA_IFFL'
# connection_logic['out_DP2'] = 'pB_IFFL'

# Call the connect function by specifying the input and output subsystems and the logic map
inputSpecies = 'inp_IFFL' #The species which is invalid in the connected model

# Call connectInteraction function for the final subsystem object
# to connect various subsystems.
# The subsystem list to be connected together is given as an argument
# along with the connection map and input species

Final_subsystem.connectSubsystems([DP1, DP2, IFFL], True, connection_logic, inputSpecies)


# (Optional) Write the connected document to SBML file
writeSBML(Final_subsystem.getSubsystemDoc(),'models/DP_IFFL_connected.xml')

# Simulate 
timepoints = np.linspace(0,50,1000)
plotSbmlWithBioscrape('models/DP_IFFL_connected.xml',0,
timepoints,['inp','pA_IFFL','pB_IFFL','out_IFFL'],'Time',
'Input and Output Species',14,14)


# Add the option of globally common species
# add to init - maintain the combine in same compartments, 
# add cell compartment to every subsystem
