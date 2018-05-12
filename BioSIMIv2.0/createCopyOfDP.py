from modules.CreateSubsystem import *
from modules.Subsystem import *

# Read the original DP model 
# DP_doc =  getFromXML('models/DP.xml')

# Create a new subsystem object to store the copy of the model
# The argument take
DP = getFromXML('models/DP.xml')
subsystemDP  = Subsystem(DP)
DP1 = subsystemDP.renameAllElementIds('DP1')

# Set the compartment for the model 
# (comment out the following lines if the new 
# model needs to be placed in the same compartment as the original)
# (ToDo - default option add)
newCompartments = ['cell']
subsystemDP.setSubsystemCompartments(newCompartments)

# Use createNewCompartment from CreateSubsystem class to create
# a new compartment to hold the newly created model
# compartment = DP1_doc.getModel().getListOfCompartments()

# Write the new SBML document to XML file
writeSBML(DP1,'models/DP1.xml')

# Simulate using bioscrape and plot
timepoints = np.linspace(0,10,1000)
plotSbmlWithBioscrape('models/DP1.xml',0,timepoints,
['inp_DP1','out_DP1'],'Time','Species',14,14)