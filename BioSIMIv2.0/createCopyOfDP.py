from modules.CreateSubsystem import *
from modules.NewSubsystem import *
from modules.NewReaction import *
from modules.renameSId import *

# Read the original DP model 
DP_doc =  getFromXML('models/DP.xml')

# Create a new subsystem object to store the copy of the model
# The argument take
DPcopy  = NewSubsystem(DP_doc)

# Call the createNewSubsystem model with the object created 
# In the arguments, any string can be given. 
# This string will be used to suffix the model elements
# In this case, it's just "1", so a DP1 will be created 
DP1_doc = DPcopy.createNewSubsystem('new')

# Set the compartment for the model 
# (comment out the following lines if the new 
# model needs to be placed in the same compartment as the original)

# Use createNewCompartment from CreateSubsystem class to create
# a new compartment to hold the newly created model
# compartment = DP1_doc.getModel().getListOfCompartments()

# Write the new SBML document to XML file
writeSBML(DP1_doc,'models/DP1.xml')

# Simulate using bioscrape and plot
timepoints = np.linspace(0,10,1000)
plotSbmlWithBioscrape('models/DP1.xml',0,timepoints,
['inp_DPnew','out_DPnew'],'Time','Species',14,14)