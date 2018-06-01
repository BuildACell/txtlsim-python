import numpy as np
from libsbml import *
from modules.Subsystem import *
from modules.SimpleModel import *
from modules.System import *
# Create a system. Example - A cell system which acts as a container for 
# all the different subsystems. Here, cell is an object of the System class.
 
cell = System('cell')

# The ListOfSharedResources is a list to name all the species that are shared
# in the cell system. Usually, we would have something as follows - 
# system.ListOfSharedResources = ['RNAP','Ribo','ATP']

# For our simple example of DP and IFFL subsystems, we use the following for a working demo
cell.ListOfSharedResources = ['inp','Xp']


# Now, create a subsystem inside the cell as follows - 
# Usage self.createSubsystem(filename, string)
# The string can be anything and is used to name the components of the subsystem
# An object of the Subsystem classs is returned 
# and a list of subsystems being added to the cell is recorded. Here, DP1.
DP1 = cell.createSubsystem('models/DP.xml','DP1')

# There are other optional steps -

# (Optional) Give a new string to suffix all components of the model. 
# By default, the names are suffixed by the keyword given to make the Subsystem object.
# Usage -  DP1_doc = DP1.suffixAllElementIds('DPx')


# (Optional) Rename IDs of any species/compartments or any other component of the 
# subsystem as desired. This may be a helpful utility function to make sure 
# that the shared resources (and other interacting elements) have same IDs or names (as desired)
# To rename ID of a component and to propagate the changes everywhere in the model - 
# Usage - subsystem_object.renameSId(old_id, new_id) (where the ids are string type)
# DP1.renameSId('inp_DP1','inp_DP1_new')

# (Optional) Rename the names of any species -
# Usage - subsystem_object.renameSName(old_name, new_name)
# DP1.renameSName('inp', 'input')
# renames 'inp' named species to 'input'

# (Optional) Give a compartment to put the subsystem in. 
# By default, the subsystem is kept in the "cell" compartment (the System object used)
# Which compartment do you want to put the subsystem in? Usage --
# newCompartment = ['cell_new']
# DP1.setSubsystemCompartments(newCompartment)

# (Optional) Write the Subsystem model created to output an SBML file
# DP1_doc = DP1.getSubsystemDoc()
# writeSBML(DP1_doc,'models/DP1.xml')

# Using the steps shown above, we create two other subsystems - DP2 and IFFL

DP2 = cell.createSubsystem('models/DP.xml','DP2')

# newCompartment = ['cell_new']
# DP2.setSubsystemCompartments(newCompartment)
# writeSBML(DP2.getSubsystemDoc(),'models/DP2.xml')

# Creating an Incoherent Feedforward Loop subsystem 
IFFL = cell.createSubsystem('models/IFFL.xml','IFFL')

# Other methods available - 
# cell.getSystemName()
# cell.setSystemName('cell2')
# cell.getListOfSubsystems()
# cell.getListOfSharedResources()
# cell.appendSharedResources(['A','B'])
# cell.removeSharedResource('A')

# newCompartment = ['cell_new']
# IFFL.setSubsystemCompartments(newCompartment)
# IFFL_doc = IFFL.getSubsystemDoc()
# writeSBML(IFFL_doc,'models/IFFL.xml')

# Set the list of shared resources to the cell using its member function. Example 1-A
# Usage - system_obj.setSharedResources(), returns a new Subsystem
# object (inside the same system object) which has the resources sharing modeled.
shared_subsystem = cell.setSharedResources()

# (Optional) Write the shared document model to SBML file
writeSBML(shared_subsystem.getSubsystemDoc(),'models/DP_IFFL_shared.xml')

# The combineSubsystems member function implements Example 1-B.
# Usage - subsystem_object.combineSubsystems(ListOfSubsystems, combineAllWithSameNames)
# The subsystem_object is a new subsystem object which calls combineSubsystems
# As a result, the subsystem_object contains the combined model.

# The second argument is Boolean which is True if all species with same 
# names need to be merged and False otherwise. 

combined_subsystem = cell.createNewSubsystem(3,1)
combined_subsystem.combineSubsystems([DP1, DP2, IFFL], False)

# (Optional) Write the combined document model to SBML file
writeSBML(combined_subsystem.getSubsystemDoc(),'models/DP_IFFL_combined.xml')

# Now, for Example 1-C, the user needs to specify 
# the map of the interaction modeling that is desired. This map uses species names.
# User specifies how the systems interact by defining the following map
# Usage - connection_logic is a dictionary specifying the map. 
# The species in the key is replaced by the species given as the value 
connection_logic = {}
connection_logic['out'] = 'pA_IFFL'
# DP2.renameSName('out','out_DP2')
# connection_logic['out_DP2'] = 'pB_IFFL'

# (Optional) The following species was used in IFFL model for when its isolated.
# But, now DP output activates the protein expressions so the input to IFFL should be invalid. 
inputSpecies = 'inp_IFFL' #The species which is invalid in the connected model

# Call connectInteraction function for the final subsystem object
# to connect various subsystems.
# Usage - subsystem_object.self.connectSubsystems(ListOfSubsystems, combineAllWithSameNames, InteractionMap, InputSpecies)

connected_subsystem = cell.createNewSubsystem(3,1)
connected_subsystem.connectSubsystems([DP1, DP2, IFFL], True, connection_logic, inputSpecies)


# (Optional) Write the connected document to SBML file
writeSBML(connected_subsystem.getSubsystemDoc(),'odels/DP_IFFL_connected.xml')

# Simulate using bioscrape
timepoints = np.linspace(0,50,1000)
# Usage - plotSbmlWithBioscrape(filename, initialTime, timepoints, 
# ListOfSpeciesToPlot, xLabel, yLabel, xAxisSize, yAxisSize)

plotSbmlWithBioscrape('models/DP_IFFL_connected.xml',0,
timepoints,['inp','pA_IFFL','pB_IFFL','out_IFFL'],'Time',
'Input and Output Species',14,14)
