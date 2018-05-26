import numpy as np
from libsbml import *
from modules.Subsystem import *
from modules.System import *

cell = System('cell')

B1 = cell.createSubsystem('models/B1.xml','B1')
writeSBML(B1.getSubsystemDoc(),'models/B1converted.xml')
# Simulate using bioscrape
timepoints = np.linspace(0,14*60*60000,1000)

plotSbmlWithBioscrape('models/B1converted.xml',0,
timepoints,['protein tetR','protein sigmaX'],'Time',
'concentration (nM)',14,14)
