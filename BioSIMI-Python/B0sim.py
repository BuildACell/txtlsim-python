import numpy as np
from libsbml import *
from modules.Subsystem import *
from modules.System import *

cell = System('cell')

B0 = cell.createSubsystem('models/B0.xml','B0')
writeSBML(B0.getSubsystemDoc(),'models/B0converted.xml')
# Simulate using bioscrape
timepoints = np.linspace(0,14*60*60,1000)

plotSbmlWithBioscrape('models/B0converted.xml',0,
timepoints,['protein tetR','protein sigmaX'],'Time',
'concentration (nM)',14,14)
